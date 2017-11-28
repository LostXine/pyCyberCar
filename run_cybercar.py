#!/usr/bin/python
# -*- coding: utf-8 -*-

from driver import driver
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

def run_cybercar():
    print "==========CyberCar Start=========="
    # init picamera
    c = PiCamera()
    c.resolution = (640, 480)
    c.framerate = 25
    # prepare memery
    raw = PiRGBArray(c, c.resolution)
    # init car driver
    d = driver()
    try:
        for frame in c.capture_continuous(raw, format='bgr', use_video_port=True):
            # get timestamp
            uid = time.time()
            # grab image for opencv
            image = frame.array
            # show image
            cv2.imshow("Frame", image)
            # waitkey
            key = cv2.waitKey(10) & 0xff
            # reset
            raw.truncate(0)
            # check key
            if key == ord("q") or key == 27:
                break

            # how to control the car:

            # set uid + set motor / steering

            # Motor control:
            # forward  0 -> 1.0
            # backward 0 -> -1.0
            
            # Servo control:
            # left - mid -right
            # -1.0 - 0.0 - 1.0
            if d.setStatus(uid, motor=0.0, servo=0.0):
                print "setStatus() failed."

        return 0
    except KeyboardInterrupt:
        return 0
    except Exception, e:
        print repr(e)
        return 1
               
    
if __name__ == '__main__':
    run_cybercar()

