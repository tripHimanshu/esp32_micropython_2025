# micropython script for esp32
# read the public IP of ESP32 using urequests.get() 

import network
import time
import urequests
import json 
import gc

# WIFI Credentials
WIFI_SSID = "Your_WIFI_SSID"
WIFI_PASSWORD = "Your_WIFI_Password"
TIMEOUT = 10 # seconds

IP_API_URL = "http://httpbin.org/ip"

# LED for status
try:
    import machine
    LED_PIN = 2
    led = machine.Pin(LED_PIN, machine.Pin.OUT)
except ImportError:
    print("WARNING: 'machine' module not found, LED status wont be shown")
    led = None
    
def connect_to_wifi(ssid, psk, timeout_s):
    wlan = network.WLAN(network.STA_IF) # create staiton interface 
    wlan.active(True) # active station interface
    wlan.disconnect() # Ensure previous connection is cleared
    print(f"Connecting with the WIFI network {ssid}...")
    wlan.connect(ssid, psk) # connect with WIFI
    start_time = time.ticks_ms()
    while not wlan.isconnected() and time.ticks_diff(time.ticks_ms(), start_time) < (TIMEOUT * 1000):
        if led:
            led.toggle()
        time.sleep_ms(200)
    if wlan.isconnected():
        print("Connection established")
        if led:
            led.on()
        return wlan
    else:
        print("Failed to connect with WIFI")
        if led:
            led.off()
        return None


def get_public_ip(url):
    print(f"Querying the {url} for public IP")
    public_ip = "unknown"
    try:
        response = urequests.get(url)
        print(f"HTTP Status Code: {response.status_code}")
        if response.status_code == 200:
            # Parse the JSON response
            # Example JSON: {"origin": "123.45.67.89"}
            data = response.json() 
            public_ip = data.get('origin', 'Not Found') # Safely get the 'origin' key
            print(f"Your Public IP Address: {public_ip}")
        else:
            print(f"Failed to get IP. Server returned status: {response.status_code}")
        response.close() # Close the response to free up network resources
    except Exception as e:
        print(f"An error occurred while fetching public IP: {e}")
    gc.collect() # Trigger garbage collection
    return public_ip

    
if __name__ == "__main__":
    try:
        station = connect_to_wifi(WIFI_SSID, WIFI_PASSWORD, TIMEOUT)
        if station:
            my_public_ip = get_public_ip(IP_API_URL)
        if my_public_ip != "Unknown":
            print(f"\nMy ESP32's detected public IP is: {my_public_ip}")
        else:
            print("Wi-Fi connection failed. Cannot get public IP.")
        print("\nScript finished. Press Ctrl+C to exit.")
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("Script terminated")
        
    
    
        

