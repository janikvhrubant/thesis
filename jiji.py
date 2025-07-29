import pyautogui
import time
import random
from pynput import mouse

# Movement threshold in pixels
JIGGLE_DISTANCE = 3
# Time in seconds between checks
CHECK_INTERVAL = 20

last_position = pyautogui.position()
last_move_time = time.time()

# Track if the user moved the mouse
def on_move(x, y):
    global last_position, last_move_time
    if (x, y) != last_position:
        last_position = (x, y)
        last_move_time = time.time()

# Start mouse listener in background
listener = mouse.Listener(on_move=on_move)
listener.daemon = True
listener.start()

print("Mouse jiggler running. Press Ctrl+C to stop.")
try:
    while True:
        now = time.time()
        if now - last_move_time >= CHECK_INTERVAL:
            x, y = last_position
            dx = random.randint(-JIGGLE_DISTANCE, JIGGLE_DISTANCE)
            dy = random.randint(-JIGGLE_DISTANCE, JIGGLE_DISTANCE)
            pyautogui.moveTo(x + dx, y + dy, duration=0.1)
            last_position = pyautogui.position()
            last_move_time = now
        time.sleep(1)
except KeyboardInterrupt:
    print("\nStopped.")
