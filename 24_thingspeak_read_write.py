# micropython script for esp32
# read temperature and humidity from dht sensor
# send the sensor values to the thingspeak server using HTTP post method
# read back the thingspeak channel feed using HTTP get method 


import machine
import network
import urequests
import time 
import dht
import gc
import sys
import random

LED_PIN = 2
DHT_SENSOR_PIN = 15

led = machine.Pin(LED_PIN, machine.Pin.OUT)
dht_sensor = dht.DHT11(machine.Pin(DHT_SENSOR_PIN)) # use DHT22 otherwise

# WIFI Credentials
WIFI_SSID = "Your_WIFI_SSID"
WIFI_PASSWORD = "Your_WIFI_Password"
CONNECTION_TIMEOUT_S = 10

WRITE_API_KEY = 'Thingspeak write API key'
CHANNEL_ID = '2995486'
READ_API_KEY = 'Thingspeak read API Key'
UPDATE_INTERVAL = 10 # seconds
last_update = 0

def exit():
    global led
    if led:
        led.off()
    sys.exit()

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
        exit()

 
def main():
    global last_update, UPDATE_INTERVAL, led
    station = connect_to_wifi(WIFI_SSID, WIFI_PASSWORD, CONNECTION_TIMEOUT_S)
    if station is None:
        exit()
    try:
        while True:
            if (time.ticks_ms() - last_update) > (UPDATE_INTERVAL*1000):
                print("Reading sensor data") 
                # read sensor data
                # dht_sensor.measure()
                # temperature = dht_sensor.temperature()
                # humidity = dht_sensor.humidity()
                # for testing purpose using random values for temperature and humidity
                temperature = random.uniform(10.0, 45.0)
                humidity = random.uniform(30.0, 70.0)
                # convert sensor data into jsom object
                sensor_data = {'field1': temperature, 'field2': humidity}
                print(sensor_data)
                print("Sending sensor data to Thingspeak")
                request = urequests.post('https://api.thingspeak.com/update?api_key=' + WRITE_API_KEY, json=sensor_data)
                if request.status_code == 200:
                    for _ in range(0,3):
                        led.value(not led.value())
                        time.sleep_ms(500)
                    print("Data sent successfully")
                    led.on()
                else:
                    print(f"Error in data sending: {request.status_code}")
                request.close()
                
                # Read data from Thingspeak
                # This will read only the last feed
                # for more feeds change the number with '&results=1'
                response = urequests.get('https://api.thingspeak.com/channels/'
                                         + CHANNEL_ID
                                         + '/feeds.json?api_key='
                                         + READ_API_KEY
                                         +'&results=1'
                                         )
                if response.status_code == 200:
                    # get the data in json format
                    data = response.json()
                    print(f"Recieved Data: {data}")
                gc.collect()
                last_update = time.ticks_ms()
    except Exception as e:
        print(f"ERROR: {e}")
        exit()
    except KeyboardInterrupt:
        print("Script terminated by the user: KeyboardInterrupt")
        exit()
        
            
if __name__ == "__main__":
    main()

