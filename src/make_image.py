from math import inf
from pathlib import Path

import matplotlib.pyplot as plt
from numpy import ndarray

from iter import IterGrid


def add_images_to_axes(axes: ndarray, arrays_list: list[ndarray], grid: IterGrid):
    for position, array in zip(grid.iterate_diagonals(), arrays_list):
        # Get to the next cell
        cell: plt.Axes = axes[position.row, position.column]

        # Turn off the axis
        cell.axis('off')
        # Set the image to the position
        cell.imshow(array, cmap='gray', vmin=0, vmax=255)


def get_fig_size(arrays_list: list[ndarray], grid: IterGrid, ppp: int) -> tuple[int, int]:
    rows_height = [inf] * grid.rows
    columns_width = [inf] * grid.columns

    for position, array in zip(grid.iterate_diagonals(), arrays_list):
        columns_width[position.column] = min(columns_width[position.column],
                                             array.shape[1])
        rows_height[position.row] = min(rows_height[position.row],
                                        array.shape[0])

    total_width = sum(columns_width)
    total_height = sum(rows_height)

    return int(total_width / ppp), int(total_height / ppp)


def make_image_from_list(array_list: list[ndarray], grid: IterGrid,
                         ppp: int, output_file: Path, background_color: tuple[float, float, float]):

    # Calculate the total width and height of the images in the grid
    total_width, total_height = get_fig_size(array_list, grid, ppp)
    # Create plt plot:
    fig, axes = plt.subplots(grid.rows, grid.columns)

    # Set the size of the figure to match the total width and height
    fig.set_size_inches(total_width, total_height)
    fig.set_facecolor(background_color)

    # Populate the grid
    add_images_to_axes(axes, array_list, grid)

    plt.subplots_adjust(left=None, bottom=None, right=None, top=None,
                        wspace=0, hspace=0)
    # Save the plot as a jpg file
    plt.savefig(output_file, pad_inches=0,
                dpi=ppp, bbox_inches='tight')
