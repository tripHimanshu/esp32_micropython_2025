# micropython script for esp32
# publish and subscribe mqtt messages using
# hive mqtt web client

# run the script in thonny
# open the hivemq web client on your web browser using link 
# http://www.hivemq.com/demos/websocket-client/
# the connection details should be pre-filled for the public broker
# click the connect button
# set the publich and subscribe topics 


import time
import network
import ubinascii
from umqtt.simple import MQTTClient
import machine
import sys

LED_PIN = 2
led = machine.Pin(LED_PIN, machine.Pin.OUT)
led.off()

# WiFi Credentials
WIFI_SSID = "Your_WIFI_SSID"
WIFI_PASSWORD = "Your_WIFI_Password"
CONNECTION_TIMEOUT_S = 10

# MQTT Broker Configuration
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
# Create a unique client ID from the ESP32's MAC address
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
print(f"Client ID: {str(CLIENT_ID)}") # for debugging only 

# Topics
TOPIC_PUB = b'esp32/test/publish'    # Topic to publish messages to
TOPIC_SUB = b'esp32/test/subscribe'  # Topic to subscribe to

# --- WiFi Connection ---
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
            print(f"IP Address is: {wlan.ifconfig()[0]}")
            led.on()
        else:
            print("Failed to connect with WIFI")
            led.off()
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit()

# --- MQTT Callback ---
def mqtt_callback(topic, msg):
    """
    Callback function to handle incoming subscribed messages.
    Prints the topic and the message.
    """
    print(f"Received message: Topic='{topic.decode()}', Message='{msg.decode()}'")

# Main Execution
def main():
    """Main function to run the MQTT client."""
    # Connect to WiFi first
    connect_to_wifi(WIFI_SSID, WIFI_PASSWORD, CONNECTION_TIMEOUT_S)

    # Initialize MQTT client
    client = MQTTClient(CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
    client.set_callback(mqtt_callback)

    try:
        # Connect to the MQTT broker
        client.connect()
        print(f"Connected to MQTT Broker: {MQTT_BROKER}")

        # Subscribe to the designated topic
        client.subscribe(TOPIC_SUB)
        print(f"Subscribed to topic: {TOPIC_SUB.decode()}")

        # Main loop to publish and check for messages
        message_count = 0
        while True:
            # Check for any incoming messages
            # check_msg() is non-blocking
            client.check_msg()

            # Publish a message every 5 seconds
            message = f"Hello from ESP32! Count: {message_count}"
            client.publish(TOPIC_PUB, message.encode())
            print(f"Published to {TOPIC_PUB.decode()}: '{message}'")
            message_count += 1
            
            time.sleep(10)

    except OSError as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("Script terminated by user") 
    finally:
        # Ensure the client is disconnected on exit
        if 'client' in locals():
            client.disconnect()
        print("Disconnected from MQTT Broker.")
        sys.exit()

# Run the main function
if __name__ == "__main__":
    main()