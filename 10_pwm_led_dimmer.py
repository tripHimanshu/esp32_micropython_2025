# micropython script for esp32
# on-board LED dimming/ fading using PWM

import machine
import time
import sys

LED_PIN = 2

led = machine.Pin(LED_PIN, machine.Pin.OUT)
pwm_led = machine.PWM(led, freq=1000, duty=0)

try:
    while True:
        print("LED brightness is increasing") 
        for duty in range(0,1024,10):
            pwm_led.duty(duty)
            time.sleep_ms(10)
            print(".", end="")
        print("\nLED is at maximum brightness")
        time.sleep(2)
        print("LED brightness is decreasing")
        for duty in range (0,1024,10):
            pwm_led.duty(1023-duty)
            time.sleep_ms(10)
            print(".", end="")
        print("\nLED is at minimum brightness")
        time.sleep(2) 
except KeyboardInterrupt:
    print("Script terminated")
    led.off()
    sys.exit()
    
            