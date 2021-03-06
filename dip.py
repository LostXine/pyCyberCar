#!/usr/bin/python
# -*- coding: utf-8 -*-

from config import *
from driver import driver
import cv2, time

class dip:
    __car = None
    
    def process_image(self, image):
        # get timestamp do not change
        uid = time.time()
        
        # --- image processing part --- 
        # *******************

        # --- CyberCar controller part --- 
        # how to control the car:
        # set uid + set motor / steering

        # Motor control:
        # forward  0 -> 1.0
        # backward 0 -> -1.0
                
        # Servo control:
        # left - mid -right
        # -1.0 - 0.0 - 1.0
        if self.__car.setStatus(uid, motor=0.0, servo=0.0):
            print "setStatus() failed."
        # return something to gui function
        res = {}
        return res
        

    def gui(self, res):
        if res.has_key('image'):
            img = res['image']
            if res.has_key('fps'):
                cv2.putText(img, "FPS: " + str(round(res['fps'],2)), (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            # show image
            cv2.imshow("Frame", img)
            # waitkey
            key = cv2.waitKey(1) & 0xff
            # return something not 0 to finish the code
            # check key
            if key == ord("q") or key == 27:
                return 1
        return 0

    def __init__(self):
        self.__car = driver()

    def __del__(self):
        del self.__car
    

