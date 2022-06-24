import serial
import hsv

def baca_serial():
    serialPort = serial.Serial(port = "COM4", baudrate=57600)
    return int(serialPort.readline())

def kalibrasi():
    hsv.kalibrasi()

def deteksi(kamera):
    hsv.deteksi(kamera)
if __name__ == "__main__":
    deteksi(0)