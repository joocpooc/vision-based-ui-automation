# config.py

# Path to Tesseract OCR
TESSERACT_PATH = r"C:/Program Files/Tesseract-OCR/tesseract.exe"
# Monitor index to capture screenshots from (1 or 2)
MONITOR_INDEX = 2
# BlueStacks instances: IPs, ports, and corresponding window names
INSTANCES = [
    {"ip": "xxx.x.x.x:PORT", "window_title": "BlueStacks App Player"},
    {"ip": "xxx.x.x.x:PORT", "window_title": "BlueStacks App Player 1"},
    {"ip": "xxx.x.x.x:PORT", "window_title": "BlueStacks App Player 2"},
    {"ip": "xxx.x.x.x:PORT", "window_title": "BlueStacks App Player 3"},
    {"ip": "xxx.x.x.x:PORT", "window_title": "BlueStacks App Player 4"}
]
# -----------------------------
# Retry / state counters
# -----------------------------

RETRY_LIMIT = 20

inv_counter = 0
enemy_retry_count = 0
search_retry_count = 0
stacked_retry_count = 0


# -----------------------------
# Timing (optional example)
# -----------------------------

DEFAULT_SLEEP = 0.2


# -----------------------------
# OCR Settings
# -----------------------------

TESSERACT_CONFIG = "--oem 3 --psm 6"
