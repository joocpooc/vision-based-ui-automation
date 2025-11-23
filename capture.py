# capture.py

import mss
from PIL import Image, ImageEnhance, ImageOps
import numpy as np
from screeninfo import get_monitors
import os
import pytesseract
from fuzzywuzzy import fuzz

# Ensure folder structure exists
for folder in ["screenshots/raw", "screenshots/preprocessed", "screenshots/debug"]:
    os.makedirs(folder, exist_ok=True)

# -------------------- Utility Functions -------------------- #

def save_image(image, filename, folder="debug"):
    """Save image in the correct screenshots folder."""
    folder_path = os.path.join("screenshots", folder)
    os.makedirs(folder_path, exist_ok=True)
    path = os.path.join(folder_path, filename)
    image.save(path)
    return path

def get_monitor(index=2):
    """Return a monitor based on index (default = 2 for second monitor)."""
    monitors = get_monitors()
    if index > len(monitors):
        raise ValueError(f"Monitor {index} not found.")
    return monitors[index - 1]

def capture_region(top_left_x, top_left_y, bottom_right_x, bottom_right_y, monitor_index=2):
    """Capture a region of the screen and return a PIL image."""
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
        save_image(image, "region_capture.png", folder="raw")
        return image

def capture_full_monitor(monitor_index=2):
    """Capture entire monitor."""
    with mss.mss() as sct:
        monitor = sct.monitors[monitor_index]
        screenshot = sct.grab(monitor)
        image = Image.frombytes("RGB", (screenshot.width, screenshot.height), screenshot.rgb)
        save_image(image, "full_capture.png", folder="raw")
        return image

# -------------------- Preprocessing -------------------- #

def preprocess_red_text(image):
    """Preprocess red text on background to improve OCR."""
    image = image.convert("RGB")
    red_rgb = (231, 19, 19)
    arr = np.array(image)
    mask = np.all(arr[:, :, :3] == red_rgb, axis=-1)
    arr[mask] = [0, 0, 0]
    processed = Image.fromarray(arr)
    save_image(processed, "red_text_processed.png", folder="preprocessed")
    return processed

def preprocess_black_text_on_yellow(image):
    """Preprocess black text on yellow background for OCR."""
    grayscale = image.convert("L")
    enhanced = ImageOps.autocontrast(grayscale)
    binary = enhanced.point(lambda x: 0 if x < 128 else 255)
    save_image(binary, "black_on_yellow_processed.png", folder="preprocessed")
    return binary

# -------------------- OCR & Fuzzy Matching -------------------- #

def fuzzy_match(extracted_text, target_texts, threshold=70):
    """Return target string if fuzzy match succeeds."""
    text = extracted_text.strip().upper()
    for target in target_texts:
        if fuzz.partial_ratio(text, target.upper()) >= threshold:
            return target
    return None

def search_text_in_region(top_left_x, top_left_y, bottom_right_x, bottom_right_y, target_texts, preprocess_fn=None, monitor_index=2, threshold=70, filename_prefix="search"):
    """
    Generic search function:
    - Captures region
    - Optionally preprocesses
    - Runs OCR
    - Fuzzy matches against target_texts
    """
    image = capture_region(top_left_x, top_left_y, bottom_right_x, bottom_right_y, monitor_index)
    
    # Preprocess if needed
    if preprocess_fn:
        image = preprocess_fn(image)
    
    # Save debug version
    save_image(image, f"{filename_prefix}_debug.png", folder="debug")
    
    # OCR
    extracted_text = pytesseract.image_to_string(image, config="--psm 6")
    
    # Fuzzy match
    matched = fuzzy_match(extracted_text, target_texts, threshold)
    if matched:
        print(f"Found '{matched}' in region.")
        return True
    else:
        print(f"No target text found in region. OCR output:\n{extracted_text}")
        return False
