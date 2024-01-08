import colorsys
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image

from iter import IterGrid
from make_image import make_image_from_list
from settings import DebugImage


@dataclass
class RGB:
    '''
    RGB color stored as 0-255 numbers
    '''
    r: float
    g: float
    b: float

    @property
    def norm(self) -> float:
        return math.hypot(self.r, self.g, self.b)

    @property
    def spectre(self) -> float:
        h, l, s = colorsys.rgb_to_hls(self.r, self.g, self.b)
        return (h + 0.5) % 1

    def as_linear(self) -> tuple[float, float, float]:
        return (self.r/255, self.g/255, self.b/255)


class ImageRGB:
    def __init__(self, image: Path) -> None:
        self.path = image
        with Image.open(image) as open_image:
            self.array = np.asarray(open_image)
        self.color: RGB = get_average_colour(self.array)


def get_all_images(folder: Path, acceptable_extensions: set[str]) -> list[Path]:
    children = (path for path in folder.iterdir())
    files = (path for path in children if path.is_file())
    images = (file for file in files if file.suffix in acceptable_extensions)
    return list(images)


def sort_images(images: list[Path], grid: IterGrid) -> list[ImageRGB]:
    average_colors = [ImageRGB(image) for image in images]
    average_colors.sort(reverse=True, key=lambda im: im.color.norm)

    # Create a list to store every diagonal
    diagonals: list[ImageRGB] = []
    for diagonal in range(grid.diagonals):
        d_length = grid.diagonal_length(diagonal)
        new_diagonal = [average_colors.pop()
                        for _ in range(d_length)]
        sort_diagonal(new_diagonal)
        diagonals.extend(new_diagonal)

    debug_colors(diagonals, grid)

    return diagonals


def sort_diagonal(diagonal: list[ImageRGB]):
    diagonal.sort(reverse=True, key=lambda im: im.color.spectre)


def split_alpha_channel(image_array: np.ndarray) -> tuple[np.ndarray, np.ndarray | None]:
    # Check the current image has alpha channel
    if len(image_array.shape) == 3:
        if image_array.shape[-1] == 4:
            rgb_values = image_array[..., :3]
            alpha_channel = image_array[..., 3]
            alpha_channel = np.stack([alpha_channel] * 3, axis=-1)
        else:
            rgb_values = image_array
            alpha_channel = None

    elif len(image_array.shape) == 2:
        # Convert to a triplet
        rgb_values = np.stack([image_array] * 3, axis=-1)
        alpha_channel = None

    return rgb_values, alpha_channel


def get_average_colour(image_array: np.ndarray) -> RGB:

    rgb_values, alpha_channel = split_alpha_channel(image_array)

    avg_color: np.ndarray = np.average(rgb_values, axis=(0, 1),
                                       weights=alpha_channel)
    if avg_color.shape == (3,):
        rgb_colors = [*avg_color]
    else:
        raise ValueError('Average colour got an unexpected dimension')

    return RGB(*(rgb_colors[:3]))


def debug_colors(images_list: list[ImageRGB], grid: IterGrid):

    images_color = (image.color for image in images_list)
    array_color = (np.array([[image_color.as_linear()]])
                   for image_color in images_color)
    color_square = [np.ones((DebugImage.PPP, DebugImage.PPP, 3), dtype=float) * color
                    for color in array_color]

    make_image_from_list(color_square, grid,
                         DebugImage.PPP, DebugImage.PATH, DebugImage.BACKGROUND_COLOR)
