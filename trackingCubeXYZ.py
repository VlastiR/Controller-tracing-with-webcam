#https://www.youtube.com/watch?v=IXyO2O-I2bs   https://www.youtube.com/watch?v=IXyO2O-I2bs
import cv2
import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
import time
from OpenGL.GLU import *
import openvr
#region cube
xx=1
yy=1
zz=1
standartVerticies = [[0.3, -0.3, -0.3],[0.3, 0.3, -0.3],[-0.3, 0.3, -0.3],[-0.3, -0.3, -0.3],[0.3, -0.3, 0.3],[0.3, 0.3, 0.3],[-0.3, -0.3, 0.3],[-0.3, 0.3, 0.3]]
standartEdges = [[0.3, -0.3, -0.3],[0.3, 0.3, -0.3],[-0.3, 0.3, -0.3],[-0.3, -0.3, -0.3],[0.3, -0.3, 0.3],[0.3, 0.3, 0.3],[-0.3, -0.3, 0.3],[-0.3, 0.3, 0.3]]
verticies = [[1, -1, -1],[1, 1, -1],[-1, 1, -1],[-1, -1, -1],[1, -1, 1],[1, 1, 1],[-1, -1, 1],[-1, 1, 1]]
edges = [[0,1],[0,3],[0,4],[2,1],[2,3],[2,7],[6,3],[6,4],[6,7],[5,1],[5,4],[5,7]]
def Cube():
    global verticies,edges
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()

#glEnd()
pygame.init()
display = (800,600)
pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
glTranslatef(0.0,0.0, -5)
#endregion
cap2=cv2.VideoCapture(0)
cap=cv2.VideoCapture(1)
while True:
    _, frame =cap.read()
    _, frame2 =cap2.read()
    hsv=cv2.cvtColor(frame , cv2.COLOR_BGR2HSV)
    hsv2=cv2.cvtColor(frame2 , cv2.COLOR_BGR2HSV)

    lower_green=np.array([50,70,70])#100,100,100   50,70,70 
    upper_green=np.array([80,255,255])#120,255,255   80,255,255
    green=cv2.inRange(hsv,lower_green,upper_green)
    res=cv2.bitwise_and(frame,frame,mask=green)

    lower_blue=np.array([100,100,100])#100,100,100
    upper_blue=np.array([255,255,255])#120,255,255
    blue=cv2.inRange(hsv2,lower_blue,upper_blue)
    res2=cv2.bitwise_and(frame2,frame2,mask=blue)

    #kernal = np.ones((5 ,5), "uint8")
    #green=cv2.dilate(green, kernal)
    #res=cv2.bitwise_and(frame,frame,green=green)


    (contours,hierarchy)=cv2.findContours(green,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area>1000):
			
            x,y,w,h = cv2.boundingRect(contour)	
            green = cv2.rectangle(green,(x,y),(x+w,y+h),(100,100,100),2)
            frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
            cv2.putText(frame,"GREEN",(x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255))
            #print(x,y)
            
            zz=(x-150)*0.01
            yy=(y-150)*0.005

    (contours,hierarchy)=cv2.findContours(blue,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area>5000):
			
            x,y,w,h = cv2.boundingRect(contour)	
            blue = cv2.rectangle(blue,(x,y),(x+w,y+h),(255,255,255),2)
            frame2 = cv2.rectangle(frame2,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.putText(frame2,"BLUE",(x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0))
            #print(x,y)
            xx=(x-300)*0.005

    #cv2.imshow("frame",frame)
    #cv2.imshow("res",res)


    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    Cube()
    pygame.display.flip()
    for i in range(len(standartVerticies)):
        for j in range(len(standartVerticies[i])):
            if j==2:verticies[i][j]=(standartVerticies[i][j]+zz)#300 135
            if j==1:verticies[i][j]=(standartVerticies[i][j]+yy)*(-1)
            if j==0:verticies[i][j]=(standartVerticies[i][j]+xx)*(-1)
    openvr.ControllerEventOutput_VREvents=10
    print(openvr.ControllerEventOutput_VREvents)

    #cv2.imshow("res",res)
    cv2.imshow("res2",res2)
    cv2.imshow("frame",frame)
    cv2.imshow("frame2",frame2)
    #cv2.imshow("green",green)
    #cv2.imshow("blue",blue)

    k=cv2.waitKey(5) & 0xFF
    if k == 27:break
cv2.destroyAllWindows()
cap.release()
