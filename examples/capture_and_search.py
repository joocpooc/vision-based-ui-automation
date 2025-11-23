from capture import capture_full_monitor, save_debug
from recognize import search_generic

if __name__ == "__main__":
    image = capture_full_monitor()
    save_debug(image, "screenshots/debug/full_monitor.png")

    # Search a region in that screenshot
    found = search_generic(
        target_texts=["ZORI", "KURN"],
        top_left_x=1528,
        top_left_y=732,
        bottom_right_x=1634,
        bottom_right_y=747,
        preprocess=True
    )
    print("Found ZORI/KURN in full monitor capture:", found)
