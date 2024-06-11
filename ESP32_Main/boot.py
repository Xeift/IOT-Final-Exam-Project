try: import usocket as socket
except: import socket
from machine import Pin, PWM
import network
import time
import esp
import dht

esp.osdebug(None)

import gc
gc.collect()

# ssid = 'HUAWEI-B525-03C8-cccluke'
# password = 'passwordcccluke'

ssid = 'Xeift'
password = '13241324'

station = network.WLAN(network.STA_IF)

station.active(True) # 連上 Wi-Fi
station.connect(ssid, password)

print('------------------------------')
while station.isconnected() == False: print('Wi-Fi 連接中')
print('Wi-Fi 連接成功')
print(station.ifconfig())
print('------------------------------\n')

led = Pin(13, Pin.OUT) # LED 腳位
dht11 = dht.DHT11(Pin(14)) # 溫溼度感測器腳位
red = PWM(Pin(25), freq=1000) # PWM LED 腳位
green = PWM(Pin(26), freq=1000)
blue = PWM(Pin(27), freq=1000)
