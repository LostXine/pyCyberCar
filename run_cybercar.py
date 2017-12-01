#!/usr/bin/python
# -*- coding: utf-8 -*-

from driver import driver
from image_process import *
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2

def run_cybercar():
    print "==========CyberCar Start=========="
    # init picamera
    c = PiCamera()
    c.resolution = (640, 480)
    c.framerate = 30
    # prepare memery
    raw = PiRGBArray(c, c.resolution)
    # init car driver
    d = dip()
    try:
        for frame in c.capture_continuous(raw, format='bgr', use_video_port=True):
            image = frame.array
            if d.process_image(image):
                break;
            # reset
            raw.truncate(0)
    except KeyboardInterrupt:
        pass
    except Exception, e:
        print repr(e)
        return 1
    return 0
               
    
if __name__ == '__main__':
    run_cybercar()

