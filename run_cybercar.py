#!/usr/bin/python
# -*- coding: utf-8 -*-

from config import *
from driver import driver
from dip import *
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2, sys, multiprocessing

d = None

def frame_loop(image):
    global d
    return d.process_image(image)

def run_cybercar():
    print "==========CyberCar Start=========="
    const = getDefaultConst()
    # init picamera
    c = PiCamera()
    c.resolution = (640, 480)
    c.framerate = 30
    # prepare memery
    raw = PiRGBArray(c, c.resolution)

    # check multiprocess mode
    mp = False
    for i in sys.argv:
        if i == '-mp':
            print "**********MULTI MODE**********"
            mp = True
    # init car driver
    global d
    d = dip()
    # set process pool
    if mp:
        pool = multiprocessing.Pool(processes=const['processor'])
        result = []
    try:
        for frame in c.capture_continuous(raw, format='bgr', use_video_port=True):
            image = frame.array
            res = 0
            if mp:
                if len(result) >= const['processor']:
                    res = result[0].get()
                    del result[0]
                result.append(pool.apply_async(frame_loop, [image]))
            else:
                res = frame_loop(image)
            if res:
                break
            # reset
            raw.truncate(0)
    except KeyboardInterrupt:
        pass
    if mp:
        pool.close()
        pool.join()
    return 0
               
    
if __name__ == '__main__':
    run_cybercar()

