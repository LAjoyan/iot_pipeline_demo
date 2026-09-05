import paho.mqtt.client as mqtt
import json


def on_message(client, userdata, message):
    payload = message.payload.decode()
    data = json.loads(payload)

    print(payload)

    print(data)


if __name__ == "__main__":
    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    client.connect("mosquitto", 1883)
    client.subscribe("home/pico/dht11")
    client.on_message = on_message
    client.loop_forever()
