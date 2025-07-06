# micropython script for esp32
# selecting one mode on the basis of button press event

import machine
import time
import sys

LED_PIN = 2
BUTTON_PIN = 0

led = machine.Pin(LED_PIN, machine.Pin.OUT)
button = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

# Mode definitions
MODE_OFF = 0
MODE_SOLID_ON = 1
MODE_FAST_BLINK = 2
MODE_SLOW_BLINK = 3
NUM_MODES = 4

# Timing parameters
DEBOUNCE_TIME = 50 # ms
SHORT_PRESS_MAX_MS = 400
LONG_PRESS_MIN_MS = 1000

# Blink interval for different modes
FAST_BLINK_INTERVAL = 100
SLOW_BLINK_INTERVAL = 500

# state variables
current_mode = MODE_OFF
last_button_state = 1 # 1-unpressed, 0-pressed
button_press_start_time = 0
last_blink_toggle_time = 0

# Helper functions for LED modes
def set_mode_off():
    global current_mode
    current_mode = MODE_OFF
    led.value(0)
    print("MODE: OFF")

def set_mode_solid_on():
    global current_mode
    current_mode = MODE_SOLID_ON
    led.value(1)
    print("MODE: SOLID ON")

def handle_fast_blink():
    global current_mode, last_blink_toggle_time
    if current_mode != MODE_FAST_BLINK:
        current_mode = MODE_FAST_BLINK
        print("MODE: FAST BLINK")
        led.value(0)
        last_blink_toggle_time = time.ticks_ms()
    current_time = time.ticks_ms()
    if time.ticks_diff(current_time, last_blink_toggle_time) >= FAST_BLINK_INTERVAL:
        led.value(not led.value())
        last_blink_toggle_time = current_time

def handle_slow_blink():
    global current_mode, last_blink_toggle_time
    if current_mode != MODE_SLOW_BLINK:
        current_mode = MODE_SLOW_BLINK
        print("MODE: SLOW BLINK")
        led.value(0)
        last_blink_toggle_time = time.ticks_ms()
    current_time = time.ticks_ms()
    if time.ticks_diff(current_time, last_blink_toggle_time) >= SLOW_BLINK_INTERVAL:
        led.value(not led.value())
        last_blink_toggle_time = current_time

# Main Application
print("Event Driven Mode Selector")

set_mode_off()

try:
    while True:
        current_time = time.ticks_ms()
        current_button_state = button.value()
        # Button press detection (Falling edge)
        if current_button_state == 0 and last_button_state == 1:
            button_press_start_time = current_time
        elif current_button_state == 1 and last_button_state == 0:
            press_duration = time.ticks_diff(current_time, button_press_start_time)
            
            if press_duration < DEBOUNCE_TIME:
                pass
            elif press_duration > LONG_PRESS_MIN_MS:
                print("EVENT: Long Press Detected")
                set_mode_off()
            elif press_duration < SHORT_PRESS_MAX_MS:
                print("EVENT: Short Press Detected")
                current_mode = (current_mode + 1)%NUM_MODES
                if current_mode == MODE_OFF:
                    set_mode_off()
                elif current_mode == MODE_SOLID_ON:
                    set_mode_solid_on()
            else:
                print("Press duration was ambigious, Ignored")
        last_button_state = current_button_state
        if current_mode == MODE_FAST_BLINK:
            handle_fast_blink()
        elif current_mode == MODE_SLOW_BLINK:
            handle_slow_blink()
        time.sleep_ms(5)
except KeyboardInterrupt:
    print("Script terminated")
    sys.exit()
    
        
                
                