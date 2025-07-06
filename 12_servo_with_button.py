# micropython script for esp32
# servo motor control using PWM

import machine
import time
import sys

SERVO_PIN = 16
BUTTON_PIN = 0

button = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP) 

# PWM configuration for servo
SERVO_FREQ = 50 # typical operting frequency

# Duty Cycle values for servo angles (approx and may vary per servo)
# 1ms pulse -> 0 degree at 50 Hz = (1ms/20ms)*1023 = 51.15
# 1.5ms pulse -> 90 degree at 50 Hz = (1.5ms/20ms)*1023 = 76.725
# 2ms pulse -> 180 degree at 50 Hz = (2ms/20ms)*1023 = 102.3 
SERVO_MIN_DUTY = 40
SERVO_MID_DUTY = 75
SERVO_MAX_DUTY = 110

SERVO_POSITIONS = [SERVO_MIN_DUTY, SERVO_MID_DUTY, SERVO_MAX_DUTY]
current_position_index = 0

# Button debounce variable
last_button_state = 1
last_button_press_time = 0
DEBOUNCE_TIME = 50

servo = machine.PWM(machine.Pin(SERVO_PIN), freq=SERVO_FREQ, duty=SERVO_POSITIONS[current_position_index])

def set_servo_angle(duty_value):
    servo.duty(duty_value)
    print(f"Setting servo to duty: {duty_value}")
    time.sleep_ms(500)

set_servo_angle(SERVO_POSITIONS[current_position_index])

try:
    while True:
        current_time = time.ticks_ms()
        current_button_state = button.value()
        if current_button_state == 0 and last_button_state == 1:
            if time.ticks_diff(current_time, last_button_press_time) > DEBOUNCE_TIME:
                print("Button pressed")
                current_position_index = (current_position_index + 1) % len(SERVO_POSITIONS)
                new_duty = SERVO_POSITIONS[current_position_index]
                set_servo_angle(new_duty)
                last_button_press_time = current_time
        last_button_state = current_button_state
        time.sleep_ms(10)
except KeyboardInterrupt:
    print("Script terminated")
    sys.exit()
    
    