[![PyPI - Version](https://img.shields.io/pypi/v/battle-map-tv)](https://pypi.org/project/battle-map-tv/)
[![Tests](https://github.com/Conengmo/battle-map-tv/actions/workflows/pytest.yml/badge.svg?branch=main)](https://github.com/Conengmo/battle-map-tv/actions/workflows/pytest.yml)
[![Mypy](https://github.com/Conengmo/battle-map-tv/actions/workflows/mypy.yml/badge.svg)](https://github.com/Conengmo/battle-map-tv/actions/workflows/mypy.yml)
[![Ruff](https://github.com/Conengmo/battle-map-tv/actions/workflows/ruff.yml/badge.svg)](https://github.com/Conengmo/battle-map-tv/actions/workflows/ruff.yml)

# Battle Map TV

Display battle maps for TTRPGs on a tv or monitor that lies flat horizontally on your table.

No more features than needed: just show an image the way you want. Optionally add a grid,
initiative tracker and area of effect shapes.

For GM's with little time or who improvise. Much easier to use during your session than a full blown VTT.

- Works on Linux, macOS and Windows
- Free and open source
- Works offline

![IMG_4856](https://github.com/user-attachments/assets/e34624eb-d7da-4804-b22b-2291513e68a8)

*My GM laptop that also runs controls and a TV showing the map. Add minis, tokens or gummibears yourself.*

## Features

- Application with two windows:
  - one on the TV with your map and grid on it
  - one on your GM laptop with controls
- Import local image files to display on the tv.
- Scale, pan, center and rotate the image.
- Overlay a grid that you can scale to 1 inch.
- Automatically detect the lines in an image and scale it to the grid overlay.
- Save settings so images load like you had them last time.
- Simple initiative tracker
- Overlay area of effects
  - snap to grid
  - rasterize to grid


## Installation

There are two options: use a fully ready executable or use Python.

### Windows executable

If you are on Windows, you can get an executable from the latest release. Look for 'battle-map-tv.exe'
under 'Assets' on https://github.com/Conengmo/battle-map-tv/releases.

### Using Python

- Open terminal or cmd.
- Check that you have Python installed by running the `python --version` command.
  - If you don't have Python, it's easy to install. See here: https://wiki.python.org/moin/BeginnersGuide/Download
- Optionally, use a virtual environment
- Install Battle Map TV with this command: `python -m pip install battle-map-tv`
- Then run it with: `python -m battle_map_tv`


## User guide

- Drag the TV window to your TV and make it fullscreen with the 'fullscreen' button.
- Use the 'add' button to load an image.
- You can drag the image to pan. Zoom with your mouse scroll wheel or use the slider in the controls window.
- Close the application with the 'exit' button.

### Initiative tracker

In the controls window, you can add players and their initiative. The list will be sorted automatically.
Just put a number and a name on each line, for example "1 barbarians" and "20 heroes".

The '+' and '-' buttons increase and decrease the font size.

The 'move' button moves the lists to different positions and rotations on the screen.

### Area of effect

Click on one of the buttons for a shape like 'circle' or 'square'. Then click and drag anywhere in the TV window
to create the shape in the size you want.

The default color for shapes is white, but you can also toggle another color with the color buttons.

You can delete a shape by right-clicking on it, or by using the 'Clear' button.

If the grid is enabled, points will automatically snap to the grid.

If you click 'rasterize', the edges of the shapes you make will fit the grid.

When creating a shape, hold 'shift' to freeze the size of the shape, but keep rotating.


## Technical

- Uses [PySide6](https://wiki.qt.io/Qt_for_Python) for the graphical user interface.
- Uses [OpenCV](https://github.com/opencv/opencv-python) to detect the grid on battle maps.
- Uses [Hatch](https://hatch.pypa.io/latest/) to build and release the package.
- Uses [Nuitka](https://nuitka.net/) to create executables.

### Create executables with Nuitka

Make sure you have a clean virtualenv, otherwise you may get errors.
Use the commands below to install the requirements and call Nuitka to build a single executable.

```
pip install -r requirements.txt
pip install nuitka imageio

python -m nuitka battle_map_tv/__main__.py --enable-plugin=pyside6 --onefile `
--windows-console-mode=attach --windows-icon-from-ico=battle_map_tv/icon.png `
--include-data-files="battle_map_tv/icon.png=battle_map_tv/icon.png" `
--output-filename="battle-map-tv.exe"
```
