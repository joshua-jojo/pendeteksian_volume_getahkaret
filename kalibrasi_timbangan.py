from time import sleep
import serial

serialPort = serial.Serial(port="COM5", baudrate=115200, timeout=0.1)


def reset(ser):
    if ser.isOpen() == False:
        ser.open()
    ser.reset_input_buffer()


def kirim_serial(data, data2, serial):
    reset(serial)
    serial.write(bytes("%s %s\n" % (data, data2), "utf-8"))
    sleep(0.1)


def baca_serial(serial):
    while True:
        reset(serial)
        data = serial.readline()
        sleep(1)
        if data == b'':
            pass
        else:
            break
    return int((data).decode())


def test_kalibrasi() :
    beban_asli = int(input("Masukkan beban asli yang di timbang : "))
    sleep(5)
    print('wait....')
    kalibrasi = 640
    while True:
        kirim_serial("kalibrasi", "", serialPort)
        while True:
            nilai_beban = baca_serial(serialPort)
            hitung = beban_asli - nilai_beban
            if hitung < beban_asli and hitung >= 4:
                if abs(hitung) >abs(hitung)*(50/100):
                    print('kurang 100')
                    kirim_serial("c", "", serialPort)
                    baca_serial(serialPort)
                    kalibrasi-=100
                elif abs(hitung) >abs(hitung)*(8/100) :
                    print('kurang 10')
                    kirim_serial("x", "", serialPort)
                    baca_serial(serialPort)
                    kalibrasi-=10

            elif hitung < -4 and hitung >= -beban_asli:
                if abs(hitung) >=20:
                    print('tambah 100')
                    kirim_serial("d", "", serialPort)
                    baca_serial(serialPort)
                    kalibrasi+=100
                elif abs(hitung) >2:
                    print('tambah 10')
                    kirim_serial("s", "", serialPort)
                    baca_serial(serialPort)
                    kalibrasi+=10
            
            elif abs(hitung) < 3 and abs(hitung) > 0 : 
                print(kalibrasi)
            else:
                print(hitung)

baca_serial(serialPort)