import argparse
import math
from pathlib import Path

import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
import tifffile
from matplotlib import cm
from matplotlib import patches
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.colors import to_rgba
from matplotlib.patches import Rectangle
from matplotlib_scalebar.scalebar import ScaleBar
from scipy import ndimage
from skimage.measure import label, regionprops
from skimage.morphology import skeletonize
from tqdm import tqdm


def run():
    parser = argparse.ArgumentParser(description="Analyze cell extension orientation")

    # Define arguments
    parser.add_argument('--input_raw', type=str, required=True,
                        help="The input raw data as TIFF (2D, 1 channel).")
    parser.add_argument('--input_target', type=str, required=False,
                        help="Masked areas used for orientation calculation (optional).")
    parser.add_argument('--output', type=str, required=False,
                        help="Output folder for saving plots; if omitted, plots are displayed.")
    parser.add_argument('--output_res', type=str, default="12:9",
                        help="Resolution of output plots as WIDTH:HEIGHT, e.g., 800:600.")
    parser.add_argument('--roi', type=str, required=False,
                        help="Region of interest as MIN_X:MAX_X:MIN_Y:MAX_Y. Multiple ROIs are comma-separated.")
    parser.add_argument('--tiles', type=str, default="100,250,500",
                        help="Tile sizes for average plots, e.g., SIZE1,SIZE2,SIZE3.")
    parser.add_argument('--max_size', type=str, required=False,
                        help="Exclude segments with area above this size (pixels).")
    parser.add_argument('--min_size', type=str, required=False,
                        help="Exclude segments with area below this size (pixels).")
    parser.add_argument('--pixel_in_micron', type=float, required=False,
                        help="Pixel width in microns, for adding a scalebar.")
    parser.add_argument('--input_table', type=str, required=False,
                        help="Table of cells to analyze, with first column as label IDs.")
    parser.add_argument('--input_labeling', type=str, required=True,
                        help="Label map for segmentation analysis (2D, 1 channel).")

    # Parse arguments
    args = parser.parse_args()

    print('Reading raw image %s and segmentation %s..' % (args.input_raw, args.input_labeling))
    image_raw = tifffile.imread(args.input_raw).T
    image = tifffile.imread(args.input_labeling).T.astype(int)
    image_target_mask = None
    image_target_distances = None
    if args.input_target is not None:
        image_target_mask = tifffile.imread(args.input_target).T.astype(bool)
        image_target_distances = ndimage.distance_transform_edt(np.invert(image_target_mask))

    # crop input images to ROI
    roi, additional_rois = get_roi(args.roi, image)  # returns array with [min_x, max_x, min_y, max_y]
    image = image[roi[0]:roi[1], roi[2]:roi[3]]
    image_raw = image_raw[roi[0]:roi[1], roi[2]:roi[3]]
    if image_target_mask is not None:
        image_target_distances = image_target_distances[roi[0]:roi[1], roi[2]:roi[3]]
        image_target_mask = image_target_mask[roi[0]:roi[1], roi[2]:roi[3]]

    pixel_in_micron = args.pixel_in_micron

    regions = get_regions(image, args.min_size, args.max_size)
    cell_table_content  = analyze_segments(regions, image_target_distances, pixel_in_micron)
    write_table(cell_table_content, args.output)

    plot(cell_table_content, image_raw, image, roi, additional_rois, image_target_mask, pixel_in_micron, args.tiles,
         args.output, args.output_res)

def get_roi(crop, image):
    crop_min_x = 0
    crop_max_x = image.shape[0]
    crop_min_y = 0
    crop_max_y = image.shape[1]
    print('Input image dimensions: %sx%s' % (crop_max_x, crop_max_y))
    additional_rois = []
    roi = [crop_min_x, crop_max_x, crop_min_y, crop_max_y]
    if crop:
        crops = crop.split(",")
        for single_crop in crops:
            if len(str(single_crop).strip()) != 0:
                crop_parts = single_crop.split(":")
                if len(crop_parts) != 4:
                    exit(
                        "Please provide crop in the following form: MIN_X:MAX_X:MIN_Y:MAX_Y - for example 100:200:100:200")
                additional_rois.append([int(crop_parts[0]), int(crop_parts[1]), int(crop_parts[2]), int(crop_parts[3])])
        if len(additional_rois) == 1:
            roi = additional_rois[0]
            additional_rois = []
    return roi, additional_rois


