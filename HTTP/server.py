from flask import Flask
import serial
import time

arduino = serial.Serial('COM6',9600,timeout=2)

time.sleep(2)

app = Flask(__name__)

@app.route('/')

def home():

    arduino.write(b'GET\n')

    data = arduino.readline().decode().strip()

    if data=="ERROR" or data=="":
        return "Sensor Error"

    print("Received data:", repr(data))

    temp=data.split(",")[0]

    html=f"""
    <html>
    <head>
    <title>IoT HTTP</title>
    <meta http-equiv="refresh" content="2">
    </head>

    <body>

    <h1>Temperature and Humidity</h1>

    <h2> {temp} °C</h2>


    </body>
    </html>
    """

    return html

app.run(host="0.0.0.0",port=5000)