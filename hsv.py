import os
from time import sleep
import cv2
import numpy as np
from imutils import perspective
import imutils
from scipy.spatial import distance as dist
import serial

serialPort = serial.Serial(port="COM5", baudrate=115200,timeout=0.1)

def reset(ser):
    if ser.isOpen() == False:
            ser.open()
    ser.reset_input_buffer()


def kirim_serial(data, data2,serial):
    serial.write(bytes("%s %s\n"%(data,data2),"utf-8"))
    reset(serial)
    sleep(0.1)



def kalibrasi(kamera):
    # cek data range warna
    if os.path.exists("RangeWarna.txt"):
        # membaca data warna yang tesedia
        data = open("RangeWarna.txt", "r")
        data = data.readlines()
    else:
        # set nilai defaut warna
        data = open("RangeWarna.txt", "x")
        data.writelines(["255\n", "0\n", "255\n", "0\n", "255\n", "0"])
        data.close()
        data = ["255", "0", "255", "0", "255", "0"]

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

    while True:
        # membaca frame
        _, frame = cam.read()

        # flip frame
        frame = cv2.flip(frame, 2)

        # convert RGB to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv = cv2.GaussianBlur(hsv, (35, 35), 0)

        # mengambil nilai dari trackbar
        hue_max = cv2.getTrackbarPos("Hue max", "Kalibrasi")
        hue_min = cv2.getTrackbarPos("Hue min", "Kalibrasi")
        sat_max = cv2.getTrackbarPos("Sat max", "Kalibrasi")
        sat_min = cv2.getTrackbarPos("Sat min", "Kalibrasi")
        val_max = cv2.getTrackbarPos("Val max", "Kalibrasi")
        val_min = cv2.getTrackbarPos("Val min", "Kalibrasi")

        # filter warna hsv
        lower = np.array([hue_min, sat_min, val_min])
        upper = np.array([hue_max, sat_max, val_max])

        # masking filter warna
        mask = cv2.inRange(hsv, lower, upper)

        # hasil bitwise
        res = cv2.bitwise_and(frame, frame, mask=mask)

        # menampilkan frame res
        cv2.imshow("Frame", res)

        # kondisi untuk lepas dari perulangan
        if cv2.waitKey(1) & 0xff == ord('q'):
            break
        elif cv2.waitKey(1) & 0xff == ord('s'):
            print("Memberhentikan program dan menyimpan data warna...")
            data = open("RangeWarna.txt", "w")
            data.writelines([str(hue_max)+"\n", str(hue_min)+"\n", str(sat_max) +
                            "\n", str(sat_min)+"\n", str(val_max)+"\n", str(val_min)])
            data.close()
            print("Data warna telah disimpan!")
            break
    cam.release()
    cv2.destroyAllWindows()
    print("Program telah dihentikan.")


def deteksi(kamera):
    try:
        data = open("RangeWarna.txt", "r")
        data = data.readlines()
    except:
        print("Range warna tidak ditemukan!")
    cam = cv2.VideoCapture(kamera)
    # try:

    def midpoint(ptA, ptB):
        return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

    def biggestContourI(contours):
        maxVal = 0
        maxI = None
        for i in range(0, len(contours) - 1):
            if len(contours[i]) > maxVal:
                cs = contours[i]
                maxVal = len(contours[i])
                maxI = i
        return maxI
    while True:
        # membaca frame
        _, frame = cam.read()

        # flip frame
        frame = cv2.flip(frame, 2)

        # convert RGB to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv = cv2.GaussianBlur(hsv, (35, 35), 0)

        # filter warna hsv
        lower = np.array([int(data[1]), int(data[3]), int(data[5])])
        upper = np.array([int(data[0]), int(data[2]), int(data[4])])

        # masking filter warna
        mask = cv2.inRange(hsv, lower, upper)

        # hasil bitwise
        res = cv2.bitwise_and(frame, frame, mask=mask)

        edges = cv2.Canny(mask, 100, 200)
        edged = cv2.dilate(edges, None, iterations=1)
        edged = cv2.erode(edged, None, iterations=1)

        h, w = frame.shape[:2]

        contours, hierarchy = cv2.findContours(
            edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        pixelsPerMetric = 65

        # # loop over the contours individually
        for c in contours:
            # if the contour is not sufficiently large, ignore it
            if cv2.contourArea(c) < 100:
                continue
            # compute the rotated bounding box of the contour
            orig = frame
            box = cv2.minAreaRect(c)
            box = cv2.cv.BoxPoints(
                box) if imutils.is_cv2() else cv2.boxPoints(box)
            box = np.array(box, dtype="int")
        #     # order the points in the contour such that they appear
        #     # in top-left, top-right, bottom-right, and bottom-left
        #     # order, then draw the outline of the rotated bounding
        #     # box
            box = perspective.order_points(box)
            cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)
        #     # loop over the original points and draw them
            for (x, y) in box:
                cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)

        #     # unpack the ordered bounding box, then compute the midpoint
        #     # between the top-left and top-right coordinates, followed by
        #     # the midpoint between bottom-left and bottom-right coordinates
            (tl, tr, br, bl) = box
            (tltrX, tltrY) = midpoint(tl, tr)
            (blbrX, blbrY) = midpoint(bl, br)
        #     # compute the midpoint between the top-left and top-right points,
        #     # followed by the midpoint between the top-righ and bottom-right
            (tlblX, tlblY) = midpoint(tl, bl)
            (trbrX, trbrY) = midpoint(tr, br)
        #     # draw the midpoints on the image
            cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
            cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
            cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
            cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)
        #     # draw lines between the midpoints
            cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
                     (255, 0, 255), 2)
            cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
                     (255, 0, 255), 2)
        #     # compute the Euclidean distance between the midpoints
            dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
            dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
        #     # if the pixels per metric has not been initialized, then
        #     # compute it as the ratio of pixels to supplied metric
        #     # (in this case, inches)

            if pixelsPerMetric is None:
                pixelsPerMetric = dB / w
        #                 # compute the size of the object
            dimA = dA / pixelsPerMetric
            dimB = dB / pixelsPerMetric
        #     # draw the object sizes on the image
            cv2.putText(orig, "{:.1f}cm".format(dimA*2.54),
                        (int(tltrX - 15), int(tltrY - 10)
                         ), cv2.FONT_HERSHEY_SIMPLEX,
                        0.65, (255, 255, 255), 2)
            cv2.putText(orig, "{:.1f}cm".format(dimB*2.54),
                        (int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
                        0.65, (255, 255, 255), 2)

        # menampilkan frame res
            cv2.imshow("Frame", hsv)
            cv2.imshow("Final", orig)
        # cv2.imshow("Edge",edges)

            panjang = dimA*2.54 * 10
            lebar = dimB*2.54 * 10
            
            kirim_serial(int(panjang), int(lebar),serialPort)
        # kondisi untuk lepas dari perulangan
        if cv2.waitKey(1) & 0xff == ord('q'):
            break
    # except:
        # print("Program dihentikan")
    cam.release()
    cv2.destroyAllWindows()