def analyze_segments(regions, image_target, pixel_in_micron):

    cell_table_content = {
        "Label": {},
        "Area in px²": {},
        "Area in um²": {},
        "Mean": {},
        "XM": {},
        "YM": {},
        "X center biggest circle": {},
        "Y center biggest circle": {},
        "%Area": {},
        "AR": {},
        "Circ.": {},
        "Round": {},
        "Solidity": {},
        "MScore": {},
        "Length cell vector": {},
        "Absolute angle": {},
        "Rolling ball angle": {},
        "Relative angle": {},
    }
    for index, region in enumerate(tqdm(regions, desc="Processing Regions")):

        # write regionprops into table
        label = region.label

        cell_table_content["Label"][label] = label
        cell_table_content["Area in px²"][label] = region.area
        if pixel_in_micron:
            cell_table_content["Area in um²"][label] = region.area * (pixel_in_micron ** 2)
        cell_table_content["Mean"][label] = region.intensity_mean
        cell_table_content["XM"][label] = region.centroid[0]
        cell_table_content["YM"][label] = region.centroid[1]
        circularity = max(0, min(4 * math.pi * region.area / math.pow(region.perimeter, 2), 1.0))
        cell_table_content["Circ."][label] = circularity
        cell_table_content["%Area"][label] = region.area / region.area_filled * 100
        # cell_table_content["AR"][region.label] = ""
        # cell_table_content["Round"][region.label] = ""
        # cell_table_content["Solidity"][region.label] = ""
        if pixel_in_micron:
            cell_table_content["MScore"][label] = circularity * ((cell_table_content["Area in um²"][label] - 27) / 27)

        skeleton, center, length_cell_vector, absolute_angle, relative_angle, rolling_ball_angle = region_extension_analysis(region, image_target)

        cell_table_content["X center biggest circle"][label] = center[0]
        cell_table_content["Y center biggest circle"][label] = center[1]
        cell_table_content["Length cell vector"][label] = length_cell_vector
        cell_table_content["Absolute angle"][label] = absolute_angle
        cell_table_content["Rolling ball angle"][label] = rolling_ball_angle
        cell_table_content["Relative angle"][label] = relative_angle

    return cell_table_content


def region_extension_analysis(region, image_target):
    # skeletonize
    skeleton = skeletonize(region.intensity_image)
    # calculate distance map
    distance_region = ndimage.distance_transform_edt(region.intensity_image)
    minx, miny, maxx, maxy = region.bbox
    # calculate center
    center = np.unravel_index(np.argmax(distance_region, axis=None), distance_region.shape)
    distance_center = np.linalg.norm(distance_region[center])
    distances_center = np.indices(region.image.shape) - np.array(center)[:, None, None]
    distances_center = np.apply_along_axis(np.linalg.norm, 0, distances_center)
    # label inside/outside cell
    condition_outside = (skeleton > 0) & (distances_center - distance_center >= 0)
    pixel_locations_relevant_to_direction = np.column_stack(np.where(condition_outside))
    pixel_locations_relevant_to_direction = pixel_locations_relevant_to_direction - center
    center_translated = [center[0] + minx, center[1] + miny]
    target_vector = [0, 0]
    if image_target is not None:
        neighbor_x = [center_translated[0] + 1, center_translated[1]]
        neighbor_y = [center_translated[0], center_translated[1] + 1]
        if neighbor_x[0] < image_target.shape[0] and neighbor_y[1] < image_target.shape[1]:
            value_at_center = image_target[center_translated[0], center_translated[1]]
            value_at_neighbor_x = image_target[neighbor_x[0], neighbor_x[1]]
            value_at_neighbor_y = image_target[neighbor_y[0], neighbor_y[1]]
            target_vector = [value_at_center - value_at_neighbor_x, value_at_center - value_at_neighbor_y]
    length_cell_vector = 0
    absolute_angle = 0
    rolling_ball_angle = 0
    relative_angle = 0
    if len(pixel_locations_relevant_to_direction) > 1:
        mean_outside = np.mean(pixel_locations_relevant_to_direction, axis=0)
        length = np.linalg.norm(mean_outside)
        relative_angle = angle_between(target_vector, mean_outside)
        length_cell_vector = length
        absolute_angle = angle_between((0, 1), mean_outside)
        rolling_ball_angle = angle_between((0, 1), target_vector)
    return skeleton, center_translated, length_cell_vector, absolute_angle, relative_angle, rolling_ball_angle


