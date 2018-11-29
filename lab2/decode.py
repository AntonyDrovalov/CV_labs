import cv2
import numpy as np
import time
import pickle
import struct
import os

file = 'video.tosha'
f = open(file,'rb')
obj = f.read(4)
length = struct.unpack('I',obj)[0]
obj = f.read(length)
pic_0 = pickle.loads(obj)
cv2.imwrite('frame.jpg',pic_0)
height = pic_0.shape[0]
width = pic_0.shape[1]
flag = False

fps = 20
size = (width,height)
videoWriter = cv2.VideoWriter('final_test.avi', cv2.VideoWriter_fourcc('I','4','2','0'), fps, size)

info = os.stat(file)
f_size = info.st_size - length - 4
print(f_size)

while(f_size):
    #line = f.readline()
    #if('' == line ):
    #    print("decoded")
    #    break
    obj = f.read(4)
    length = struct.unpack('I',obj)[0]
    obj = f.read(length)
    pic = pickle.loads(obj)
    f_size = f_size - length - 4
    print(f_size)
    if(flag):
        print('yes')
        #cv2.imshow('frame',pic)
        #cv2.waitKey()
        videoWriter.write(pic)
    else:
        test = np.zeros_like(pic_0)
        for row in range(test.shape[0]):
            for col in range(test.shape[1]):    
                new_row = row+int(pic[row,col,0])
                if new_row>=test.shape[0]: continue
                if new_row<0: continue
                new_col = col+int(pic[row,col,1])
                if new_col>=test.shape[1]: continue
                if new_col<0: continue
                test[new_row,new_col]=pic_0[row,col]
        print('no')
        #cv2.imshow('frame', test)
        #cv2.waitKey()
        videoWriter.write(pic)
    flag = not flag

    


f.close()
cv2.destroyAllWindows()