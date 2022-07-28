import os
import numpy as np
import cv2
import mediapipe as mp
import module1 as m
import time
import cvzone


video=cv2.VideoCapture(0)

video.set(3,1280)
video.set(4,720)
p_time=0

xp,yp=0,0
ImageCanvas=np.zeros((720,1280,3),dtype='uint8')
obj=m.handD(min_detection_confidence=0.6)

# Creating trackbars
cv2.namedWindow('win')
def fun(x):
    pass
cv2.createTrackbar('B','win',0,255,fun)
cv2.createTrackbar('G','win',0,255,fun)
cv2.createTrackbar('R','win',0,255,fun)


while True:
    _,img=video.read()
    img=cv2.flip(img,1)
    b = cv2.getTrackbarPos('B', 'win')
    g = cv2.getTrackbarPos('G', 'win')
    r = cv2.getTrackbarPos('R', 'win')

    img=obj.fhands(img)

    lm=obj.posLandmarks(img)

    if(len(lm)!=0):
        # print(lm)
        x1,y1=lm[8][1:]
        x2,y2=lm[12][1:]

        f=obj.fUp()
        # print(f)



        if f[1:5]==[1,1,1,1]:
            cv2.line(ImageCanvas, (xp, yp), (x1, y1), (0, 0, 0), 50)

        elif f[1] and f[2]:
            # print('Drwaing Mode')

            cv2.circle(img, (x1, y1), 15, (b,g,r), cv2.FILLED)
            # cv2.circle(ImageCanvas,(x1,y1),15,(0,0,255),cv2.FILLED)
            if xp == 0 and yp == 0:
                xp, yp = x1, y1
            cv2.line(ImageCanvas, (xp, yp), (x1, y1), (b,g,r), 4)
            xp, yp = x1, y1

        elif f[1] == 1:
            cv2.putText(img, 'Move', (x1, y1), None, 3, (255, 0, 0), 3)
            xp, yp = 0, 0


    # cv2.rectangle(img,(lm[18][1:]),(lm[3][1:]),(255,0,0),3)

    imgGrey = cv2.cvtColor(ImageCanvas, cv2.COLOR_BGR2GRAY)
    _,imgInv = cv2.threshold(imgGrey,50,255,cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img,imgInv)
    img = cv2.bitwise_or(img,ImageCanvas)
    cv2.imshow('Paint', img)
    c_time=time.time()
    fps=1/(c_time-p_time)
    p_time=c_time

    cv2.putText(img,str(int(fps)),(10,100),None,3,(0,0,255),5)
    # cv2.addWeighted(img,0.5,ImageCanvas,0.5,0.5)

    # cv2.imshow('RealPaint', ImageCanvas)
    if cv2.waitKey(2) & 0xFF==ord('q'):
        break


video.release()
cv2.destroyAllWindows()
