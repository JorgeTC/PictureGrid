# PictureGrid

PictureGrid is a Python project that arranges a collection of images into a grid, sorting them based on their average color.

## Features

- **Image Sorting**: Arrange images in the grid based on their average color.
- **Configurable Grid**: Easily configure the dimensions of the grid to suit your visual preferences.
- **Debugging Visualization**: Generate a debug image with colored squares to visualize the sorting process.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/JorgeTC/PictureGrid.git
   cd PictureGrid
   ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

Configure the project settings in `settings.py`:
Adjust grid dimensions, source image directory, and output file details.
Specify acceptable image extensions.

Run the main script:

```bash
python merge.py
```

This will sort the images and generate the final grid image.
Will also generate a file with a grid to know the colour that represents each picture in the sorting process.

## Configuration

Adjust the settings in the settings.py file to customize the behavior of the PictureGrid project.

## Dependencies

    numpy
    matplotlib
    Pillow

---

Feel free to contribute, report issues, or suggest improvements!