import cv2
import time
import numpy as np
import math
import handTracking as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


wCam,hCam=1280,720

cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime=0




detector=htm.handDetector(detectionCon=0.9)

def isInside(circle_x, circle_y, rad, x, y):
     
    if ((x - circle_x) * (x - circle_x) +
        (y - circle_y) * (y - circle_y) <= rad * rad):
        return True;
    else:
        return False;

pointList=[]
penColor=(255,0,255)
while True:
    success,img=cap.read()
    detector.findHands(img)
    lmList=detector.findPosition(img,draw=False)

  
    x1,x2,y1,y2,x3,y3,x0,y0=0,0,0,0,0,0,0,0
    if len(lmList)>0:
        x1,y1=lmList[8][1],lmList[8][2]

        if(x1>=1150 and x1<=1280 and y1>=0 and y1<=150):
            penColor=(255,0,255)
        elif(x1>=1030 and x1<1150 and y1>=0 and y1<=150):
            penColor=(2,255,255)
        x0,y0=lmList[0][1],lmList[0][2]
        x2,y2=lmList[4][1],lmList[4][2]
        x3,y3=lmList[12][1],lmList[12][2]
        length=int(math.hypot(x2-x0,y2-y0))
        length2=int(math.hypot(x3-x0,y3-y0))

        if(length>200):
            if((x1,y1) not in pointList):
                pointList.append((x1,y1,penColor))    
        elif(length2<190):
            for (delx,dely,pencolor) in pointList:
                if(isInside(x1,y1,20,delx,dely)):
                    pointList.remove((delx,dely,pencolor))
   
    for (x,y,pencolor) in pointList:
        # print(x,y)
        cv2.circle(img,(x,y),5,pencolor,cv2.FILLED)
    
    
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.rectangle(img,(1150,0),(1280,150),(255,0,255),-1);
    cv2.rectangle(img,(1030,0),(1150,150),(2,255,255),-1);
 
    cv2.putText(img,f'FPS : {int(fps)}',(10,70),cv2.FONT_HERSHEY_COMPLEX,3,(255,9,255),3)
    cv2.imshow("Img",img)
    cv2.waitKey(1)