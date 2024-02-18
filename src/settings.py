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


class OutFile:
    # Directory to store the output file
    DIR: Path = None

    # Name of the output file
    NAME: str = None

    # Full path to the output file
    PATH = DIR / NAME


RGB_LETTERBOX = (20/255, 24/255, 28/255)


class OutImage(OutFile):
    BACKGROUND_COLOR = RGB_LETTERBOX
    DIR = Path("./out").resolve()
    NAME = 'grid.jpg'
    PPP = 300


class DebugImage(OutFile):
    BACKGROUND_COLOR = RGB_LETTERBOX
    DIR = Path("./out").resolve()
    NAME = 'grid_debug.jpg'
    PPP = 300
