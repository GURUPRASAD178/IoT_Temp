import sqlite3
import ssl
import paho.mqtt.client as mqtt

HOST="19a0593840e34e83bb2d9f9d421fcb05.s1.eu.hivemq.cloud"
PORT=8883

USERNAME="Guruprasad"
PASSWORD="Gphd1234"

TOPIC="iot/lab/dht11"

db=sqlite3.connect("sensor_data.db",check_same_thread=False)
cursor=db.cursor()

def on_message(client,userdata,msg):

    data=msg.payload.decode()

    print(data)

    hum, temp, hi=data.split(",")

    cursor.execute(
        "INSERT INTO sensor_data(temperature,humidity,heat_index) VALUES(?,?,?)",
        (float(temp),float(hum),float(hi))
    )

    db.commit()

client=mqtt.Client()

client.username_pw_set(USERNAME,PASSWORD)

client.tls_set(cert_reqs=ssl.CERT_REQUIRED)

client.on_message=on_message

client.connect(HOST,PORT)

client.subscribe(TOPIC)

print("Subscriber Started...")

client.loop_forever()





