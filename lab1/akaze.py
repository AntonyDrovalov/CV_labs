import numpy as np
import cv2
import os
import time

from matplotlib import pyplot as plt

def matching(des1,des2): 
    bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
    matchezz = bf.match(des1, des2)
    return sorted(matchezz, key=lambda x: x.distance)


def local(kp,kp2):
    origin_x = 0
    origin_y = 0
    test_x = 0
    test_y = 0
    for item in kp:
        origin_x = origin_x + item.pt[0]
        origin_y = origin_y + item.pt[1]

    for item in kp2:
        test_x = test_x + item.pt[0]
        test_y = test_y + item.pt[1]

    origin_x = origin_x/len(kp)
    origin_y = origin_y/len(kp)
    test_x = test_x/len(kp2)
    test_y = test_y/len(kp2)

    dx = origin_x - test_x
    dy = origin_y - test_y

    #print('average kp : ' + str(origin_x) + ' ' + str(origin_y))
    #print('average kp2 : ' + str(test_x) + ' ' + str(test_y))
    #print('localisation: dx = ' + str(dx) + ' dy = ' + str(dy) )
    return (dx,dy)
    #cv2.circle(imgRGB,(int(origin_x),int(origin_y)), 50, (0,0,255), -1)
    #plt.imshow(imgRGB),plt.show()


# To compare two photos(draw centers and matches) 
def compare(img1_path,img2_path):
    imgRGB = cv2.imread(img1_path)
    img = cv2.cvtColor(imgRGB, cv2.COLOR_BGR2GRAY)
    kp, des = akaze.detectAndCompute(img, None)

    #testRGB = cv2.imread('dataset_bear/_DSC0290.JPG')
    testRGB = cv2.imread(img2_path)
    test = cv2.cvtColor(testRGB, cv2.COLOR_BGR2GRAY)
    kp2, des2 = akaze.detectAndCompute(test, None)
    matches = matching(des,des2)
    wKeypoints = cv2.drawMatches(img, kp, test, kp2, matches[:100], None, flags=2)
    
    origin_x = 0
    origin_y = 0
    test_x = 0
    test_y = 0
    for item in kp:
        origin_x = origin_x + item.pt[0]
        origin_y = origin_y + item.pt[1]

    for item in kp2:
        test_x = test_x + item.pt[0]
        test_y = test_y + item.pt[1]

    origin_x = origin_x/len(kp)
    origin_y = origin_y/len(kp)
    test_x = test_x/len(kp2)
    test_y = test_y/len(kp2)

    cv2.circle(imgRGB,(int(origin_x),int(origin_y)), 50, (0,0,255), -1)
    cv2.circle(testRGB,(int(test_x),int(test_y)), 50, (0,0,255), -1)
    
    plt.imshow(imgRGB), plt.show()
    plt.imshow(testRGB), plt.show()
    plt.imshow(wKeypoints), plt.show()

# To get metrics (time,localisation(dx,dy),percent of true matches)
def metrics(img_path,dataset_path):
    imgRGB = cv2.imread(img_path)
    img = cv2.cvtColor(imgRGB, cv2.COLOR_BGR2GRAY)
    kp, des = akaze.detectAndCompute(img, None)

    counter = 0
    countMatches = 0
    myTime = 0
    size = 0
    #path = "dataset_monkey"

    file = open("conclusion.txt","w")

    dir = os.listdir(dataset_path)

    for item in dir:
        testRGB = cv2.imread(dataset_path + '/' + item)
        test = cv2.cvtColor(testRGB, cv2.COLOR_BGR2GRAY)

        kp2, des2 = akaze.detectAndCompute(test, None)

        start = time.clock()

        matches = matching(des,des2)

        elapsed = time.clock()
        elapsed = elapsed - start

        countMatches = countMatches + len(matches)
        size = size + os.path.getsize(dataset_path + '/' + item)
        myTime = myTime + elapsed
        counter = counter + 1

        dx,dy = local(kp,kp2)

        print('photo ' + str(counter) + ' ' + item + ': ')
        print('time : ' + str(elapsed))
        print("keypoints: " + str(len(kp)))
        print("keypoints 2: " + str(len(kp2)))
        print("matches: "+ str(len(matches)))
        print("percent: " + str(len(matches)/len(kp)))
        print("match distance: " + str(matches[0].distance) +' '+ str(matches[-1].distance))
        print("dx = " + str(dx) + ' dy = ' + str(dy))
        print()

        file.write('photo ' + str(counter) + ' ' + item + ':\n')
        file.write('time : ' + str(elapsed) + '\n')
        file.write("keypoints: " + str(len(kp)) + '\n')
        file.write("keypoints 2: " + str(len(kp2)) + '\n')
        file.write("matches: "+ str(len(matches)) + '\n')
        file.write("percent: " + str(len(matches)/len(kp)) + '\n')
        file.write("match distance: " + str(matches[0].distance) +' '+ str(matches[-1].distance) + '\n')
        file.write("dx = " + str(dx) + ' dy = ' + str(dy) + '\n')
        

    file.write('Conclusion: \n')
    file.write('percent: ' + str(countMatches/(len(kp)*len(dir)))+ '\n')
    file.write('seconds per 1 Mb: ' + str(myTime*1000/size)+ '\n')

    file.close()


akaze = cv2.AKAZE_create()
metrics('original_bear.JPG','dataset1')
#compare('original_bear.JPG','dataset_bear/_DSC0290.JPG')
