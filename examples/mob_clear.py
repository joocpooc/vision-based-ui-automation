# examples/mob_clear_example.py

from recognize import search_generic
from automation import hold_click_all_instances, respawn, battle, search_words, search_return_to_towne
from config import instances
import time

# Define mob clearing positions
POSITIONS = [
    {"name": "Bottom Left", "x": 17, "y": 446, "duration": 1000},
    {"name": "Top Left", "x": 114, "y": 415, "duration": 2250},
    {"name": "Top Right", "x": 140, "y": 485, "duration": 3300},
    {"name": "Bottom Right", "x": 26, "y": 440, "duration": 2000},
]

CHECK_REGION = (363, 455, 827, 477)  # Region to check for "Zori Kurn"
PLATONIUS_REGION = (363, 455, 827, 477)
RETURN_TO_TOWNE_REGION = (424, 807, 768, 917)


def mob_clear_example():
    print("Starting mob clearing example...")
    total_fail_count = 0

    while True:
        for pos in POSITIONS:
            print(f"Moving to {pos['name']}")

            # Check for platonius or return to towne
            if search_words(["platonius"], *PLATONIUS_REGION, threshold=80):
                print("Platonius spawned, moving on")
                return
            if search_return_to_towne(*RETURN_TO_TOWNE_REGION):
                print("Return to Towne found, stopping mob clear")
                return

            respawn()
            hold_click_all_instances(instances, pos["x"], pos["y"], pos["duration"])
            battle(2)
            respawn()

            # Check Zori Kurn twice in a row
            consecutive = 0
            while consecutive < 2:
                if search_generic(["ZORI", "KURN"], *CHECK_REGION, preprocess=True):
                    consecutive += 1
                    print(f"Found 'Zori Kurn' ({consecutive}/2)")
                else:
                    consecutive = 0
                    print("'Zori Kurn' not found, continuing to next position")
                    break

            if consecutive >= 2:
                print("Found 'Zori Kurn' twice in a row. Stopping mob clearing.")
                return

        total_fail_count += 1
        if total_fail_count >= 30:
            print("Reached max iterations. Stopping mob clearing.")
            return


if __name__ == "__main__":
    mob_clear_example()
