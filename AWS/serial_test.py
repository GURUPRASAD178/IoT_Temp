import serial

arduino = serial.Serial("COM6",9600)

while True:
    line = arduino.readline().decode().strip()
    print(line)