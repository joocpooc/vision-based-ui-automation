# examples/game_run_example.py

from recognize import search_generic
from automation import hold_click_all_instances, tap_all_instances, battle, respawn
from config import instances
import time

def fight_boss_example(name: str, check_texts: list[str], fail_limit: int = 2):
    """Generic boss fight example for demonstration purposes."""
    fail_count = 0
    print(f"Starting fight: {name}")
    while fail_count < fail_limit:
        battle(1)
        respawn()
        tap_all_instances(instances, 480, 300)  # Example tap
        if search_generic(check_texts, 363, 455, 827, 477, preprocess=True):
            print(f"{name} found!")
            fail_count += 1
        else:
            print(f"{name} not found, retrying...")
            fail_count = 0
            time.sleep(1)

def example_run():
    print("Starting example game run...")
    
    # Step 1: Clear mobs (simplified)
    hold_click_all_instances(instances, 50, 400, 2000)
    battle(2)
    respawn()

    # Step 2: Fight first boss
    fight_boss_example("Zori Kurn", ["ZORI", "KURN"])

    # Step 3: Fight second boss
    fight_boss_example("Auros Kurn", ["AUROS", "KURN"])

    # Step 4: Looting example
    hold_click_all_instances(instances, 40, 410, 1000)
    print("Loot collected!")

if __name__ == "__main__":
    example_run()