def get_regions(labeled, min_size, max_size):
    # obtain labels
    print("Labeling segmentation..")
    # Heuristic: if the image has only two unique values and one is 0, assume it's a binary mask
    unique_vals = np.unique(labeled)
    if len(unique_vals) == 2 and 0 in unique_vals:
        # Binary mask case (e.g., 0 and 255)
        binary_mask = labeled != 0  # Covers 255 or 1 as foreground
        labeled, n_components = label(binary_mask, return_num=True)

    else:
        n_components = len(unique_vals)
    print(f'{n_components} objects detected.')
    # calculate region properties
    segmentation = labeled > 0
    regions = regionprops(label_image=labeled, intensity_image=segmentation)
    regions = filter_regions_by_size(min_size, max_size, n_components, regions)
    return regions


def filter_regions_by_size(min_size, max_size, n_components, regions):
    # sort out regions which are too big
    max_area = max_size
    if max_area:
        regions = [region for region in regions if region.area < int(max_area)]
        region_count = len(regions)
        print(
            "Ignored %s labels because their region is bigger than %s pixels" % (n_components - region_count, max_area))
    # sort out regions which are too small
    min_area = min_size
    if min_area:
        regions = [region for region in regions if region.area >= int(min_area)]
        region_count = len(regions)
        print("Ignored %s labels because their region is smaller than %s pixels" % (
            n_components - region_count, min_area))
    return regions


import numpy as np


def angle_between(v1, v2):
    """
    Returns the signed angle in radians between vectors 'v1' and 'v2' in the 2D plane.
    The result is in the interval (-π, π] where a positive value indicates that v2 is
    counterclockwise from v1, and a negative value indicates v2 is clockwise from v1.

    For example:
        angle_between((1, 0), (0, 1))  ->  1.5708  (90 degrees, v2 is counterclockwise from v1)
        angle_between((1, 0), (1, 0))  ->  0.0
        angle_between((1, 0), (-1, 0)) ->  3.1416 or -3.1416 (depending on convention)

    Parameters:
        v1, v2 : array-like
            Two-dimensional vectors with at least 2 components.

    Returns:
        float
            The signed angle in radians between v1 and v2.
    """
    # Ensure the vectors are 2D (only x and y components) and non-zero length
    if (v1[0] == 0 and v1[1] == 0) or (v2[0] == 0 and v2[1] == 0):
        return 0.0

    # Normalize the vectors
    v1_u = np.array(v1) / np.linalg.norm(v1)
    v2_u = np.array(v2) / np.linalg.norm(v2)

    # Compute the dot product and ensure it is within the valid range for arccos/arctan2
    dot = np.dot(v1_u, v2_u)
    dot = np.clip(dot, -1.0, 1.0)

    # Compute the determinant (which is equivalent to the 2D cross product's magnitude)
    det = v1_u[0] * v2_u[1] - v1_u[1] * v2_u[0]

    # Use arctan2 to get the signed angle
    angle = np.arctan2(det, dot)
    return angle


def write_table(cell_table_content, output):
    if cell_table_content is not None:
        if output:
            output = Path(output)
            output.mkdir(parents=True, exist_ok=True)
            pd.DataFrame(data=cell_table_content).to_csv(output.joinpath("cells.csv"))

def plot(cell_table, raw_image, label_image, roi, additional_rois, image_target_mask, pixel_in_micron, tiles, output, output_res):
    if output:
        output = Path(output)
        output.mkdir(parents=True, exist_ok=True)
    output_res = output_res.split(':')
    output_res = [int(output_res[0]), int(output_res[1])]
    roi_colors = []
    if len(additional_rois) > 0:
        roi_colors = plot_rois(output, output_res, label_image, roi, additional_rois)
    directions = create_arrows(cell_table, image_target_mask)
    plot_all_directions(output, output_res, directions, label_image, roi, additional_rois, roi_colors, image_target_mask, pixel_in_micron)
    for tile in tiles.split(','):
        plot_average_directions(output, output_res, directions, raw_image, roi, additional_rois, roi_colors,
                                tile_size=int(tile), image_target_mask=image_target_mask, pixel_in_micron=pixel_in_micron)
    if output:
        print("Results writen to %s" % output)


