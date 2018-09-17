import cv2
import numpy as np
import time

videocam = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('closed_frontal_palm.xml')

StartX = 0
StartY = 0
deltaX = 0
deltaY = 0


while True:
    ret , img = videocam.read()
    gray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit = 2.0, tileGridSize=(8,8))
    # img = clahe.apply(gray)
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(hsv)
    h1=clahe.apply(h)
    s1 = clahe.apply(s)
    v1 = clahe.apply(v)

    hsv1 = cv2.merge([h,s,v])
    mask = cv2.inRange(hsv,np.array([0,65,100]),np.array([50,255,255]))
    mask1 = clahe.apply(mask)
    res = cv2.bitwise_and(img,img,mask = mask)
    res_gray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
    res_gray1 = clahe.apply(res_gray)
    faces = face_cascade.detectMultiScale(v1 , 1.1 , 7)
    for (x,y,w,h) in faces:
        deltaX = StartX - x
        deltaY = StartY - y
        # print (deltaX)
        # print (deltaY)
        if(deltaX > 20 ):
            print ('Right')
        elif(deltaX < -20):
            print ('left')
            print deltaX
            print StartX,x
        elif(deltaY<-20):
            print 'down'
        elif(deltaY>20):
            print 'up'

        StartX = x
        StartY = y
        cv2.rectangle(v1 ,(x,y),(x+w,y+h),(255,0,0),2)
        print hsv[y+h/2:y+h,x+w/2:x+w]
    #time.sleep(0.2)

    # cv2.imshow('img', img)
    # cv2.imshow('gray',gray)
    cv2.imshow('hsv',hsv)
    # cv2.imshow('hsv1', v1)
    cv2.imshow('mask',mask)
    # cv2.imshow('mask1', mask1)
    # cv2.imshow('res', res_gray)
    # cv2.imshow('res_gray', res_gray1)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
videocam.release()
cv2.destroyAllWindows()
