import numpy as np
import cv2
import time

clicked = False

def onMouse(event, x, y, flags, param):
    global clicked
    if event == cv2.EVENT_LBUTTONUP:
        clicked = True

cameraCapture = cv2.VideoCapture(0)
cv2.namedWindow('MyWindow')
cv2.setMouseCallback('MyWindow', onMouse)
print ('Showing camera feed. Click window or press any key to stop.')
size = (int(cameraCapture.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cameraCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
fps = 30

videoWriter = cv2.VideoWriter('My.avi', cv2.VideoWriter_fourcc('I','4','2','0'),fps, size)
success, frame = cameraCapture.read()
while success and cv2.waitKey(1) == 255 and not clicked:
    cv2.imshow('MyWindow', frame)
    videoWriter.write(frame)
    success, frame = cameraCapture.read()

cap = cv2.VideoCapture('My.avi')

while(cap.isOpened()):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    gray = cv2.cvtColor(gray,cv2.COLOR_GRAY2RGB)
    cv2.line(gray,(0,0),(size[0],size[1]),(203,192,255),5)
    cv2.rectangle(gray,(int(size[0]/2),int(size[1]/2)),(size[0],size[1]),(0,255,0),3)
    cv2.imshow('gray',gray)
    time.sleep(0.1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cameraCapture.release()
cv2.destroyAllWindows()