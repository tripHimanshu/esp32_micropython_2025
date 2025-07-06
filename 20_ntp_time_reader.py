# micropython script for esp32
# read the time, day and date from NTP 

import network
import time
import ntptime # NTP client
import gc

# WIFI Credentials
WIFI_SSID = "Your_WIFI_SSID"
WIFI_PASSWORD = "Your_WIFI_Password"
TIMEOUT = 10 # seconds

# IST is UTC+5:30
IST_OFFSET_SECONDS = (5 * 3600) + (30 * 60) # 5 hours * 3600 sec/hr + 30 min * 60 sec/min

# Day Names
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

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


def read_ntptime():
    print("Synchronizing time with NTP server")
    try:
        # MicroPython time epoch is 2000-01-01
        # NTP time epoch is 1900-01-01
        # This delta corrects for that
        ntptime.NTP_DELTA = 3155673600
        # specify an NTP host, or it will use a default (often pool.ntp.org)
        ntptime.host = 'pool.ntp.org' # Example: 'time.google.com' or 'ntp.nict.jp'
        ntptime.settime() # Synchronize the RTC (Real Time Clock)
        print("Time synchronized successfully!")

        # Get the current time as a tuple (UTC time by default from ntptime)
        # Tuple format: (year, month, mday, hour, minute, second, weekday, yearday)
        # weekday: 0-Monday, 1-Tuesday, ..., 6-Sunday
        
        # Get UTC time in seconds since epoch (Year 2000)
        utc_seconds = time.time() 
        # Calculate IST seconds
        ist_seconds = utc_seconds + IST_OFFSET_SECONDS
        # Convert IST seconds back to a time tuple
        # Using gmtime() on the adjusted timestamp is safest as localtime() can be tricky
        current_time_tuple_ist = time.gmtime(ist_seconds) 

        year = current_time_tuple_ist[0]
        month = current_time_tuple_ist[1]
        day_of_month = current_time_tuple_ist[2]
        hour = current_time_tuple_ist[3]
        minute = current_time_tuple_ist[4]
        second = current_time_tuple_ist[5]
        weekday_num = current_time_tuple_ist[6] # 0 for Monday, 6 for Sunday

        day_name = WEEKDAYS[weekday_num] # Get readable day name

        print("\n--- Current Time & Date in Delhi (IST) ---")
        print(f"Date: {year}-{month:02d}-{day_of_month:02d}")
        print(f"Time: {hour:02d}:{minute:02d}:{second:02d} IST")
        print(f"Day:  {day_name}")
        print("------------------------------------------")
        gc.collect() # free up the memory
    except Exception as e:
        print(f"Error synchronizing or displaying time: {e}")

    
if __name__ == "__main__":
    try:
        station = connect_to_wifi(WIFI_SSID, WIFI_PASSWORD, TIMEOUT)
        if station:
            while station:
                read_ntptime()
                print("Waiting 10 seconds to read time again")
                time.sleep(10)
        else:
            print("WIFI Connection failed, cannot access internet")
    except KeyboardInterrupt:
        print("Script terminated")
        
    
    
        
