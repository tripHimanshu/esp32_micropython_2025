# micropython script for esp32
# button press duration detect

import machine
import time
import sys

LED_PIN = 2
BUTTON_PIN = 0

led = machine.Pin(LED_PIN, machine.Pin.OUT)
button = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

# threshold for short and long presses
short_press_max_ms = 300
long_press_min_ms = 800

last_button_state = 1
press_start_time = 0

def indicate_short_press():
    print("Detected short press")
    led.on()
    time.sleep_ms(50)
    led.off()
    time.sleep_ms(50)
    led.on()
    time.sleep_ms(50)
    led.off()
    time.sleep_ms(200)

def indicate_long_press():
    print("Detected long press")
    led.on()
    time.sleep_ms(500)
    led.off()
    time.sleep_ms(500)
    
try:
    while True:
        current_button_state = button.value()
        # detect button press (Falling Edge) 
        if current_button_state == 0 and last_button_state == 1:
            press_start_time = time.ticks_ms()
        # detect button release (Rising edge)
        elif current_button_state == 1 and last_button_state == 0:
            press_duration = time.ticks_diff(time.ticks_ms(), press_start_time)
            if press_duration <= short_press_max_ms:
                indicate_short_press()
            elif press_duration >= long_press_min_ms:
                indicate_long_press()
            else:
                print("Press duration was neither short nor long")
            time.sleep_ms(10)
        last_button_state = current_button_state
        time.sleep_ms(10)
except KeyboardInterrupt:
    print("Script terminated")
    sys.exit()
    
            