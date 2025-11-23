# preprocess.py

from PIL import Image, ImageOps
import numpy as np


def preprocess_image_for_red_text(image: Image.Image) -> Image.Image:
    """
    Preprocess a PIL image with red text on background.
    Converts specified red pixels to black for better OCR results.
    """
    image = image.convert("RGB")
    red_rgb = (231, 19, 19)
    image_array = np.array(image)

    # Mask red pixels
    red_pixels = np.all(image_array[:, :, :3] == red_rgb, axis=-1)
    image_array[red_pixels] = [0, 0, 0]  # Convert red pixels to black

    return Image.fromarray(image_array)


def preprocess_image_for_black_text_on_yellow(image: Image.Image) -> Image.Image:
    """
    Preprocess a PIL image with black text on yellow background.
    Converts to grayscale, enhances contrast, and applies binary thresholding.
    """
    grayscale = image.convert("L")
    enhanced = ImageOps.autocontrast(grayscale)
    binary = enhanced.point(lambda x: 0 if x < 128 else 255)  # Thresholding
    return binary
