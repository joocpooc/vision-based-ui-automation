from recognize import search_generic

if __name__ == "__main__":
    found = search_generic(
        target_texts=["ZORI", "KURN"],
        top_left_x=1528,
        top_left_y=732,
        bottom_right_x=1634,
        bottom_right_y=747,
        preprocess=True
    )
    print("Found ZORI/KURN:", found)
