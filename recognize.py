# recognize.py

import pytesseract
from PIL import Image
from fuzzywuzzy import fuzz
import mss
from preprocess import preprocess_image_for_black_text_on_yellow


def fuzzy_match(extracted_text: str, target_texts: list[str], threshold: int = 70) -> str | None:
    """
    Fuzzy match OCR text against target strings.
    """
    cleaned_text = extracted_text.strip().upper()
    for target in target_texts:
        if fuzz.partial_ratio(cleaned_text, target.upper()) >= threshold:
            return target
    return None


def search_generic(target_texts: list[str], top_left_x: int, top_left_y: int,
                   bottom_right_x: int, bottom_right_y: int,
                   preprocess: bool = False, psm: int = 6) -> bool:
    """
    Generic OCR search function.

    Args:
        target_texts: List of words to search for.
        top_left_x/y, bottom_right_x/y: Screen coordinates.
        preprocess: Whether to preprocess the image (black text on yellow).
        psm: OCR Page Segmentation Mode.
    """
    with mss.mss() as sct:
        monitor = sct.monitors[2]
        bbox = {
            "left": monitor["left"] + top_left_x,
            "top": monitor["top"] + top_left_y,
            "width": bottom_right_x - top_left_x,
            "height": bottom_right_y - top_left_y
        }

        screenshot = sct.grab(bbox)
        image = Image.frombytes('RGB', (screenshot.width, screenshot.height), screenshot.rgb)

        if preprocess:
            image = preprocess_image_for_black_text_on_yellow(image)

        extracted_text = pytesseract.image_to_string(image, config=f"--psm {psm}")
        matched_text = fuzzy_match(extracted_text, target_texts)
        return matched_text is not None


# Example usage:
# Check for ZORI/KURN
if __name__ == "__main__":
    found = search_generic(["ZORI", "KURN"], 100, 100, 300, 150)
    print("Found ZORI/KURN:", found)
