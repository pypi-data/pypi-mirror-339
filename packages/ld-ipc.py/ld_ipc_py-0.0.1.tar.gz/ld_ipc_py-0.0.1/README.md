<div align="center">

# ld-ipc.py

Python SDK for LDPlayer IPC.

[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/EvATive7/ld-ipc.py/package.yml)](https://github.com/EvATive7/ld-ipc.py/actions)
[![Python](https://img.shields.io/pypi/pyversions/ld-ipc.py)](https://pypi.org/project/ld-ipc.py)
[![PyPI version](https://badge.fury.io/py/ld-ipc.py.svg)](https://pypi.org/project/ld-ipc.py)
[![Coverage Status](https://coveralls.io/repos/EvATive7/ld-ipc.py/badge.svg?branch=develop&service=github)](https://coveralls.io/github/EvATive7/ld-ipc.py?branch=master)
[![License](https://img.shields.io/github/license/EvATive7/ld-ipc.py.svg)](https://pypi.org/project/ld-ipc.py/)

</div>

## Usage

Install the package using pip: `pip install ld-ipc.py`  

```python
from pathlib import Path

from PIL import Image
from ldipc import LDPlayer

# Set the path and index of LDPlayer
ldplayer_path = Path(r"C:\leidian\LDPlayer9")  # Replace with your LDPlayer path
player_index = 0  # Replace with the index of players you want to capture

try:
    # Create an LDPlayer instance
    ld_player = LDPlayer(ldplayer_path, player_index)

    # capture screenshots
    screenshot_array = ld_player.capture()

    # Convert numpy array to PIL image and save
    screenshot_image = Image.fromarray(screenshot_array)
    screenshot_image.save("screenshot.png")

    print("Screenshot has been saved as screenshot.png")
except Exception as e:
    print(f"Error capturing screenshot: {e}")

```

## Platform

Only Windows is supported.
