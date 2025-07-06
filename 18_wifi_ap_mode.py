# micropython script for esp32
# configure the esp32 wifi in access point mode 

import network
import machine
import time

AP_SSID = "ESP32AP_1" # Name of WIFI network the esp32 will create
AP_PASSWORD = "mysecretpassword" # Must be 8 characters
AP_CHANNEL = 1 # WIFI channel (1-13)
AP_IP = '192.168.4.1' # IP address for esp32 

LED_PIN = 2
led = machine.Pin(LED_PIN, machine.Pin.OUT)
led.off()

ap = None # Initialize ap outside try/except for KeyboardInterrupt access

try:
    ap = network.WLAN(network.AP_IF)
    # Configure the AP
    ap.config(essid=AP_SSID, password=AP_PASSWORD, channel=AP_CHANNEL) 
    ap.ifconfig((AP_IP, '255.255.255.0', AP_IP, '8.8.8.8')) # (IP, Subnet, Gateway, DNS)
    ap.active(True) # Activate the AP interface
    print(f"Configuring AP: {AP_SSID} with IP: {AP_IP}")
    # Wait for AP to become active and indicate status with LED
    while not ap.active():
        print("Waiting for AP to become active...")
        led.toggle()
        time.sleep_ms(200)
    print("AP is Active!")
    print(f"Connect to WiFi network: '{AP_SSID}'")
    print(f"IP Address: {ap.ifconfig()[0]}") # Print the actual assigned IP
    led.value(1) # LED solid ON to indicate AP is active
    # Keep the script running to maintain the AP
    while True:
        time.sleep(10) # Sleep to reduce CPU usage
except KeyboardInterrupt:
    print("\nScript terminated by KeyboardInterrupt")
    if ap is not None and ap.active(): # Ensure ap exists and is active before deactivating
        ap.active(False)
        print("AP deactivated.")
    led.off() # Ensure LED is off on termination
