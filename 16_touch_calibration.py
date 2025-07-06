# micropython script for esp32
# calibrating touch threshold

import machine
import time
import sys

TOUCH_PIN = 27

touch_pad = machine.TouchPad(TOUCH_PIN)

try:
    while True:
        touch_value = touch_pad.read()
        print(f"Raw Touch Value = {touch_value}")
        time.sleep_ms(500)
except KeyboardInterrupt:
    print("Script terminated")
    sys.exit()
    