# micropython script for esp32
# toggle led with button press using hardware interrupt

import machine
import time
import sys

LED_PIN = 2
BUTTON_PIN = 0

led = machine.Pin(LED_PIN, machine.Pin.OUT)
button = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

button_press_flag = False
last_interrupt_time = 0
debounce_time = 50 # ms

# Interrupt Service Routine
def button_handler(pin):
    global button_press_flag, last_interrupt_time
    current_time = time.ticks_ms()
    if time.ticks_diff(current_time, last_interrupt_time) > debounce_time:
        button_press_flag = True
        last_interrupt_time = current_time

button.irq(trigger=machine.Pin.IRQ_FALLING, handler=button_handler)

try:
    while True:
        if button_press_flag:
            button_press_flag = False
            led.toggle()
            print("LED is on" if led.value() else "LED is off")
            time.sleep_ms(10)
except KeyboardInterrupt:
    print("Script terminated")
    sys.exit()
    