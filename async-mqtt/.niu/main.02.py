# Complete project details at https://RandomNerdTutorials.com/micropython-ssd1306-oled-scroll-shapes-esp32-esp8266/

from machine import Pin, I2C
import ssd1306, time, machine, socket
from time import sleep
import config

i2c = I2C(-1, scl=Pin(5), sda=Pin(4))

oled = ssd1306.SSD1306_I2C(128, 64, i2c)
led = machine.Pin(2, machine.Pin.OUT)
relay = Pin(14, Pin.OUT)


# ----- General Functions -----

def do_connect():
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


def relay():
    while True:
    # RELAY ON
        relay.value(0)
        sleep(5)
        oled.fill(0)
        oled.show()
    # RELAY OFF
        relay.value(1)
        sleep(5)
        oled.fill(0)
        oled.show()


# ----- Main Function -----

def main():
    oled.fill(0)
    oled.text('POWERING ON', 10, 10)
    oled.show()
    do_connect()
    relay()

# ----- Run Main Function -----

main()




client = MQTTClient('NodeMCU_52dc166c-2de7-43c1-88ff-f80211c7a8f6', 'mqtt.factoriadigital.cl')
client.connect()

client = MQTTClient("NodeMCU_5", "mqtt.factoriadigital.cl", user="rovak", password="mosca", port=1883) 
