import cv2
import numpy as np
import time
import pickle
import struct
import os
import sys


if(len(sys.argv) != 3):
    print('\nWrite : name_of_program input_video output_video\n')
else:
    #cap = cv2.VideoCapture(0)
    print('Compressing video...\n')
    cap = cv2.VideoCapture(sys.argv[1])
    ret, frame1 = cap.read()
    prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
    fps = 20
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    flag = True

    print(size)

    f = open('video_compressed.tosha','wb')
    myObj = pickle.dumps(frame1)
    f.write(bytearray(struct.pack('I',len(myObj))))
    f.write(bytearray(myObj))

    i = 0
    while(ret):
        print(i)
        i = i+1
        ret, frame2 = cap.read()
        if(not ret):
            break
        next = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
        #cv2.imshow('video',frame2)
        
        if(flag):
            flow = cv2.calcOpticalFlowFarneback(prvs,next, None, 0.5, 3, 30, 3, 7, 1.5, 0)
            myObj = pickle.dumps(flow)
        else:
            myObj = pickle.dumps(frame2)
        flag = not flag
        f.write(bytearray(struct.pack('I',len(myObj))))
        f.write(bytearray(myObj))
        #k = cv2.waitKey(30) & 0xff
        #if k == 27:
        #    break
        prvs = next.copy()
        frame1 = frame2.copy()

    f.close()

    print('Loading compressed video...')

    file1 = 'video_compressed.tosha'
    f = open(file1,'rb')
    obj = f.read(4)
    length = struct.unpack('I',obj)[0]
    obj = f.read(length)
    pic_0 = pickle.loads(obj)
    #cv2.imwrite('frame.jpg',pic_0)
    height = pic_0.shape[0]
    width = pic_0.shape[1]
    flag = False

    fps = 20
    size = (width,height)
    videoWriter = cv2.VideoWriter(sys.argv[2], cv2.VideoWriter_fourcc('I','4','2','0'), fps, size)

    info = os.stat(file1)
    f_size = info.st_size - length - 4
    #print(f_size)

    while(f_size):
        obj = f.read(4)
        length = struct.unpack('I',obj)[0]
        obj = f.read(length)
        pic = pickle.loads(obj)
        f_size = f_size - length - 4
        print(f_size)
        if(flag):
            videoWriter.write(pic)
            pic_0 = pic.copy()
        else:
            test = pic_0.copy()
            for row in range(test.shape[0]):
                for col in range(test.shape[1]):    
                    new_row = row+int(pic[row,col,0])
                    if new_row>=test.shape[0]: continue
                    if new_row<0: continue
                    new_col = col+int(pic[row,col,1])
                    if new_col>=test.shape[1]: continue
                    if new_col<0: continue
                    test[new_row,new_col] = pic_0[row,col]
            videoWriter.write(test)
        flag = not flag

    f.close()
    cap.release()
    cv2.destroyAllWindows()
