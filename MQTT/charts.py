import ssl
import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

HOST="19a0593840e34e83bb2d9f9d421fcb05.s1.eu.hivemq.cloud"
PORT=8883

USERNAME="Guruprasad"
PASSWORD="Gphd1234"

TOPIC="iot/lab/dht11"

temperature=[]
humidity=[]
heatindex=[]

def on_message(client,userdata,msg):

    data=msg.payload.decode()

    t,h, hi=data.split(",")

    temperature.append(float(t))
    humidity.append(float(h))
    heatindex.append(float(hi))

    if len(temperature)>50:
        temperature.pop(0)
        humidity.pop(0)
        heatindex.pop(0)

client=mqtt.Client()

client.username_pw_set(USERNAME,PASSWORD)

client.tls_set(cert_reqs=ssl.CERT_REQUIRED)

client.on_message=on_message

client.connect(HOST,PORT)

client.subscribe(TOPIC)

client.loop_start()

fig,(ax1,ax2, ax3)=plt.subplots(3,1)

def update(frame):

    ax1.clear()
    ax2.clear()
    ax3.clear()

    ax1.plot(temperature,marker='o')
    ax1.set_title("Temperature")

    ax2.plot(humidity,marker='o')
    ax2.set_title("Humidity")

    ax3.plot(heatindex,marker='o')
    ax3.set_title("Heat Index")

ani=FuncAnimation(fig,update,interval=1000)

plt.tight_layout()

plt.show()