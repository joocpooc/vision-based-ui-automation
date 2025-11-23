# actions.py

import subprocess
import threading
import time
from config import instances  # if you move your instances list to config.py


def connect_bluestacks_devices():
    for instance in instances:
        ip = instance["ip"]
        try:
            subprocess.run(f"adb connect {ip}", shell=True, check=True)
            print(f"Connected to {ip}")
        except subprocess.CalledProcessError:
            print(f"Failed to connect to {ip}")


def check_adb_devices():
    subprocess.run("adb devices", shell=True)


def wait_for_user_confirmation():
    input("Press Enter to start the script after verifying connections...")


def tap_on_instance(instance_ip, x, y):
    subprocess.run(f"adb -s {instance_ip} shell input tap {x} {y}", shell=True)


def send_text(instance_ip, text):
    subprocess.run(f"adb -s {instance_ip} shell input text {text}", shell=True)


def send_keystroke(instance_ip, key_code):
    subprocess.run(f"adb -s {instance_ip} shell input keyevent {key_code}", shell=True)


def hold_left_click(instance_ip, x, y, duration=3000):
    subprocess.run(f"adb -s {instance_ip} shell input swipe {x} {y} {x} {y} {duration}", shell=True)


def hold_click_all_instances(instances, x, y, duration=3000):
    threads = [threading.Thread(target=hold_left_click, args=(i["ip"], x, y, duration)) for i in instances]
    for t in threads: t.start()
    for t in threads: t.join()


def tap_all_instances(instances, x, y):
    def tap(instance_ip):
        subprocess.run(f"adb -s {instance_ip} shell input tap {x} {y}", shell=True)
    threads = [threading.Thread(target=tap, args=(i["ip"],)) for i in instances]
    for t in threads: t.start()
    for t in threads: t.join()

#example function for game automation:
def host_game():
    # Example: Tap on coordinates (600, 25) for instance 1 (127.0.0.1:5555)
    tap_on_instance(instances[0]["ip"], 580, 45)

    # Wait for 3 seconds before the next tap
    time.sleep(2)

    tap_on_instance(instances[0]["ip"], 243, 497)
    time.sleep(1)
    tap_on_instance(instances[0]["ip"], 333, 110)
    tap_on_instance(instances[0]["ip"], 830, 310)
    tap_on_instance(instances[0]["ip"], 108, 484)
    send_text(instances[0]["ip"], "aqw")
    send_keystroke(instances[0]["ip"], 66)
    time.sleep(1)
    tap_on_instance(instances[0]["ip"], 448, 487)
