# micropython script for esp32
# fetch the website content using esp32

import network
import time
import urequests
import gc

# WIFI Credentials
WIFI_SSID = "Your_WIFI_SSID"
WIFI_PASSWORD = "Your_WIFI_Password"
TIMEOUT = 10 # seconds

TARGET_URL = "http://example.com/"

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


def read_website(url):
    print(f"Reading content from {TARGET_URL}")
    try:
        response = urequests.get(url)
        print(f"HTTP Status Code: {response.status_code}")
        if response.status_code == 200:
            print("\nWebsite content (First 500 characters)---")
            content = response.text
            print(content[:500] + "..." if len(content) > 500 else content)
            print("-----------------------------------------")
        else:
            print(f"Failed to fetch content, Server returned status {response.status_code}")
        response.close() # close the response to free up network resources
    except Exception as e:
        print(f"An error occured while fetching content: {e}")
    gc.collect() # trigger garbage collection to free up the memory
    
if __name__ == "__main__":
    try:
        station = connect_to_wifi(WIFI_SSID, WIFI_PASSWORD, TIMEOUT)
        if station:
            read_website(TARGET_URL)
        else:
            print("WIFI Connection failed, cannot access internet")
        print("Press CTRL+C to terminate the script")
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("Script terminated")
        
    
    
        