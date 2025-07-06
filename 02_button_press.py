# micropython script for esp32
# detect the button press and print "button pressed"

import machine
import time
import sys

BUTTON_PIN = 0 # on-board boot button

button = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

try:
    while True:
        if button.value() == 0:
            print("Button pressed")
            while button.value() == 0:
                time.sleep_ms(1)
except KeyboardInterrupt:
    print("Script terminated")
    sys.exit()
    
    
            