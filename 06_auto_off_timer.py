# micropython script for esp32
# button triggered auto off timer (hardware timer for timeout)

import machine
import time
import sys

LED_PIN = 2
BUTTON_PIN = 0

led = machine.Pin(LED_PIN, machine.Pin.OUT)
button = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

auto_off_timeout = 5000
auto_off_timer = machine.Timer(0)

def turn_off_led(time):
    led.off()
    print("auto_off_timer expired, led is off") 

last_button_state = 1

try:
    while True:
        current_button_state = button.value()
        if current_button_state == 0 and last_button_state == 1:
            print("Button pressed")
            led.on()
            try:
                auto_off_timer.deinit()
            except Exception as e:
                pass
            auto_off_timer.init(period=auto_off_timeout, mode=machine.Timer.ONE_SHOT, callback=turn_off_led)
            print("auto_off_timer started")
            time.sleep_ms(200)
        last_button_state = current_button_state
        time.sleep_ms(10)
except KeyboardInterrupt:
    print("Script terminated")
    auto_off_timer.deinit()
    sys.exit()
    