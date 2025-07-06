# micropython script for esp32
# pwm led dimmer with button input

import machine
import time
import sys

LED_PIN = 2
BUTTON_PIN = 0
PWM_FREQ = 1000 # Hz
PWM_DUTY_MAX = 1023

# Brightness levels
BRIGHTNESS_LEVELS = [
    0,                        # 0% (Off)
    int(PWM_DUTY_MAX * 0.05), # 5%
    int(PWM_DUTY_MAX * 0.15), # 15%
    int(PWM_DUTY_MAX * 0.30), # 30%
    int(PWM_DUTY_MAX * 0.50), # 50%
    int(PWM_DUTY_MAX * 0.75), # 75%
    PWM_DUTY_MAX              # 100% (Full Brightness) 
]

current_brightness_index = 0

# BUtton debounce variables
last_button_state = 1
last_button_press_time = 0
DEBOUNCE_TIME = 200


led = machine.Pin(LED_PIN)
pwm_led = machine.PWM(led, freq=PWM_FREQ, duty= BRIGHTNESS_LEVELS[current_brightness_index])
button = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

try:
    while True:
        current_time = time.ticks_ms()
        current_button_state = button.value()
        # detect button press (falling edge with debounce)
        if current_button_state == 0 and last_button_state == 1:
            if time.ticks_diff(current_time, last_button_press_time) > DEBOUNCE_TIME:
                print("Button pressed")
                current_brightness_index = (current_brightness_index + 1) % len(BRIGHTNESS_LEVELS)
                duty_cycle = BRIGHTNESS_LEVELS[current_brightness_index]
                pwm_led.duty(duty_cycle)
                percentage = (duty_cycle/PWM_DUTY_MAX)*100
                print(f"Brightness Level -> {current_brightness_index},  Duty -> {duty_cycle} ({percentage:.1f}%)")
                last_button_press_time = current_time
        last_button_state = current_button_state
        jhi
        time.sleep_ms(10)
        
except KeyboardInterrupt:
    print("Script terminated")
    led.off()
    sys.exit()
    