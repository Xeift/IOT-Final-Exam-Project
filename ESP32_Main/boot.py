'''
TODO:
1. 在 ESP32 上新增 API，透過 API 將即時資訊顯示在眼鏡上
2. 網頁上每 2 秒自動更新溫溼度
3. 網頁新增淺色/深色模式切換按鈕
4. 記錄溫溼度並導出成 excel
5. 即時圖表
6. CSS 最佳化
7. 結合 LED 顯示
✅8. 新增 SO_REUSEADDR，解決 address in use 的報錯
9. Line 機器人控制
''' 

try: import usocket as socket
except: import socket
from machine import Pin
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