def create_arrows(cell_table_content, image_target_mask):
    """
    Generate arrow definitions for each cell based on a fully computed cell table.

    Parameters:
        cell_table_content (dict): Dictionary with keys for each metric and values that are sub-dictionaries
            mapping label -> measurement. Expected keys include "Label", "XM", "YM",
            "length_cell_vector", "absolute_angle", and "relative_angle".

    Returns:
        numpy.ndarray: An array with one arrow per cell. Each arrow is a list of the form:
            [center, vector, [relative_angle, arrow_length]]
                - center: [x_center, y_center]
                - vector: [dx, dy] computed from absolute_angle and length_cell_vector
                - [relative_angle, arrow_length]: additional metadata
    """
    arrows = []
    # Loop over all labels stored in the table.
    # Assume that cell_table_content["Label"] is a dict where keys are the label IDs.
    for label in cell_table_content["Label"]:
        XM = cell_table_content["X center biggest circle"][label]
        YM = cell_table_content["Y center biggest circle"][label]
        center = [XM, YM]

        # Get the extension length and angle from the table.
        length_vector = cell_table_content["Length cell vector"][label]
        absolute_angle = cell_table_content["Absolute angle"][label]
        relative_angle = cell_table_content["Relative angle"][label]

        # Compute the components of the arrow using the absolute angle.
        # This assumes the standard mathematical convention:
        # dx = L * sin(theta), dy = L * cos(theta)
        dx = length_vector * np.sin(absolute_angle)
        dy = length_vector * np.cos(absolute_angle)
        # Assemble the arrow.
        arrow = [center, [dx, dy], [relative_angle if image_target_mask is not None else absolute_angle, length_vector]]
        arrows.append(arrow)

    return np.array(arrows)


def plot_average_directions(output, output_res, arrows, bg_image, roi, additional_rois, roi_colors, tile_size,
                            image_target_mask, pixel_in_micron):
    shape = bg_image.shape
    print("Calculating average directions, tile size %s..." % tile_size)
    u, v, x, y, counts = calculate_average_directions(arrows, shape, roi, tile_size, image_target_mask)
    rois = [roi]
    rois.extend(additional_rois)
    colors = ['black']
    colors.extend(roi_colors)
    print("Plotting average directions...")
    plt.figure("Average directions tile size %s" % tile_size, figsize=output_res)
    plt.imshow(bg_image.T, extent=roi, origin='upper', cmap='gray')
    ax = plt.gca()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    if pixel_in_micron:
        scalebar = ScaleBar(pixel_in_micron, 'um', location='upper right', color='white', box_color='black')
        plt.gca().add_artist(scalebar)
    plot_grid(x, y, u, v, counts, tile_size, image_target_mask)
    if image_target_mask is not None:
        generate_target_contour(image_target_mask)
    plt.margins(0, 0)
    plt.tight_layout(pad=1)
    if output:
        for i, region in enumerate(rois):
            adjust_to_region(roi[3] + roi[2], region, colors[i], scalebar if pixel_in_micron else None)
            # plt.tight_layout(pad=1)
            plt.savefig(output.joinpath(
                'directions_%s-%s-%s-%s_tile%s.png' % (region[0], region[1], region[2], region[3], tile_size)))
        plt.close()
    else:
        plt.show()


