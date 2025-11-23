# capture.py

import mss
from PIL import Image
import numpy as np
from screeninfo import get_monitors
import os

for folder in ["screenshots/raw", "screenshots/preprocessed", "screenshots/debug"]:
    os.makedirs(folder, exist_ok=True)


def get_monitor(index=2):
    """Safely return a monitor based on index (default = 2 for second monitor)."""
    with mss.mss() as sct:
        if index >= len(sct.monitors):
            raise ValueError(f"Monitor {index} not found.")
        return sct.monitors[index]


def capture_region(top_left_x, top_left_y, bottom_right_x, bottom_right_y, monitor_index=2):
    """
    Capture a specific region on a selected monitor and return a PIL image.
    """

    with mss.mss() as sct:
        monitor = sct.monitors[monitor_index]

        bbox = {
            "left": monitor["left"] + top_left_x,
            "top": monitor["top"] + top_left_y,
            "width": bottom_right_x - top_left_x,
            "height": bottom_right_y - top_left_y
        }

        screenshot = sct.grab(bbox)
        image = Image.frombytes("RGB", (screenshot.width, screenshot.height), screenshot.rgb)

        return image


def capture_full_monitor(monitor_index=2):
    """Capture the entire monitor as a PIL Image."""
    with mss.mss() as sct:
        monitor = sct.monitors[monitor_index]
        screenshot = sct.grab(monitor)
        return Image.frombytes("RGB", (screenshot.width, screenshot.height), screenshot.rgb)


def save_debug(image, filename):
    """Save an image for debugging purposes."""
    image.save(filename)


def get_monitor_info():
    """Return all connected monitor data."""
    return get_monitors()


def print_monitor_info():
    """Print all connected monitor data."""
    for i, m in enumerate(get_monitors(), start=1):
        print(f"Monitor {i}: {m.width}x{m.height} at ({m.x}, {m.y})")
