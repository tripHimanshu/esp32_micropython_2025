# micropython_tcp_client.py

import machine
import network
import time
import random
from umqtt.simple import MQTTClient
import sys

# --- Configuration ---
WIFI_SSID = "Your_WIFI_SSID"
WIFI_PASSWORD = "Your_WIFI_Password"  # Replace with your Wi-Fi password
CONNECTION_TIMEOUT_S = 10

LED_PIN = 2
led = machine.Pin(LED_PIN, machine.Pin.OUT)

MQTT_BROKER_IP = 'RaspberryPi IP Address' # Replace with your Raspberry Pi's IP address where Mosquitto is running
MQTT_PORT = 1883 # Default MQTT port
MQTT_TOPIC = b'sensor/data' # MQTT topic to publish to (must be bytes)
DEVICE_ID = 'ESP32_MQTT_Sensor_001' # Unique identifier for this device
PUBLISH_INTERVAL_SECONDS = 10 # How often to publish data

def connect_to_wifi(ssid, password, timeout_s):
    try:
        wlan = network.WLAN(network.STA_IF) # station interface
        wlan.active(False)
        time.sleep(1)
        wlan.active(True) # station interface active
        wlan.disconnect() # remove previous connection
        print(f"Connecting with WIFI {WIFI_SSID}")
        start_time = time.ticks_ms()
        wlan.connect(ssid, password)
        while not wlan.isconnected() and time.ticks_diff(time.ticks_ms(), start_time) < (timeout_s*1000):
            print(".", end="")
            led.toggle()
            time.sleep_ms(100)
        if wlan.isconnected():
            print("Successfully connected with WIFI")
            led.on()
            return wlan
        else:
            print("Failed to connect with WIFI")
            led.off()
            return None
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit()
        

def get_simulated_sensor_data(device_id):
    """
    Generates simulated temperature and humidity data,
    along with the device ID and a timestamp.
    Returns data as a JSON-like string.
    """
    temperature = round(random.uniform(20.0, 30.0), 2)  # Simulate temperature between 20 and 30 Celsius
    humidity = round(random.uniform(40.0, 70.0), 2)     # Simulate humidity between 40 and 70 %
    timestamp = time.time() # Unix timestamp (seconds since epoch)

    # Format the data as a JSON-like string for easier parsing by subscribers
    data_string = (
        f'{{"device_id": "{device_id}", '
        f'"timestamp": {timestamp}, '
        f'"temperature": {temperature}, '
        f'"humidity": {humidity}}}'
    )
    return data_string

def main():
    """Main function to run the MQTT client."""
    station = connect_to_wifi(WIFI_SSID, WIFI_PASSWORD, CONNECTION_TIMEOUT_S)

    client = None # Initialize client to None
    while True:
        try:
            if client is None:
                print(f"Connecting to MQTT broker at {MQTT_BROKER_IP}:{MQTT_PORT}...")
                # Client ID should be unique for each device connecting to the broker
                client = MQTTClient(client_id=DEVICE_ID, server=MQTT_BROKER_IP, port=MQTT_PORT)
                client.connect()
                print("Connected to MQTT broker!")

            # Get simulated sensor data
            sensor_data_payload = get_simulated_sensor_data(DEVICE_ID)
            print(f"Publishing to topic '{MQTT_TOPIC.decode()}': {sensor_data_payload}")

            # Publish the data
            client.publish(MQTT_TOPIC, sensor_data_payload.encode('utf-8'))

            # Wait for the specified interval before publishing again
            time.sleep(PUBLISH_INTERVAL_SECONDS)

        except OSError as e:
            print(f"MQTT connection or network error: {e}")
            print("Attempting to reconnect in 5 seconds...")
            if client:
                client.disconnect() # Disconnect to ensure a clean reconnect
            client = None # Reset client to force re-initialization and reconnect
            # Re-check Wi-Fi connection in case it dropped
            if not sta_if.isconnected():
                connect_wifi(WIFI_SSID, WIFI_PASSWORD)
            time.sleep(5)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            print("Retrying in 5 seconds...")
            if client:
                client.disconnect()
            client = None
            time.sleep(5)

# --- Entry Point ---
if __name__ == '__main__':
    main()