from math import inf
from pathlib import Path

import matplotlib.pyplot as plt
from numpy import ndarray

from iter import IterGrid

# Constants for margins and spacing
MARGIN_RATIO = 0.05  # Fraction of the figure width/height used as margin
SPACING_RATIO = 0.1  # Fraction of space between images in the grid


def add_images_to_axes(axes: ndarray, images: list[ndarray], grid: IterGrid):
    for position, image in zip(grid.iterate_diagonals(), images):
        # Get the corresponding cell in the grid
        cell: plt.Axes = axes[position.row, position.column]

        # Hide axes and display the image
        cell.axis('off')
        cell.imshow(image, cmap='gray', vmin=0, vmax=255)
        cell.set_aspect('auto')


def calculate_grid_size(images: list[ndarray], grid: IterGrid, pixels_per_inch: int) -> tuple[int, int]:
    row_heights = [inf] * grid.rows
    column_widths = [inf] * grid.columns

    for position, image in zip(grid.iterate_diagonals(), images):
        column_widths[position.column] = min(column_widths[position.column], image.shape[1])
        row_heights[position.row] = min(row_heights[position.row], image.shape[0])

    total_width_pixels = sum(column_widths)
    total_height_pixels = sum(row_heights)

    total_width_inches = total_width_pixels / pixels_per_inch
    total_height_inches = total_height_pixels / pixels_per_inch

    return total_width_inches, total_height_inches


def calculate_spacing_ratios(images: list[ndarray]) -> tuple[float, float]:
    poster_aspect_ratio = images[0].shape[0] / images[0].shape[1]
    horizontal_spacing = SPACING_RATIO
    vertical_spacing = horizontal_spacing / poster_aspect_ratio
    return horizontal_spacing, vertical_spacing


def make_image_from_list(images: list[ndarray], grid: IterGrid,
                         pixels_per_inch: int, output_path: Path,
                         background_color: tuple[float, float, float]):
    # Calculate the total grid size in inches
    grid_width, grid_height = calculate_grid_size(images, grid, pixels_per_inch)

    # Calculate spacing between subplots
    horizontal_spacing, vertical_spacing = calculate_spacing_ratios(images)

    # Create the figure and axes
    fig, axes = plt.subplots(grid.rows, grid.columns)
    fig.set_facecolor(background_color)

    # Populate the grid with images
    add_images_to_axes(axes, images, grid)

    # Adjust the figure size to include margins
    margin_width = MARGIN_RATIO * grid_width
    margin_height = MARGIN_RATIO * grid_height
    total_width = grid_width + 2 * margin_width
    total_height = grid_height + 2 * margin_height
    fig.set_size_inches(total_width, total_height)

    # Configure subplot spacing
    plt.subplots_adjust(
        left=MARGIN_RATIO,
        right=1 - MARGIN_RATIO,
        bottom=MARGIN_RATIO,
        top=1 - MARGIN_RATIO,
        wspace=horizontal_spacing,
        hspace=vertical_spacing
    )

    # Save the figure with high resolution
    output_format = output_path.suffix.strip('.')
    plt.savefig(output_path, format=output_format, dpi=pixels_per_inch * 2,
                bbox_inches='tight', pad_inches=MARGIN_RATIO / 2)
    plt.close(fig)  # Close the figure to free memory
