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
    gray = cv2.cvtColor(img , cv2.COLOR_BGR2HSV)
    faces = face_cascade.detectMultiScale(gray , 1.1 , 6)
    crop = 0


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
        cv2.rectangle(img ,(x,y),(x+w,y+h),(255,0,0),2)

        crop = img[(y-h if y-h>0 else 0):y+h,(x-w if x-w>0 else 0):x+w]
        # cv2.imshow('crop', crop)    
        #time.sleep(0.2)

    
    cv2.imshow('crop', crop) 
    cv2.imshow('frame',img)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
videocam.release()
cv2.destroyAllWindows()
