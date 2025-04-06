# Nerd Dictation GUI

A simple graphical user interface for [nerd-dictation](https://github.com/ideasman42/nerd-dictation), a speech-to-text tool for Linux.

## Features

- System tray integration
- Start/stop dictation with a single click
- Status monitoring
- Minimal and lightweight interface

## Installation

### Prerequisites

- Python 3.6 or higher
- PyQt6
- nerd-dictation must be installed and available in your PATH

### Install from PyPI (recommended)

```bash
pip install nerd-dictation-gui
```

### Install from source

```bash
git clone https://github.com/yourusername/nerd-dictation-gui.git
cd nerd-dictation-gui
pip install -e .
```

## Usage

After installation, you can run the application in two ways:

```bash
# As a module
python -m nerd_dictation_gui

# Or using the entry point
nerd-dictation-gui
```

The application will start minimized in your system tray with an icon. Left-click the icon to toggle dictation on/off, or right-click for more options.

## Creating Executable

You can create a standalone executable using PyInstaller:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name nerd-dictation-gui --add-data "src/nerd_dictation_gui/resources/*:nerd_dictation_gui/resources" src/nerd_dictation_gui/main.py
```

The executable will be created in the `dist` directory.

## License

[MIT](LICENSE)
