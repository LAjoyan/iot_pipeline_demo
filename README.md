# IoT Pipeline Demo: Raspberry Pi Pico WH to Mosquitto & Docker

An end-to-end IoT telemetry pipeline that reads environmental data (temperature and humidity) from a DHT11 sensor on a Raspberry Pi Pico WH, transmits it over Wi-Fi via MQTT, and ingests it inside a containerized Python service using Docker Compose.

---

## Project Structure
```text
iot_pipeline_demo/
├── .vscode/
├── src_pico/
│   ├── umqtt/
│   │   └── simple.py
│   ├── .micropico
│   ├── main.py
│   ├── wifi_credentials.json
│   └── wifi.py
├── src_pipeline/
│   ├── .venv/
│   ├── dockerfiles/
│   │   └── consumer.dockerfile
│   ├── .python-version
│   ├── consumer.py
│   ├── docker-compose.yaml
│   ├── pyproject.toml
│   └── uv.lock
├── .gitignore
└── README.md
```
---

## How It Works

1. **Raspberry Pi Pico WH** connects to local Wi-Fi, reads temperature and humidity from the DHT11 sensor every second, serializes the readings into JSON (`{"temperature": 23, "humidity": 45}`), and publishes the payload to topic `home/pico/dht11`.
2. **Mosquitto Broker** runs inside a Docker container listening on port `1883` to route messages.
3. **Consumer Service** runs as a containerized Python application using `uv`, subscribes to the broker using `paho-mqtt`, and parses the real-time sensor stream.

---

## Prerequisites

### Hardware

* Raspberry Pi Pico WH (Flashed with the latest [MicroPython firmware](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html))
* DHT11 Sensor connected to GPIO pin **16**
* LED indicator connected to GPIO pin **15** (lights up when Wi-Fi connects)
* Micro-USB cable

### Software on Your PC

* Python **3.13**
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) (installed and running)
* Visual Studio Code with the **MicroPico** extension installed

---
