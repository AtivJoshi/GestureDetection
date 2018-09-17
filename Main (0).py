import cv2
import numpy as np
import time
import volume
import Media_Controll
import math

videocam = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('palm.xml')

StartX = 0
StartY = 0
deltaX = 0
deltaY = 0

while True:
    ret , img = videocam.read()
    gray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray , 1.1 , 6)
    #blur = cv2.GaussianBlur(gray,(35,35),0)
    # crop_img = gray
    cv2.rectangle(img,(300,300),(100,100),(0,255,0),0)
    crop_img = img[100:300, 100:300]
    # for (x,y,w,h) in faces:
    #     cv2.rectangle(img ,(x,y),(x+w,y+h),(255,0,0),2)
    #     if(x>50 and y>50 and w>50 and h>50):
    #         print 'inside'
    #         crop_img_gray = gray[y:h, x:w]
    #         crop_img = cv2.GaussianBlur(crop_img_gray,(30,30),0)            
    cv2.imshow('cropped',crop_img)

    ret,thresh1 = cv2.threshold(crop_img,30,200,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    image, contours, hierarchy = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    
    cnt = max(contours, key = lambda x: cv2.contourArea(x))
    
    x,y,w,h = cv2.boundingRect(cnt)
    cv2.rectangle(crop_img,(x,y),(x+w,y+h),(0,0,255),0)
    hull = cv2.convexHull(cnt)
    drawing = np.zeros(crop_img.shape,np.uint8)
    cv2.drawContours(drawing,[cnt],0,(0,255,0),0)
    cv2.drawContours(drawing,[hull],0,(0,0,255),0)
    hull = cv2.convexHull(cnt,returnPoints = False)
    defects = cv2.convexityDefects(cnt,hull)
    count_defects = 0
    cv2.drawContours(thresh1, contours, -1, (0,255,0), 3)
    for i in range(defects.shape[0]):
        s,e,f,d = defects[i,0]
        start = tuple(cnt[s][0])
        end = tuple(cnt[e][0])
        far = tuple(cnt[f][0])
        a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
        b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
        c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
        angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
        if angle <= 90:
            count_defects += 1
            cv2.circle(crop_img,far,1,[0,0,255],-1)
        #dist = cv2.pointPolygonTest(cnt,far,True)
        cv2.line(crop_img,start,end,[0,255,0],2)
        # print count_defects
    cv2.imshow('frame',img)
    cv2.imshow('drawing',drawing)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

videocam.release()
cv2.destroyAllWindows()