def calculate_average_directions(directions, shape, crop_extend, tile_size, image_target_mask):
    tiles_num_x = int(shape[0] / tile_size)+1
    tiles_num_y = int(shape[1] / tile_size)+1

    # tile centers
    x = np.array([tile_x * tile_size + crop_extend[0] for tile_x, _ in np.ndindex(tiles_num_x, tiles_num_y)], dtype=int)
    y = np.array([tile_y * tile_size + crop_extend[2] for _, tile_y in np.ndindex(tiles_num_x, tiles_num_y)], dtype=int)

    arrow_indices_x = np.array([int((arrow[0][0] - crop_extend[0]) / tile_size) for arrow in directions])
    arrow_indices_y = np.array([int((shape[1]-arrow[0][1] - crop_extend[2]) / tile_size) for arrow in directions])
    counts = [np.count_nonzero((arrow_indices_x == index_x) & (arrow_indices_y == index_y)) for index_x, index_y in
              np.ndindex(tiles_num_x, tiles_num_y)]
    where = [np.asarray((arrow_indices_x == index_x) & (arrow_indices_y == index_y)).nonzero() for index_x, index_y in
             np.ndindex(tiles_num_x, tiles_num_y)]
    max_length = np.mean(directions[:][:, 2, 1])
    print(max_length)

    # weighted sum of the relative angle of an arrow in relation to a target (weights: length of the arrow)
    # sum_weighted_angle = [np.sum(directions[arrow_indices[0]][:, 2, 0] * directions[arrow_indices[0]][:, 2, 1]) for
    if image_target_mask is not None:
        avg_angle = [np.mean((np.pi-np.abs(directions[arrow_indices[0]][:, 2, 0])) * directions[arrow_indices[0]][:, 2, 1]/max_length) for arrow_indices in where]
        sum_weights = [np.sum(directions[arrow_indices[0]][:, 2, 1]) for arrow_indices in where]
        avg_length = np.divide(sum_weights, counts, out=np.zeros_like(avg_angle),
                               where=np.array(counts, dtype=int) != 0)
        u = avg_angle
        v = avg_length
    else:
        u = [-np.mean(directions[arrow_indices[0]][:, 1, 0]) for arrow_indices in where]
        v = [-np.mean(directions[arrow_indices[0]][:, 1, 1]) for arrow_indices in where]

    return u, v, x, y, counts


def plot_arrows(x, y, u, v):
    norm = Normalize(-np.pi, np.pi)
    colors = np.arctan2(v, u)
    colormap = cm.hsv
    return plt.quiver(x, y, u, v, color=colormap(norm(colors)), angles='xy', width=0.003)


def plot_arrows_relative(x, y, u, v, relative_angle):
    norm = Normalize(0, np.pi)
    colors = np.pi - np.abs(relative_angle)
    colormap = cm.coolwarm
    return plt.quiver(x, y, u, v, color=colormap(norm(colors)), angles='xy', width=2, units='dots')


def plot_grid(x, y, u, v, counts, tile_size, image_target_mask):

    if image_target_mask is not None:
        norm = Normalize(0, np.pi)
        colors_legend = u
        colormap = cm.coolwarm
        colors = u
    else:
        norm = Normalize(-np.pi, np.pi)
        ph = np.linspace(-np.pi, np.pi, 13)
        scale_start = 30.
        offset = 40.
        x_legend = scale_start * np.cos(ph) + offset
        y_legend = scale_start * np.sin(ph) + offset
        u_legend = np.cos(ph) * scale_start * 0.5 + offset
        v_legend = np.sin(ph) * scale_start * 0.5 + offset
        colors_legend = np.arctan2(np.sin(ph), np.cos(ph))
        # norm.autoscale(colors_legend)
        colormap = cm.hsv
        colors = np.arctan2(v, u)

    max_length = 10.
    max_count = tile_size * tile_size / 10000.
    for index, _x in enumerate(x):
        _y = y[index]
        if image_target_mask is not None:
            average_length = v[index]
        else:
            average_length = np.linalg.norm([u[index], v[index]])
        cell_count = float(counts[index])
        alpha = min(1., cell_count / max_count) * min(1., average_length / max_length) * 0.9
        facecolor = to_rgba(colormap(norm(colors[index])), alpha)
        plt.gca().add_patch(Rectangle((_x, _y), tile_size, tile_size, facecolor=facecolor))

    if image_target_mask is None:
        for index, _x in enumerate(x_legend):
            pos1 = [_x, y_legend[index]]
            pos2 = [u_legend[index], v_legend[index]]
            plt.annotate('', pos1, xytext=pos2, xycoords='axes pixels', arrowprops={
                'width': 3., 'headlength': 4.4, 'headwidth': 7., 'edgecolor': 'black',
                'facecolor': colormap(norm(colors_legend[index]))
            })
    else:
        sm = plt.cm.ScalarMappable(cmap=colormap)
        sm.set_array(norm(colors))
        cbar = plt.colorbar(sm, ax=plt.gca(), location='bottom', pad=0.01, aspect=50)
        vmin, vmax = cbar.vmin, cbar.vmax
        cbar.set_ticks([vmin, vmax])
        cbar.set_ticklabels(['Moving away from target', 'Moving towards target'])
        cbar.ax.xaxis.get_majorticklabels()[0].set_horizontalalignment('left')
        cbar.ax.xaxis.get_majorticklabels()[-1].set_horizontalalignment('right')
        circ1 = mpatches.Rectangle((0,0), 1, 1, edgecolor='#ff0000', facecolor='#000000', hatch=r'O', label='target')
        plt.legend(handles=[circ1], loc=2, handlelength=4, handleheight=4)
        # legend = plt.gca().legend(handles=[cbar, patch], loc='lower center', bbox_to_anchor=(0.5, -0.3))
    # plt.quiver(x+tile_size/2., y+tile_size/2., u, v, color=colormap(norm(colors)), angles='xy', scale_units='xy', scale=0.5)


