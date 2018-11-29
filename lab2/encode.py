import cv2
import numpy as np
import time
import pickle
import struct

cap = cv2.VideoCapture('My.avi')
ret, frame1 = cap.read()
prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
hsv = np.zeros_like(frame1)
hsv[...,1] = 255
fps = 20
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
videoWriter = cv2.VideoWriter('calc.avi', cv2.VideoWriter_fourcc('I','4','2','0'), fps, size)
videoWriter2 = cv2.VideoWriter('flow.avi', cv2.VideoWriter_fourcc('I','4','2','0'), fps, size)
flag = True

f = open('video.tosha','wb')
myObj = pickle.dumps(frame1)
f.write(bytearray(struct.pack('I',len(myObj))))
f.write(bytearray(myObj))


while(1):
    ret, frame2 = cap.read()
    next = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
    #flow = cv2.calcOpticalFlowFarneback(prvs,next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    flow = cv2.calcOpticalFlowFarneback(prvs,next, None, 0.5, 3, 30, 3, 7, 1.5, 0)
    next_calc = np.zeros_like(prvs)
    next_calc[...,1] = 255
    
    calc = np.zeros_like(frame2)
    for row in range(prvs.shape[0]):
        for col in range(prvs.shape[1]):    
            new_row = row+int(flow[row,col,0])
            if new_row>=prvs.shape[0]: continue
            if new_row<0: continue
            new_col = col+int(flow[row,col,1])
            if new_col>=prvs.shape[1]: continue
            if new_col<0: continue
            calc[new_row,new_col]=frame1[row,col]
    videoWriter.write(calc)
    cv2.imshow('calc_frame', calc)
    
    if(flag):
        myObj = pickle.dumps(calc)
    else:
        myObj = pickle.dumps(frame2)
    flag = not flag
    f.write(bytearray(struct.pack('I',len(myObj))))
    f.write(bytearray(myObj))
    
    
    
    #difference = cv2.subtract(prvs, new_frame)    
    #result = not np.any(difference)
    #if result is True:
    #    print ("Pictures are the same")

    mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
    hsv[...,0] = ang*180/np.pi/2
    hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
    bgr = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
    cv2.imshow('frame2',bgr)
    videoWriter2.write(bgr)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    elif k == ord('s'):
        cv2.imwrite('opticalfb.png',frame2)
        cv2.imwrite('opticalhsv.png',bgr)
    prvs = next.copy()
    frame1 = frame2.copy()

'''
cap = cv2.VideoCapture('original.avi')

while(cap.isOpened()):
    ret, frame = cap.read()
    cv2.imshow('final',frame)
    time.sleep(0.1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
'''

f.close()
cap.release()
cv2.destroyAllWindows()