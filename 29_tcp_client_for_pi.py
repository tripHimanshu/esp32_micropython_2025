# micropython_tcp_client.py

import socket
import time
import machine
import network
import random
import sys

# --- Configuration ---
WIFI_SSID = "Your_WIFI_SSID"
WIFI_PASSWORD = "Your_WIFI_Password"  # Replace with your Wi-Fi password
CONNECTION_TIMEOUT_S = 10

LED_PIN = 2
led = machine.Pin(LED_PIN, machine.Pin.OUT)

SERVER_IP = 'RaspberryPi IP Address'  # Replace with your Raspberry Pi's IP address
SERVER_PORT = 54321  # Must match the port your TCP server is listening on

DEVICE_ID = 'ESP32_Sensor_002' # Unique identifier for this device

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
    """
    temperature = round(random.uniform(20.0, 45.0), 2)  # Simulate temperature between 20 and 30 Celsius
    humidity = round(random.uniform(40.0, 70.0), 2)     # Simulate humidity between 40 and 70 %
    timestamp = time.time() # Unix timestamp (seconds since epoch)

    # Format the data as a string suitable for sending
    # Using a comma-separated format for easy parsing on the server side
    data_string = f"{device_id},{timestamp},{temperature},{humidity}\n"
    return data_string

# --- Main Application Logic ---
def main():
    """Main function to run the TCP client."""
    station = connect_to_wifi(WIFI_SSID, WIFI_PASSWORD, CONNECTION_TIMEOUT_S)

    while True:
        try:
            # Create a TCP/IP socket
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Set a timeout for connection and sending/receiving data
            client_socket.settimeout(10)

            print(f"Attempting to connect to server at {SERVER_IP}:{SERVER_PORT}...")
            client_socket.connect((SERVER_IP, SERVER_PORT))
            print("Connected to server!")

            while True:
                # Get simulated sensor data
                sensor_data = get_simulated_sensor_data(DEVICE_ID)
                print(f"Sending data: {sensor_data.strip()}")

                # Send the data to the server
                client_socket.sendall(sensor_data.encode('utf-8'))

                # Wait for 10 seconds before sending the next data point
                time.sleep(10)

        except OSError as e:
            print(f"Connection error: {e}")
            print("Retrying connection in 5 seconds...")
            # Close the socket in case of an error to free up resources
            if 'client_socket' in locals() and client_socket:
                client_socket.close()
            time.sleep(5)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            print("Restarting connection attempt in 5 seconds...")
            if 'client_socket' in locals() and client_socket:
                client_socket.close()
            time.sleep(5)
        finally:
            # Ensure the socket is closed when exiting the inner loop or on error
            if 'client_socket' in locals() and client_socket:
                client_socket.close()
                print("Socket closed.")

# --- Entry Point ---
if __name__ == '__main__':
    main()
