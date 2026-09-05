import time
from wifi import connect_wifi
from machine import Pin
from dht import DHT11


time.sleep(0.1)

led = Pin(15, Pin.OUT)
dht_sensor = DHT11(Pin(16))

if connect_wifi():
    led.value(1)

while True:
    dht_sensor.measure()
    temp = dht_sensor.temperature()
    humidity = dht_sensor.humidity()

    data = {"temperature": temp, "humidity": humidity}
    print(data)
