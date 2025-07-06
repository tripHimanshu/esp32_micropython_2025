# micropython script for esp32
# configuring esp32 as we server (AP mode)
# controlling the on-board led using the web page

import machine
import network
import time
import sys
import gc
import usocket as socket

LED_PIN = 2 
led = machine.Pin(LED_PIN,machine.Pin.OUT)
led.off() # default led state is OFF 

# Configure the ESP32 in access point mode
try:
    SSID = 'ESP_HT'
    PASSWORD = 'mysecretpassword'
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=SSID, password=PASSWORD, authmode=network.AUTH_WPA_WPA2_PSK)
    print("Configuring the ESP32 in Access Point Mode")
    for _ in range (0,11):
        led.toggle()
        time.sleep_ms(500)
    if ap.active():
        print("AP interface is active")
        print(f"IP of ESP32 is {ap.ifconfig()[0]}")
    else:
        print("ESP32 is not configured in AP mode")
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit()



# ***************************************
# web page
# ***************************************
def web_page():
    if isLedBlinking==True:
        led_state = 'Blinking'
        print('led is Blinking')
    else:
        if led.value()==1:
            led_state = 'ON'
            print('led is ON')
        elif led.value()==0:
            led_state = 'OFF'
            print('led is OFF')

    html_page = """    
    <html>    
    <head>    
     <meta content="width=device-width, initial-scale=1" name="viewport"></meta>    
    </head>    
    <body>    
     <center><h2>ESP32 Web Server in MicroPython </h2></center>    
     <center>    
      <form>    
      <button name="LED" type="submit" value="1"> LED ON </button>    
      <button name="LED" type="submit" value="0"> LED OFF </button>  
      <button name="LED" type="submit" value="2"> LED BLINK </button>   
      </form>    
     </center>    
     <center><p>LED is now <strong>""" + led_state + """</strong>.</p></center>    
    </body>    
    </html>"""  
    return html_page   

timer0 = machine.Timer(0)
def handle_callback(timer):
    led.value(not led.value())
isLedBlinking = False

# create server socket at esp32
# if socket is not created, script is terminated
try:
    # create socket (TCP)
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # bind the socket with IP and PORT
    # blank IP specifies that socket is reachable by any addr
    # the machine happens to have
    # web server port is 80
    s.bind(('',80))
    # start listening for clients 
    s.listen(5)
    print('Socket created')
except Exception as e:
    print('Error: ',str(e))
    sys.exit()

# forever loop
try:
    while True:
        # accept client connection 
        conn,addr = s.accept()
        print('client connected from ',addr)
        # recieve data from client machine
        request = conn.recv(1024)
        request = str(request)
        print('request content = ',request)
        # find the request 
        led_on = request.find('/?LED=1')
        led_off = request.find('/?LED=0')
        led_blink = request.find('/?LED=2')
        if led_on == 6:
            # turn on the LED
            print('LED ON')
            led.value(1)
            if isLedBlinking == True:
                timer0.deinit()
                isLedBlinking = False
        elif led_off == 6:
            # turn off the LED
            print('LED OFF')
            led.value(0)
            if isLedBlinking == True:
                timer0.deinit()
                isLedBlinking = False
        elif led_blink == 6:
            # blink the LED
            print('LED is Blinking')
            isLedBlinking = True
            timer0.init(period=500,mode=machine.Timer.PERIODIC,callback=handle_callback)
        # send response back to client machine 
        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        # close the connection
        conn.close()
        gc.collect()
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit()
except KeyboardInterrupt:
    print("Script terminated by user: Keyboard Interrupt")
    sys.exit()
    
