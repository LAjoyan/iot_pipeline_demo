import time
from wifi import connect_wifi
from machine import Pin
from dht import DHT11
from umqtt.simple import MQTTClient

time.sleep(0.1)

led = Pin(15, Pin.OUT)
dht_sensor = DHT11(Pin(16))

if connect_wifi():
    led.value(1)


def connect_mqtt():
    client = MQTTClient(client_id="pico", server="<IP_ADDRESS>", port=1883)
    client.connect()
    print("Connected to MQTT")
    return client


while True:
    dht_sensor.measure()
    temp = dht_sensor.temperature()
    humidity = dht_sensor.humidity()

    data = {"temperature": temp, "humidity": humidity}
    print(data)

    time.sleep(1)
