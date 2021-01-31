from mqtt_as import config


config['server'] = 'mqtt.factoriadigital.cl'  # Change to suit e.g. 'iot.eclipse.org'


# Required on Pyboard D and ESP32. On ESP8266 these may be omitted (see above).
config['ssid'] = 'VTR-3040963'
config['wifi_pw'] = '5djkhmJXzzdw'