def plot_all_directions(output, output_res, directions, bg_image, roi, additional_rois, additional_roi_colors,
                        image_target_mask, pixel_in_micron):
    print("Plotting all directions...")
    rois = [roi]
    rois.extend(additional_rois)
    colors = ['black']
    colors.extend(additional_roi_colors)
    fig = plt.figure("All directions", output_res)
    plt.imshow(bg_image.T, extent=roi, origin='upper', cmap='gray')
    scalebar = None
    if pixel_in_micron:
        scalebar = ScaleBar(pixel_in_micron, 'um', location='upper right', color='white', box_color='black')
        plt.gca().add_artist(scalebar)
    # bg_image_with_arrows = np.array(bg_image)

    if image_target_mask is not None:
        generate_target_contour(image_target_mask)

    x = directions[:, 0, 0]
    y = roi[3]-directions[:, 0, 1]
    u = -directions[:, 1, 0]
    v = -directions[:, 1, 1]
    rel_angle = directions[:, 2, 0]

    # plt.scatter(x, y, color='white', s=15)
    if image_target_mask is not None:
        quiver = plot_arrows_relative(x, y, u, v, rel_angle)
        # draw_arrows(bg_image_with_arrows, x, y, u, v, rel_angle)
    else:
        quiver = plot_arrows(x, y, u, v)

    # Image.fromarray(bg_image_with_arrows).save('directions.tif')

    plt.margins(0, 0)
    plt.tight_layout(pad=1)
    if output:
        for i, region in enumerate(rois):
            adjust_to_region(roi[3] + roi[2], region, colors[i], scalebar if pixel_in_micron else None)
            plt.savefig(output.joinpath('directions_%s-%s-%s-%s.png' % (region[0], region[1], region[2], region[3])))
        plt.close()
    print("Done printing all directions")


def generate_target_contour(image_target_mask):
    plt.contour(image_target_mask.T, 1, origin='upper', colors='red')
    cs = plt.contourf(image_target_mask.T, 1, hatches=['', 'O'], origin='upper', colors='none')
    cs.set_edgecolor((1, 0, 0.2, 1))


def adjust_to_region(data_height, region, region_color, scalebar):
    plt.setp(plt.gca().spines.values(), color=region_color)
    plt.setp([plt.gca().get_xticklines(), plt.gca().get_yticklines()], color=region_color)
    [x.set_linewidth(2) for x in plt.gca().spines.values()]
    plt.xlim(region[0], region[1])
    plt.ylim(data_height - region[3], data_height - region[2])
    if scalebar:
        scalebar.remove()
        plt.gca().add_artist(scalebar)


def plot_rois(output, output_res, bg_image, roi, additional_rois):
    print("Plotting ROIs...")
    plt.figure("ROIs", output_res)
    plt.imshow(bg_image, extent=roi, origin='upper', cmap='gray', vmin=0, vmax=1)
    indices = [i for i, _ in enumerate(additional_rois)]
    norm = Normalize()
    norm.autoscale(indices)
    colormap = cm.rainbow
    colors = colormap(norm(indices))
    for i, region in enumerate(additional_rois):
        rect = patches.Rectangle((region[0], bg_image.shape[0] - region[3]), region[1] - region[0],
                                 region[3] - region[2],
                                 linewidth=1, edgecolor=colors[i], facecolor='none')
        plt.gca().add_patch(rect)
    plt.margins(0, 0)
    plt.tight_layout(pad=1)
    plt.savefig(output.joinpath('ROIs.png'))
    plt.close()
    return colors

