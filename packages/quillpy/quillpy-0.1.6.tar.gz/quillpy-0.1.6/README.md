# QuillPy

A lightweight terminal-based text editor for Python

## Installation

```bash
# Install from PyPI
pip install quillpy

# Install with clipboard support (Windows)
pip install quillpy[windows]


```

## Usage

```bash
quillpy filename.txt  # Open existing file
quillpy newfile.txt    # Create new file
```

If that dosen't work, try:

```bash
python -m quillpy filename.txt  # Open existing file
python -m quillpy newfile.txt    # Create new file
```

**Key Bindings:**

- Ctrl+S: Save file
- Ctrl+Q: Quit editor
- Ctrl+C: Copy selection
- Ctrl+V: Paste clipboard
- Arrow keys: Navigation
- Backspace: Delete previous character
- Enter: Insert newline

## Features

- Cross-platform terminal UI
- Basic text editing operations
- Syntax highlighting (Python supported)
- Multiple file support
- Clipboard support (Windows)

## License

[MIT License](LICENSE)

## Development Setup

```bash
python -m pip install -e .
```

Please follow PEP8 guidelines and include tests with any changes.
