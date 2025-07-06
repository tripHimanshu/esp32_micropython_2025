# micropython script for esp32
# led blinking without blocking delay (software timer) 

import machine
import time
import sys

LED_PIN = 2
blink_time_ms = 1000 # ms
last_toggle_time = 0

led = machine.Pin(LED_PIN, machine.Pin.OUT)

try:
    while True:
        if time.ticks_diff(time.ticks_ms(), last_toggle_time) >= blink_time_ms:
            last_toggle_time = time.ticks_ms()
            led.toggle()
            print("LED is on" if led.value() else "LED is off")
except KeyboardInterrupt:
    print("Script terminated")
    led.off()
    sys.exit()
    