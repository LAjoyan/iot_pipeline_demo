import time
from wifi import connect_wifi
from machine import Pin


time.sleep(0.1)

led = Pin(15, Pin.OUT)

if connect_wifi():
    led.value(1)
