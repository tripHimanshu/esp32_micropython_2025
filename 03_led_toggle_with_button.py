# micropython script for esp32
# toggle led with each button press

import machine
import time
import sys

LED_PIN = 2
BUTTON_PIN = 0

led = machine.Pin(LED_PIN, machine.Pin.OUT)
button = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

try:
    while True:
        if button.value() == 0:
            led.toggle()
            print("LED is on" if led.value() else "LED is off")
            while button.value() == 0:
                time.sleep_ms(1)
except KeyboardInterrupt:
    print("Script terminated")
    led.off()
    sys.exit()
    