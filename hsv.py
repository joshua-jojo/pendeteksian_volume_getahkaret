import os
import cv2
import numpy as np

def kalibrasi(kamera) :
    # cek data range warna 
    if os.path.exists("RangeWarna.txt"): 
        # membaca data warna yang tesedia
        data = open("RangeWarna.txt","r")
        data = data.readlines()
    else:
        # set nilai defaut warna
        data = open("RangeWarna.txt","x")
        data.writelines(["255\n","0\n","255\n","0\n","255\n","0"])
        data.close()
        data = ["255","0","255","0","255","0"]

    cam = cv2.VideoCapture(kamera)

    def nothing(x):
        pass

    # trackbar
    cv2.namedWindow('Kalibrasi')
    cv2.resizeWindow("Kalibrasi", 700, 350)
    cv2.createTrackbar('Hue max', 'Kalibrasi', int(data[0]), 255, nothing)
    cv2.createTrackbar('Hue min', 'Kalibrasi', int(data[1]), 255, nothing)
    cv2.createTrackbar('Sat max', 'Kalibrasi', int(data[2]), 255, nothing)
    cv2.createTrackbar('Sat min', 'Kalibrasi', int(data[3]), 255, nothing)
    cv2.createTrackbar('Val max', 'Kalibrasi', int(data[4]), 255, nothing)
    cv2.createTrackbar('Val min', 'Kalibrasi', int(data[5]), 255, nothing)

    while True :
        # membaca frame 
        _,frame = cam.read()

        # flip frame 
        frame = cv2.flip(frame,2)

        # convert RGB to HSV 
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # mengambil nilai dari trackbar
        hue_max = cv2.getTrackbarPos("Hue max","Kalibrasi")
        hue_min = cv2.getTrackbarPos("Hue min","Kalibrasi")
        sat_max = cv2.getTrackbarPos("Sat max","Kalibrasi")
        sat_min = cv2.getTrackbarPos("Sat min","Kalibrasi")
        val_max = cv2.getTrackbarPos("Val max","Kalibrasi")
        val_min = cv2.getTrackbarPos("Val min","Kalibrasi")
        
        # filter warna hsv 
        lower = np.array([hue_min,sat_min,val_min])
        upper = np.array([hue_max,sat_max,val_max])

        # masking filter warna 
        mask = cv2.inRange(hsv, lower, upper)

        # hasil bitwise 
        res = cv2.bitwise_and(frame,frame, mask= mask)

        # menampilkan frame res 
        cv2.imshow("Frame",res)


        # kondisi untuk lepas dari perulangan
        if cv2.waitKey(1) & 0xff == ord('q'):
            break
        elif cv2.waitKey(1) & 0xff == ord('s'):
            print("Memberhentikan program dan menyimpan data warna...")
            data = open("RangeWarna.txt","w")
            data.writelines([str(hue_max)+"\n",str(hue_min)+"\n",str(sat_max)+"\n",str(sat_min)+"\n",str(val_max)+"\n",str(val_min)])
            data.close()
            print("Data warna telah disimpan!")
            break
    cam.release()
    cv2.destroyAllWindows()
    print("Program telah dihentikan.")

def deteksi(kamera):
    try:
        data = open("RangeWarna.txt","r")
        data = data.readlines()
    except:
            print("Range warna tidak ditemukan!")
    cam = cv2.VideoCapture(kamera)
    try:
        while True :
            # membaca frame 
            _,frame = cam.read()

            # flip frame 
            frame = cv2.flip(frame,2)

            # convert RGB to HSV 
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # filter warna hsv 
            lower = np.array([int(data[1]),int(data[3]),int(data[5])])
            upper = np.array([int(data[0]),int(data[2]),int(data[4])])
            
            # masking filter warna 
            mask = cv2.inRange(hsv, lower, upper)

            # hasil bitwise 
            res = cv2.bitwise_and(frame,frame, mask= mask)

            # menampilkan frame res 
            cv2.imshow("Frame",res)


            # kondisi untuk lepas dari perulangan
            if cv2.waitKey(1) & 0xff == ord('q'):
                break
    except:
        print("Program dihentikan")
    cam.release()
    cv2.destroyAllWindows()