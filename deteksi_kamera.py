import cv2

cam = cv2.VideoCapture(1)

while True:
    _, frame = cam.read()
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) & 0xff == ord("q"):
        break