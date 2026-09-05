import time
from wifi import connect_wifi
from machine import Pin
from dht import DHT11
from umqtt.simple import MQTTClient
import json

time.sleep(0.1)

# change representation -> MOSQUITTO needs this
TOPIC = b"home/pico/dht11"
MQTT_BROKER = "192.168.0.103"

led = Pin(15, Pin.OUT)
dht_sensor = DHT11(Pin(16))

if connect_wifi():
    led.value(1)


def connect_mqtt():
    client = MQTTClient(client_id="pico", server="<MQTT_BROKER>", port=1883)
    client.connect()
    print("Connected to MQTT")
    return client


client = connect_mqtt()

while True:
    dht_sensor.measure()
    temp = dht_sensor.temperature()
    humidity = dht_sensor.humidity()

    data = {"temperature": temp, "humidity": humidity}
    print(data)

    # dict -> str '{"temperature": 25, "humidity": 65}'
    payload = json.dumps(data)
    client.publish(TOPIC, payload)

    time.sleep(1)
