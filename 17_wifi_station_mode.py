#  micropython script for esp32
# configure the wifi station mode and connect with wifi network

import network
import machine
import ubinascii
import time
import sys

WIFI_SSID = "Your_WIFI_SSID"
WIFI_PASSWORD = "Your_WIFI_Password"

LED_PIN = 2
led = machine.Pin(LED_PIN, machine.Pin.OUT)

def connect_to_wifi(ssid, psk):
    wlan = network.WLAN(network.STA_IF) # station interface
    wlan.active(True) # interface activated
    if not wlan.isconnected():
        print(f"Connecting to wifi network {ssid}...")
        wlan.connect(ssid, psk)
        timeout = 10 # seconds
        start_time = time.ticks_ms()
        while not wlan.isconnected() and time.ticks_diff(time.ticks_ms(), start_time) < (timeout * 1000):
            led.toggle()
            time.sleep_ms(200)
    if wlan.isconnected():
        print("Connection established")
        led.on()
        return wlan
    else:
        print("Failed to connect within timeout")
        led.off()
        return None

def display_network_details(wlan_obj):
    if wlan_obj and wlan_obj.isconnected():
        print("\n--- Network Details ---")
        ip, subnet, gateway, dns = wlan_obj.ifconfig()
        print(f"IP Address:    {ip}")
        print(f"Subnet Mask:   {subnet}")
        print(f"Gateway:       {gateway}")
        print(f"DNS Server:    {dns}")
        # get MAC address  in human readable format
        mac = ubinascii.hexlify(wlan_obj.config('mac'),':').decode().upper()
        print(f"MAC Address:   {mac}")
        # get RSSI (Received Signal Strength Indicator)
        rssi = wlan_obj.status('rssi')
        print(f"RSSI (signal): {rssi} dBm")
        # Get the current connection status code
        status_code = wlan_obj.status()
        print(f"Status Code:   {status_code}")
        print("\n")
    else:
        print("Not connected to wifi, can nto display details")

if __name__ == "__main__":
    try:
        wlan_station = connect_to_wifi(WIFI_SSID, WIFI_PASSWORD)
        if wlan_station:
            display_network_details(wlan_station)
        print("Script finished, WIFI connection maintained, press CTRL+C to exit")
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("Script terminated")
        wlan_station.disconnect()
        wlan_station.active(False)
        sys.exit()
    