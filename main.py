import serial

serialPort = serial.Serial(port = "COM4", baudrate=57600)

while True :
    print(int(serialPort.readline()))