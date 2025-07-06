# micropython script for esp32
# led blinking using hardware timer

import machine
import time 
import sys

LED_PIN = 2

led = machine.Pin(LED_PIN, machine.Pin.OUT)

def toggle_led(time):
    led.toggle()
    print("LED is on" if led.value() else "LED is off") 

# timer initialization
timer0 = machine.Timer(0) # use any available hardware timer
timer0.init(period=1000, mode=machine.Timer.PERIODIC, callback=toggle_led)

try:
    while True:
        time.sleep(5)
        print("ESP task is completed") 
except KeyboardInterrupt:
    print("script terminated")
    if led:
        led.off()
    timer0.deinit()
    sys.exit()
    
