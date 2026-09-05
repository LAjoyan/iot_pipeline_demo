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

## Step 1: Find Your PC's Local IP Address

The Pico needs your PC's local network IP address to send MQTT messages to the Mosquitto container.

### On Windows

1. Open PowerShell or Command Prompt.
2. Run:

```cmd
ipconfig
```

Locate **Wireless LAN adapter Wi-Fi** and copy the IPv4 Address (e.g., `192.168.0.103`).

### On macOS / Linux

Run:

```bash
# macOS
ipconfig getifaddr en0

# Linux
ip a
```

> **Note:** Both your computer and the Raspberry Pi Pico must be connected to the exact same Wi-Fi network.

---

## Step 2: Run the Pipeline with Docker Compose

We start the Mosquitto broker *first* so that it is ready to receive connections when we plug in the Pico later.

Make sure `src_pipeline/consumer.py` points to the internal Docker service name:

```python
client.connect("mosquitto", 1883)
```

Open your terminal, navigate to `src_pipeline/`, and start the containers:

```bash
cd src_pipeline
docker compose up --build
```

### Verify Incoming Data

The consumer container will build using `uv` on Python 3.13, connect to Mosquitto, and wait. Once the Pico is configured, it will print sensor readings live:

```text
consumer   | {"temperature": 22, "humidity": 48}
consumer   | {'temperature': 22, 'humidity': 48}
```

To stop the containers:

```bash
docker compose down
```

---

## Step 3: Configure and Flash the Pico

### Create Wi-Fi Credentials

Inside `src_pico/`, create a file named `wifi_credentials.json`:

```json
{
  "WIFI_SSID": "YOUR_WIFI_NAME",
  "WIFI_PASSWORD": "YOUR_WIFI_PASSWORD"
}
```

> This file is ignored by `.gitignore` so your private credentials are never pushed to GitHub.

### Update the Broker IP Address

In `src_pico/main.py`, update `MQTT_BROKER` with your machine's local IPv4 address (found in Step 1):

```python
MQTT_BROKER = "192.168.0.103"  # Use your actual IP address here
```

### Initialize the MicroPico Project

To ensure VS Code only uploads the Pico code (and not your Docker files), you should open the Pico folder directly:

1. In VS Code, go to **File > Open Folder...** and open the `src_pico/` directory.
2. Connect your Raspberry Pi Pico WH to your PC via USB.
3. Open the VS Code Command Palette (`Ctrl+Shift+P` on Windows/Linux, `Cmd+Shift+P` on macOS).
4. Type and select **`MicroPico: Configure project`**. This will initialize the hidden `.micropico` configuration file.

### Upload Code to Pico

1. Ensure the MicroPico status bar at the bottom of VS Code shows that your Pico is **Connected**.
2. In the VS Code Explorer file tree, select the following items:
   - `main.py`
   - `wifi.py`
   - `wifi_credentials.json`
   - `umqtt/` (the entire folder)
3. Right-click the selected files and choose **Upload to Pico**.
4. Once the upload is complete, you can manually reset the Pico (unplug the USB and plug it back in).

The Pico will turn on, connect to Wi-Fi (lighting up the LED on pin 15), and immediately start sending data to the Mosquitto broker running on your PC!

---
