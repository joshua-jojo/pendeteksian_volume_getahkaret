import serial
import hsv

port_kamera = 1

def kalibrasi(kamera):
    hsv.kalibrasi(kamera)

def deteksi(kamera):
    hsv.deteksi(kamera)
if __name__ == "__main__":
    deteksi(port_kamera)
    # kalibrasi(port_kamera)