# micropython script for esp32
# blinks the on-board led

import machine
import time
import sys

LED_PIN = 2

led = machine.Pin(LED_PIN, machine.Pin.OUT)

try:
    while True:
        led.toggle()
        print("LED is on" if led.value() else "LED is off")
        time.sleep(1) # 1 second
except KeyboardInterrupt:
    print("Script terminated")
    led.off()
    sys.exit()
    