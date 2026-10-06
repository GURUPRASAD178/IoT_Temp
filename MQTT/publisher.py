import serial
import ssl
import paho.mqtt.client as mqtt

HOST="19a0593840e34e83bb2d9f9d421fcb05.s1.eu.hivemq.cloud"
PORT=8883

USERNAME="Guruprasad"
PASSWORD="Gphd1234"

TOPIC="iot/lab/dht11"

arduino=serial.Serial("COM6",9600)

client=mqtt.Client()

client.username_pw_set(USERNAME,PASSWORD)

client.tls_set(cert_reqs=ssl.CERT_REQUIRED)

client.connect(HOST,PORT)

print("Connected")

while True:

    line=arduino.readline().decode().strip()

    print("Publishing:",line)

    client.publish(TOPIC,line)