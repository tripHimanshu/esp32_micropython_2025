# micropython script for esp32
# reading the ADC value

import machine
import time
import sys

ADC_PIN = 34
BUTTON_PIN = 0
LED_PIN = 2

led = machine.Pin(LED_PIN, machine.Pin.OUT) 

adc_pin = machine.ADC(machine.Pin(ADC_PIN))

# Set the ADC attenuation. ATTN_11DB covers the 0V to ~3.9V range,
# which is good for sensors powered by 3.3V.
adc_pin.atten(machine.ADC.ATTN_11DB)

# Set the ADC resolution (default is 12 bits, 0-4095)
# This is usually not necessary to set explicitly if 12-bit is default,
# but included for clarity.
adc_pin.width(machine.ADC.WIDTH_12BIT)

last_button_state = 1
last_button_press_time = 0
DEBOUNCE_TIME = 50

button = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

try:
    while True:
        # detect the button press and read the adc value with each button press
        current_time = time.ticks_ms()
        current_button_state = button.value()
        if current_button_state == 0 and last_button_state == 1:
            if time.ticks_diff(current_time, last_button_press_time) > DEBOUNCE_TIME:
                print("Button pressed")
                raw_value = adc_pin.read()
                # convert raw value to voltage
                # This is an approximate conversion. Actual Vref can vary slightly.
                # For ATTN_11DB, max voltage is approx 3.9V.
                # So, 4095 corresponds to ~3.9V.
                # Voltage = (Raw_Value / Max_Raw_Value) * Max_Voltage_Range
                voltage = (raw_value / 4095.0) * 3.9 # Using 3.9V as max for ATTN_11DB
                print(f"Raw ADC Value: {raw_value:4d} | Estimated Voltage: {voltage:.2f} V")
                # Simple LED feedback: turn LED on briefly
                led.on()
                time.sleep_ms(100)
                led.off()
                last_button_press_time = current_time # Update time of last valid press
        last_button_state = current_button_state # Update last state for next iteration
        time.sleep_ms(10)
except KeyboardInterrupt:
    print("Script terminated")
    sys.exit()
    