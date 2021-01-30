# Complete project details at https://RandomNerdTutorials.com/micropython-ssd1306-oled-scroll-shapes-esp32-esp8266/

from machine import Pin, I2C
import ssd1306, time, machine, socket, ds18x20, onewire
from time import sleep
from mqtt import MQTTClient
import config

i2c = I2C(-1, scl=Pin(5), sda=Pin(4))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
led = machine.Pin(2, machine.Pin.OUT)
relay = Pin(14, Pin.OUT)
ds_pin = machine.Pin(2)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
p0 = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)


# Default MQTT server to connect to
SERVER = "mqtt.factoriadigital.cl"
CLIENT_ID = "NodeMCU_01"
TOPIC = b"test"


    



def toggle(p):
    p.value(not p.value())

def callback(p):
    if p.value() == 0:
        print("light on")


def read_ds_sensor():
    roms = ds_sensor.scan()
    #print('Found DS devices: ', roms)
    ds_sensor.convert_temp()
    for rom in roms:
        temp = ds_sensor.read_temp(rom)
        if isinstance(temp, float):
            temp = round(temp, 2)
            print('TEMP:', temp,"°C")
            return temp
    return '0'

def sub_cb(topic, msg):
    global state
    print("LED: ", msg)
    temp = read_ds_sensor()
    if msg == b"on":
        relay.value(1)
        state = 1
    elif msg == b"off":
        relay.value(0)
        state = 0
    elif msg == b"toggle":
        # LED is inversed, so setting it to current state
        # value will make it toggle
        relay.value(state)
        state = 1 - state

def main(server=SERVER):
    c = MQTTClient(CLIENT_ID, server, user="rovak", password="mosca", port=1883)
    # Subscribed messages will be delivered to this callback
    c.set_callback(sub_cb)
    c.connect()
    c.subscribe(TOPIC)
    print("Connected to %s, subscribed to %s topic" % (server, TOPIC))

    try:
        while 1:
            c.wait_msg()
            oled.fill(0)
            oled.text('Waiting msg.', 10, 10)
            oled.text('string', 10, 32)
            oled.show()

    finally:
        c.disconnect()
 


# ----- General Functions -----

def do_connect():
    relay.value(0)
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        led.on()
        print('connecting to network...')
        oled.fill(0)
        oled.text('Connecting', 10, 10)
        oled.text('to network...', 10, 32)
        oled.show()
        time.sleep(0.5)
        sta_if.active(True)
        sta_if.connect(config.WIFI_SSID, config.WIFI_PASS)
        while not sta_if.isconnected():
            led.on()
            oled.fill(0)
            oled.text('Cannot connect', 10, 10)
            oled.text('Retrying...', 10, 32)
            oled.show()
            pass
    print('network config:', sta_if.ifconfig())
    oled.fill(0)
    oled.text('Connected', 10, 10)
    oled.text(str(sta_if.ifconfig()[0]), 10, 32)
    oled.text(config.WIFI_SSID, 10, 54)
    oled.show()
    led.off()
    p0.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=callback)
    main()



do_connect()







