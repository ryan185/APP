from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
prevImg = None
boxList = []

def find_rect_targetColor(image):
    num=0
    x=0
    hsv= cv2.cvtColor(image, cv2.COLOR_BGR2HSV_FULL)
    h = hsv[:, :, 0]
    s = hsv[:, :, 1]
    mask = np.zeros(h.shape, dtype = np.uint8)
    mask[((h < 20) | (h > 150)) & (s > 10)] = 255
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    rects = []
    NumeroContornos = str(len(contours))
    s1= 3
    s2 = 10
    xcnts = []
    for contour in contours:
        if NumeroContornos!=0:
               num=num+1
        area = cv2.contourArea(contour)

        if area < 1:
            approx = cv2.convexHull(contour)  
            rect = cv2.boundingRect(approx)
            rects.append(np.array(rect))
            xcnts.append(contour)
            x=len(xcnts)
    return rects,x

def findLine(image, image1):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,500,700,apertureSize =3)   
    lines = cv2.HoughLinesP(edges, rho = 1, theta = np.pi/180, threshold = 10, minLineLength = 10, maxLineGap = 1)
    lineCount = 0
    contours, hierarchy = cv2.findContours(edges,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    font = cv2.FONT_HERSHEY_SIMPLEX
    if lines is not None:
        lineCount = lines.shape[0]
        for i in range(lineCount):
            x1 = lines[i][0][0]
            y1 = lines[i][0][1]    
            x2 = lines[i][0][2]
            y2 = lines[i][0][3]         
        for contour, hier in zip(contours, hierarchy):
            rox= cv2.boundingRect(contour)
            cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.line(image1, (x1, y1), (x2, y2), (0,0, 255), 2)
            global boxList
            boxList.append(np.array(rox))
    rects,x= find_rect_targetColor(image1)
    return image, image1, lineCount,boxList

def moveDetect(image, grayImg):
    cv2.accumulateWeighted(grayImg, prevImg, 0.99)
    moveImg = cv2.absdiff(grayImg, cv2.convertScaleAbs(prevImg))
    moveImg = cv2.bitwise_and(image, image, mask = moveImg)
    return moveImg

def flashDetect(image,previmage):
    mg = cv2.absdiff(image,previmage)
    blurred = cv2.GaussianBlur(mg, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    lower_white = np.array([0,0,168], dtype=np.uint8)
    upper_white = np.array([172,111,255], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower_white, upper_white)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    res = cv2.bitwise_and(image,image, mask= mask)
    #cv2.imshow("flash",res)
    return res
def circle(image):

    whiteLower = (0,0,168)
    whiteUpper = (172,111,255)

    pts = deque()
    counter = 0
    #frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(image, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, whiteLower, whiteUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    #cv2.imshow("mask", mask)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        if radius > 10:
            cv2.circle(image, (int(x), int(y)), int(radius),(0, 255, 255), 2)   
            pts.appendleft(center)
    
    #cv2.imshow("Frame", image)
    counter += 1
    return image

def main():
    cv2.namedWindow("original", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("original", 800, 600)
    cv2.moveWindow("original",0 , 40)
    cv2.namedWindow("Result", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Result", 800, 600)
    cv2.moveWindow("Result",900, 120)
    cv2.namedWindow("flash", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("flash", 600, 400)
    cv2.moveWindow("flash",1200, 200)
    #cam = cv2.VideoCapture("/home/nvidia/Desktop/spx/spark.mp4")
    cam = cv2.VideoCapture("/home/nvidia/Desktop/spx/sparkPJ1.mp4")
    #cam = cv2.VideoCapture("/home/nvidia/Desktop/spark/welding.mp4")
    #cam = cv2.VideoCapture("/home/nvidia/Desktop/spark/IMG_0009.MOV")
    #cam = cv2.VideoCapture("/home/nvidia/Desktop/spark/spark001.mp4")
    #cam = cv2.VideoCapture("/home/nvidia/Desktop/spark/spark002.mp4")
    #cam = cv2.VideoCapture("/home/nvidia/Desktop/spark/spark003.mp4")
    #cam = cv2.VideoCapture("/home/nvidia/Desktop/spark/spark004.mp4")
    #cam = cv2.VideoCapture("/home/nvidia/Desktop/spark/spark005.mp4")
    #cam.set(0, 9000)
    #cam = cv2.VideoCapture(0)
    fps = cam.get(cv2.CAP_PROP_FPS)
    timestamps = [cam.get(cv2.CAP_PROP_POS_MSEC)]
    calc_timestamps = [0.0]
    prev=0.0
    curv = 0.0
    xImage = None
    while True:
        spt = 0
        ret, image = cam.read()
        image = cv2.resize(image, dsize = (640, 480))
        dupimage=image.copy()
        imposeImg=image.copy()
        if ret:
            cv2.imshow("original", image)
            gray = cv2.cvtColor(dupimage, cv2.COLOR_BGR2GRAY)
            global prevImg

            if prevImg is None:
                prevImg = gray.copy().astype("float")
                continue
            moveImg = moveDetect(image, gray)
            prevImg  = gray.copy().astype("float")
            cv2.imshow("original", image)
            if((np.mean(moveImg)>0.01) and (np.mean(moveImg)<1)):
                print np.mean(moveImg)
                rects,x= find_rect_targetColor(moveImg)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                edges = cv2.Canny(gray,500,700,apertureSize =3)   
                contours, hierarchy = cv2.findContours(edges,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
                for rect in rects:
                    cv2.rectangle(moveImg, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), (0, 255, 0), thickness = 2)
                    cv2.rectangle(imposeImg, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), (0, 255, 0), thickness = 2)
                cv2.imshow("original", image)
                resultImage, resultWithLineAndPoints, lineCount,boxList= findLine(moveImg, imposeImg)

                spt= x + (lineCount*100)
                sptP = float(spt) / 1000.0
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(resultWithLineAndPoints,'LineCount : '+str(lineCount),(50,50), font, .5,(255,255,255),2,True)
                cv2.putText(resultWithLineAndPoints,'PointCount : '+str(x),(50,70), font, .5,(255,255,255),2,True)
                cv2.putText(resultWithLineAndPoints,'SPARKRATE : '+str(spt),(50,90), font, .5,(255,255,255),2,True)
                cv2.line(resultWithLineAndPoints,(20,460),(20,460-(int(460.0*sptP))),(255,0,0),30)
                #ress=circle(resultWithLineAndPoints)

                #cv2.imshow("circle", ress)  
                cv2.imshow("Result", resultWithLineAndPoints)  
            if (np.mean(moveImg)>=1 and np.mean(moveImg)< 1000 and xImage is not None):
                if prev == 0:
                        prev = cam.get(cv2.CAP_PROP_POS_MSEC)
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        cv2.putText(resultWithLineAndPoints,'FlashDifferen ce : '+str(prev),(50,110), font, .5,(255,255,255),2,True)
        	        resultWithLineAndPoints=flashDetect(resultWithLineAndPoints, prev)
                        cv2.imshow("flash", resultWithLineAndPoints)   
                        #print prev
                else:
                        prev=cam.get(cv2.CAP_PROP_POS_MSEC) - prev
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        cv2.putText(resultWithLineAndPoints,'FlashDifference : '+str(prev),(50,110), font, .5,(255,255,255),2,True)
        	        resultWithLineAndPoints=flashDetect(resultWithLineAndPoints, prev)
			#cv2.imshow("Result",  b)
                        #cv2.imshow("flash", resultWithLineAndPoints)      
                        prev = 0.0
            	#cv2.imshow("Result", resultWithLineAndPoints)
            xImage=image.copy()
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            ret, image = cam.read()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
