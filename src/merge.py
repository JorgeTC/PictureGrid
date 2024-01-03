import matplotlib.pyplot as plt
from numpy import ndarray

from get_images import get_all_images, sort_images, ImageRGB
from settings import Grid, SrcImages, OutImage
from iter import IterGrid


def add_images_to_axes(axes: ndarray, images_list: list[ImageRGB], grid: IterGrid):
    for position, image in zip(grid.iterate_diagonals(), images_list):
        # Get to the next cell
        cell: plt.Axes = axes[position.row, position.column]

        # Turn off the axis
        cell.axis('off')
        # Set the image to the position
        cell.imshow(image.array, cmap='gray', vmin=0, vmax=255)


def get_fig_size(images_list: list[ImageRGB], grid: IterGrid) -> tuple[int, int]:
    rows_height = [0] * grid.rows
    columns_width = [0] * grid.columns

    images_arrays = (image.array for image in images_list)
    for position, array in zip(grid.iterate_diagonals(), images_arrays):
        columns_width[position.column] = max(columns_width[position.column],
                                             array.shape[1])
        rows_height[position.row] = max(rows_height[position.row],
                                        array.shape[0])

    total_width = sum(columns_width)
    total_height = sum(rows_height)

    return int(total_width / OutImage.PPP), int(total_height / OutImage.PPP)


def check_grid_size(grid: IterGrid, images_len: int):
    grid_size = grid.rows * grid.columns
    if grid_size != images_len:
        raise ValueError(f'{images_len} were found. '
                         f'Grid size is {grid_size}')


def make_image_from_list(images_list: list[ImageRGB], grid: IterGrid):
    # Calculate the total width and height of the images in the grid
    total_width, total_height = get_fig_size(images_list, grid)
    # Create plt plot:
    fig, axes = plt.subplots(grid.rows, grid.columns)

    # Set the size of the figure to match the total width and height
    fig.set_size_inches(total_width, total_height)
    fig.set_facecolor(OutImage.BACKGROUND_COLOR)

    # Populate the grid
    add_images_to_axes(axes, images_list, grid)

    plt.subplots_adjust(left=None, bottom=None, right=None, top=None,
                        wspace=0, hspace=0)
    # Save the plot as a jpg file
    plt.savefig(OutImage.PATH, pad_inches=0,
                dpi=OutImage.PPP, bbox_inches='tight')


def main():
    images_paths = get_all_images(SrcImages.DIR, SrcImages.EXTENSIONS)

    grid_dim = IterGrid(Grid.ROWS, Grid.COLUMNS)

    # Raise error if amount of images is not correct
    check_grid_size(grid_dim, len(images_paths))

    # Sort images by colour
    images_list = sort_images(images_paths, grid_dim)

    # Create a image with the images in grid disposition
    make_image_from_list(images_list, grid_dim)


if __name__ == '__main__':
    main()
