import paho.mqtt.client as mqtt
import json


def on_message(client, userdata, message):
    # needs to decode because original msg is encoded after publishing
    payload = message.payload.decode()

    print(payload)


if __name__ == "__main__":
    client = mqtt.Client()
    client.connect("localhost", 1883)
    client.subscribe("home/pico/dht11")
    client.on_message = on_message
    client.loop_forever()
