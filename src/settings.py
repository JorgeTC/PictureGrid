from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path


class Grid:
    ROWS = 10
    COLUMNS = 10

    DIAGONALS = ROWS + COLUMNS - 1


class SrcImages:
    # Folder to store the input images
    DIR = Path("./res").resolve()

    # Acceptable images extensions
    EXTENSIONS = {'.jpg'}


@dataclass(frozen=True)
class OutFile:
    # Directory to store the output file
    DIR: Path

    # Name of the output file
    NAME: str

    # Pixels per inch
    PPP: int

    # Colour for the space between images
    BACKGROUND_COLOR: tuple[int, int, int]

    def PATH(cls):
        '''Full path to the output file'''
        return cls.DIR / cls.NAME


RGB_LETTERBOX = (20/255, 24/255, 28/255)


OutImage = OutFile(BACKGROUND_COLOR=RGB_LETTERBOX,
                   DIR=Path("./out").resolve(),
                   NAME='grid.jpg',
                   PPP=300)


DebugImage = OutFile(BACKGROUND_COLOR=RGB_LETTERBOX,
                     DIR=Path("./out").resolve(),
                     NAME='grid_debug.jpg',
                     PPP=300)


class RepresentativeColor(Enum):
    AVERAGE = auto()
    MEDIAN = auto()


REPRESENTATIVE_COLOR = RepresentativeColor.AVERAGE
