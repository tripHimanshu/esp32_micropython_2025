# micropython script for esp32
# read temperature and humidity using DHT11 or DHT22 sensor

from machine import Pin
import time
import dht
import sys

DHT_SENSOR_PIN = 14
SENSOR_TYPE = dht.DHT22 # dht.DHT11 for DHT11 sensor
READ_INTERVAL_S = 10

LED_PIN = 2
led = Pin(LED_PIN, Pin.OUT)
led.off()

try:
    sensor = SENSOR_TYPE(Pin(DHT_SENSOR_PIN))
    print(f"DHT Sensor ({SENSOR_TYPE.__name__}) initialized on GPIO {DHT_SENSOR_PIN}")
    time.sleep(2)
except Exception as e:
    print("Error initializing DHT Sesnor: {e}")
    # blink LED rapidly to indicate error
    for _ in range (10):
        led.toggle()
        time.sleep_ms(100)
    raise

while True:
    try:
        sensor.measure()
        time.sleep_ms(100)
        temperature = sensor.temperature()
        humidity = sensor.humidity()
        print(f"Temperature: {temperature:.1f}0C | Humidity: {humidity:.1f}%")
        # blink LED to show the success
        led.on()
        time.sleep_ms(50)
        led.off()
    except OSError as e:
        print(f"Error reading from DHT sensor: {e}")
        # Blink LED rapidly to indicate an error reading
        for _ in range(3):
            led.value(not led.value())
            time.sleep_ms(200)
        led.off()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        for _ in range(5):
            led.value(not led.value())
            time.sleep_ms(150)
        led.off()
    # Wait for the next reading interval
    time.sleep(READ_INTERVAL_S)