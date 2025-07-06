# micropython script for esp32
# read weather data from open weather map API
# using urequests get method 

import machine
import network
import urequests
import time 
import gc
import sys

LED_PIN = 2

led = machine.Pin(LED_PIN, machine.Pin.OUT)

# WIFI Credentials
WIFI_SSID = "Your_WIFI_SSID"
WIFI_PASSWORD = "Your_WIFI_Password"
CONNECTION_TIMEOUT_S = 10

BASE_URL = 'https://api.openweathermap.org/data/2.5/weather?q='
CITY = 'Ghaziabad'
API_KEY = 'openweather map API key'
URL = BASE_URL+CITY+'&appid='+API_KEY

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
    global last_update, led
    try:
        station = connect_to_wifi(WIFI_SSID, WIFI_PASSWORD, CONNECTION_TIMEOUT_S)
        while True:
            if (time.ticks_ms() - last_update) > (UPDATE_INTERVAL*1000):
                print("Reading weather data from OpenWeatherMap")
                # send request to openweathermap API to get the weather data
                response = urequests.get(URL)
                if response.status_code == 200:
                    # get the data in json format
                    data = response.json()
                    # print(data)
                    # get the main dict block for weather data
                    main = data['main']
                    # get the temperature and subtract it with 273.15
                    # to convert it in degree celcius (default value in Kelvin)
                    temperature = main['temp'] - 273.15
                    # get the humidity in %
                    humidity = main['humidity']
                    # get the pressure in hPA
                    pressure = main['pressure']
                    # get the weather report
                    report = data['weather']
                    # print the data on terminal
                    print("City: {}".format(CITY))
                    print("Temperature: {:.1f} {}C".format(temperature,chr(176)))
                    print("Humidity: {} %".format(humidity))
                    print("Pressure: {} hPA".format(pressure))
                    print("Weather Report: {}".format(report[0]['description']))
                    for _ in range(0,3):
                        led.value(not led.value())
                        time.sleep_ms(200)
                    led.on()
                else:
                    print(f"Error in getting data : {response.status_code}")
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


