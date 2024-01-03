import colorsys
import math
from dataclasses import dataclass
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from iter import IterGrid
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


def get_representative_colour(image_array: np.ndarray, *,
                              criteria=(cv2.TERM_CRITERIA_EPS +
                                        cv2.TERM_CRITERIA_MAX_ITER, 200, .1),
                              flags=cv2.KMEANS_RANDOM_CENTERS):

    pixels = np.float32(image_array.reshape(-1, 3))

    n_colors = 5

    _, labels, palette = cv2.kmeans(pixels, n_colors,
                                    None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)

    dominant = palette[np.argmax(counts)]
    return RGB(*(dominant[0:3]))


def debug_colors(images_list: list[ImageRGB], grid: IterGrid):

    total_width = grid.columns
    total_height = grid.rows
    fig, axes = plt.subplots(grid.rows, grid.columns)
    fig.set_size_inches(total_width, total_height)
    fig.set_facecolor(DebugImage.BACKGROUND_COLOR)

    colors = (image.color for image in images_list)
    for position, image_color in zip(grid.iterate_diagonals(), colors):
        color = np.array([[image_color.as_linear()]])
        image = np.ones((1, 1, 3), dtype=float) * color

        # Get to the next cell
        cell: plt.Axes = axes[position.row, position.column]
        cell.axis('off')
        cell.imshow(image)

    plt.subplots_adjust(left=None, bottom=None, right=None, top=None,
                        wspace=0, hspace=0)
    # Save the plot as a jpg file
    plt.savefig(DebugImage.PATH, pad_inches=0,
                dpi=DebugImage.PPP, bbox_inches='tight')
