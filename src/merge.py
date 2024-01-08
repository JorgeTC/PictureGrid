from get_images import get_all_images, sort_images
from iter import IterGrid
from make_image import make_image_from_list
from settings import Grid, OutImage, SrcImages


def check_grid_size(grid: IterGrid, images_len: int):
    grid_size = grid.rows * grid.columns
    if grid_size != images_len:
        raise ValueError(f'{images_len} were found. '
                         f'Grid size is {grid_size}')


def main():
    images_paths = get_all_images(SrcImages.DIR, SrcImages.EXTENSIONS)

    grid_dim = IterGrid(Grid.ROWS, Grid.COLUMNS)

    # Raise error if amount of images is not correct
    check_grid_size(grid_dim, len(images_paths))

    # Sort images by colour
    images_list = sort_images(images_paths, grid_dim)
    array_list = [image.array for image in images_list]

    # Create a image with the images in grid disposition
    make_image_from_list(array_list, grid_dim,
                         OutImage.PPP, OutImage.PATH, OutImage.BACKGROUND_COLOR)


if __name__ == '__main__':
    main()
