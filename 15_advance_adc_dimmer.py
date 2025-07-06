# micropython script for esp32
# advance adc dimmer (dims the LED using PWM) 

from machine import Pin, ADC, PWM
import time
import sys

ADC_PIN = 34 # Analog input for potentiometer/sensor
LED_PIN = 2  # Onboard LED (for PWM dimming)

# PWM configuration for LED
PWM_FREQ = 1000 # Hz for LED, avoids flicker
PWM_DUTY_MAX = 1023 # Max duty cycle for ESP32 PWM (0-1023 range)

# ADC Configuration
adc = ADC(Pin(ADC_PIN))
# Initialize PWM for the LED
led_pwm = PWM(Pin(LED_PIN), freq=PWM_FREQ, duty=0) # Start LED off

# Attenuation settings to cycle through
# Each tuple: (Attenuation Constant, Max Voltage for that attenuation)
ATTENUATION_SETTINGS = [
    (ADC.ATTN_0DB, 1.1),   # Approx. 0 - 1.1V
    (ADC.ATTN_2_5DB, 1.5), # Approx. 0 - 1.5V
    (ADC.ATTN_6DB, 2.2),   # Approx. 0 - 2.2V
    (ADC.ATTN_11DB, 3.9)   # Approx. 0 - 3.9V (good for 3.3V sensors)
]
current_atten_index = 3 # Start with ATTN_11DB (index 3) for 0-3.3V range

# Set initial attenuation
adc.atten(ATTENUATION_SETTINGS[current_atten_index][0])
adc.width(ADC.WIDTH_12BIT) # Ensure 12-bit resolution

# --- button debounce variables
BUTTON_PIN = 0 # Onboard BOOT button
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)
last_button_state = 1
last_button_press_time = 0
DEBOUNCE_TIME_MS = 200

try:
    while True:
        current_time = time.ticks_ms()
        current_button_state = button.value()
        if current_button_state == 0 and last_button_state == 1:
            if time.ticks_diff(current_time, last_button_press_time) > DEBOUNCE_TIME_MS:
                print("Button pressed") 
                current_atten_index = (current_atten_index + 1) % len(ATTENUATION_SETTINGS)
                new_atten_const, max_voltage = ATTENUATION_SETTINGS[current_atten_index]
                adc.atten(new_atten_const) # Apply the new attenuation
                print(f"Changed Attenuation to: {new_atten_const} (Max Voltage: {max_voltage:.1f}V)")
                print("Adjust potentiometer and observe LED response.")
                last_button_press_time = current_time
        last_button_state = current_button_state
        # Continuous ADC reading and LED dimming
        raw_value = adc.read() # Read the current analog value (0-4095)
        # Get the max voltage for the current attenuation setting
        current_max_voltage = ATTENUATION_SETTINGS[current_atten_index][1]
        # Convert raw value to estimated voltage (for printing/understanding)
        estimated_voltage = (raw_value / 4095.0) * current_max_voltage
        # Map the raw ADC value (0-4095) to the PWM duty cycle range (0-1023)
        # This directly scales the input from 0-4095 to 0-1023 for LED brightness.
        # If using ATTN_0DB, values above ~1.1V will still max out at 4095.
        mapped_duty = int((raw_value / 4095.0) * PWM_DUTY_MAX)
        led_pwm.duty(mapped_duty)
        # Print values periodically to avoid spamming console
        if time.ticks_diff(current_time, last_button_press_time) % 500 < 10: # Print every ~500ms
            print(f"ADC: {raw_value:4d} | Volts: {estimated_voltage:.2f} V | LED Duty: {mapped_duty:4d}")
        time.sleep_ms(10) # Small delay to reduce CPU usage
except KeyboardInterrupt:
    print("Script terminated")
    sys.exit()
        