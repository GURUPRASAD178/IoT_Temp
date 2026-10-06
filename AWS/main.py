import json
import serial
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# -----------------------------
# AWS IoT Configuration
# -----------------------------

ENDPOINT = "ahoayyxc9cm2h-ats.iot.ap-southeast-2.amazonaws.com"

CLIENT_ID = "ArduinoDHT11"

TOPIC = "sensor/dht11"

ROOT_CA = "AmazonRootCA1.pem"

PRIVATE_KEY = "33a6c8b0fe9fe0ebf57109d7fc3f1c1679c051c0717659dfa84dec651c305cde-private.pem.key"

CERTIFICATE = "33a6c8b0fe9fe0ebf57109d7fc3f1c1679c051c0717659dfa84dec651c305cde-certificate.pem.crt"

# -----------------------------
# Create MQTT Client
# -----------------------------

client = AWSIoTMQTTClient(CLIENT_ID)

client.configureEndpoint(ENDPOINT, 8883)

client.configureCredentials(
    ROOT_CA,
    PRIVATE_KEY,
    CERTIFICATE
)

client.connect()

print("Connected to AWS IoT")

# -----------------------------
# Arduino Serial Port
# -----------------------------

arduino = serial.Serial("COM6",9600)

while True:

    line = arduino.readline().decode().strip()

    try:

        humidity, temperature, heat_index = line.split(",")

        payload = {
            "deviceId": "Arduino001",
            "humidity": float(humidity),
            "temperature": float(temperature),
            "heat_index": float(heat_index)
        }

        client.publish(
            TOPIC,
            json.dumps(payload),
            1
        )

        print(payload)

    except Exception as e:

        print("Error:",e)