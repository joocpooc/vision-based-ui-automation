# config.py

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
