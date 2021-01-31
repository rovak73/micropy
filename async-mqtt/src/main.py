import time
import blynklib
from time import sleep
from machine import Pin


# BLYNK

BLYNK_AUTH = '25tNT5eqiZN-9WcOURHTtmP40CZSyEyX' #insert your Auth Token here
# base lib init
blynk = blynklib.Blynk(BLYNK_AUTH)

# Define constants

#PUB_TIME_SEC = 10





# RELAY

rel_1 = Pin(14, Pin.OUT)
rel_2 = Pin(15, Pin.OUT)


def readRel_1():
    global rel_1_status
    if rel_1.value() == 0:
        rel_1_status = 'off'
    elif rel_1.value() == 1:
        rel_1_status = 'on'
    return rel_1_status

def readRel_2():
    global rel_2_status
    if rel_2.value() == 0:
        rel_2_status = 'off'
    elif rel_2.value() == 1:
        rel_2_status = 'on'
    return rel_2_status



# PUSH BUTTON

# define pin 0 as an input and activate an internal Pull-up resistor:
button = Pin(0, Pin.IN, Pin.PULL_UP)

def readBut():
    return button.value()




# NETWORK

import network

def do_connect():
    WIFI_SSID = 'VTR-3040963'
    WIFI_PASS = '5djkhmJXzzdw'
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(WIFI_SSID, WIFI_PASS)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
    ip = wlan.ifconfig()
    print("Connecting to Blynk server...")
    blynk = blynklib.Blynk(BLYNK_AUTH)
    adc = machine.ADC(0)
    return ip

def netConnect():
    global wlan
    WIFI_SSID = 'VTR-3040963'
    WIFI_PASS = '5djkhmJXzzdw'
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting...')
        wlan.connect(WIFI_SSID, WIFI_PASS)
        while not wlan.isconnected():
            encode_led(' sos ')
            pass
    print('network OK.')
    blinkLed_2(1)
    #uasyncio.run(blink(Pin(16), 1500))
    return wlan



# MQTT

from simple import MQTTClient

server = "mqtt.factoriadigital.cl"
client = MQTTClient("rovak-ESP8266-001", server, user="rovak", password="mosca", port=1883)
topic = b"test"

def sub_cb(topic, msg):
    global state
    print(topic, msg)
    if msg == b"rel_1_on":
        rel_1.value(1)
        state = 1
    elif msg == b"rel_2_on":
        rel_2.value(1)
        state = 1
    elif msg == b"rel_1_off":
        rel_1.value(0)
        state = 0
    elif msg == b"rel_2_off":
        rel_2.value(0)
        state = 0
    elif msg == b"rel_1_toggle":
        rel_1.value(state)
        state = 1 - state
    elif msg == b"rel_2_toggle":
        # LED is inversed, so setting it to current state
        # value will make it toggle
        rel_2.value(state)
        state = 1 - state

def mqttCallback():
    # Subscribed messages will be delivered to this callback
    pass




# LED

import uasyncio

led_1 = machine.Pin(2, machine.Pin.OUT)
led_2 = machine.Pin(16, machine.Pin.OUT)

# create async blink function

async def blink(led, period_ms):
    while True:
        led.off()
        await uasyncio.sleep_ms(25)
        led.on()
        await uasyncio.sleep_ms(200)
        led.off()
        await uasyncio.sleep_ms(25)
        led.on()
        await uasyncio.sleep_ms(period_ms)

async def blinkas(led1, led2):
    uasyncio.create_task(blink(led1, 700))
    uasyncio.create_task(blink(led2, 400))
    await uasyncio.sleep_ms(10_000)






# create a blink function

def blinkLed_1(num):
    for i in range(0, num):
        led_1.off()
        sleep(0.01)
        led_1.on()

def blinkLed_2(num):
    for i in range(0, num):
        led_2.off()
        sleep(0.01)
        led_2.on()

def dot():
   led_2.off()
   time.sleep(0.1)
   led_2.on()
   time.sleep(0.1)

def dash():
   led_2.off()
   time.sleep(0.3)
   led_2.on()
   time.sleep(0.1)

def nextLetter():
   led_2.on()
   time.sleep(0.2)

def space():
   led_2.off()
   time.sleep(0.6)

def encode_led(sentence):
    encodedSentence = morse(sentence)
    for character in encodedSentence:
        if character == '-':
            dash()
        elif character == '.':
            dot()
        elif character == ' ':
            nextLetter()
        else:
            space() 

def morse(txt):
    '''Morse code encryption and decryption'''
    
    d = {'A':'.-','B':'-...','C':'-.-.','D':'-..','E':'.',
         'F':'..-.','G':'--.','H':'....','I':'..','J':'.---',
         'K':'-.-','L':'.-..','M':'--','N':'-.','O':'---',
         'P':'.--.','Q':'--.-','R':'.-.','S':'...','T':'-',
         'U':'..-','V':'...-','W':'.--','X':'-..-','Y':'-.--',
         'Z':'--..', ' ':' '}
    translation = ''
    
    # Encrypt Morsecode
    if txt.startswith('.') or txt.startswith('−'):
        # Swap key/values in d:
        d_encrypt = dict([(v, k) for k, v in d.items()])
        # Morse code is separated by empty space chars
        txt = txt.split(' ')
        for x in txt:
            translation += d_encrypt.get(x)
        
    # Decrypt to Morsecode:
    else:
        txt = txt.upper()
        for x in txt:
            translation += d.get(x) + ' '
    return translation.strip()




# DS18B20

import onewire, ds18x20
# Define the pin to be used with 1-wire bus ==> pin 2 (D4)
dat = Pin(2)
# create the onewire object
ds = ds18x20.DS18X20(onewire.OneWire(dat))
sensors = ds.scan()

def readDs():
    ds.convert_temp()
    time.sleep_ms(250)
    return round(ds.read_temp(sensors[0]), 2)




# COLLECT DATA

def colectData():
    buttonState = readBut()
    extTemp = readDs()
    ip = wlan.ifconfig()[0]
    rel_1_state = readRel_1()
    rel_2_state = readRel_2()
    return extTemp, buttonState, ip, rel_1_state, rel_2_state
    



# I2C / OLED

from machine import I2C
import ssd1306

i2c = I2C(-1, scl=Pin(5), sda=Pin(4))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

def displayData(extTemp, buttonState, ip, rel_1_state, rel_2_state):
    oled.fill(0)
    oled.text("Temp:   " + str(extTemp) + " oC", 0, 4)
    oled.text("Button: " + str(buttonState), 0, 16)
    oled.text("Rel_1:  " + str(rel_1_state), 0, 28)
    oled.text("Rel_2:  " + str(rel_2_state), 0, 40)
    oled.text("IP:" + str(ip), 0, 52)
    oled.show()

# Clear display :

def displayClear():
    oled.fill(0)
    oled.show()



'''------ main function --------'''



def main():
    while button.value():
        start_time = time.time()
        netConnect()
        extTemp, buttonState, ip, rel_1_state, rel_2_state  = colectData()
        displayData(extTemp, buttonState, ip, rel_1_state, rel_2_state)
        payload = str(extTemp)
        client.connect()
        client.publish(topic, payload)
        client.set_callback(sub_cb)
        client.subscribe(topic)
        client.wait_msg()
        client.disconnect()
        print("execTime %s seconds, payload:" % (time.time() - start_time))
    print('loop exited')
    encode_led(' ok ')
    




'''------ run main function --------'''

main()



