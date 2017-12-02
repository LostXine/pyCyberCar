#!/usr/bin/python
# -*- coding: utf-8 -*-

from config import *
from driver import driver
from dip import *
import cv2, sys, multiprocessing, time

d = None

def frame_loop(image):
    global d
    return d.process_image(image)

def run_cybercar():
    print "==========CyberCar Start=========="
    const = getDefaultConst()

    # check multiprocess mode
    mp = False
    fps = False
    for i in sys.argv:
        if i == '-mp' or i == '-m':
            print "**********MULTI MODE**********"
            mp = True
        if i == '-fps' or i == '-f':
            fps = True
    # init camera
    cc = cv2.VideoCapture(0)
    # set width and height
    cc.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, const['cam_width'])
    cc.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, const['cam_height'])
    cc.set(cv2.cv.CV_CAP_PROP_FPS, const['cam_fps'])
    # init car driver
    global d
    d = dip()
    # set process pool
    if mp:
        pool = multiprocessing.Pool(processes=const['processor'])
        result = []
    # setup fps counter
    if fps:
        c_frame = 0
        c_time = [time.time()]
    try:
        ret = cc.read()
        while ret:
            ret, image = cc.read()
            res = {}
            if mp:
                if len(result) >= const['processor']:
                    res = result[0].get()
                    del result[0]                    
                result.append(pool.apply_async(frame_loop, [image]))
            else:
                res = frame_loop(image)
            if fps:
                # calculate fps
                c_time.append(time.time())
                if c_frame < 20:
                    c_frame += 1
                else:
                    del c_time[0]
                c_fps = c_frame/ (c_time[-1] - c_time[0])
                f = sys.stdout
                f.write("Current fps: %.2f" % c_fps)
                f.flush()
                f.write('\r')
                res['fps'] = c_fps
            
            res['image'] = image
            # draw results
            if d.gui(res):
                break
        else:
            print "Capture failed."
    except KeyboardInterrupt:
        pass
    if mp:
        pool.close()
        pool.join()
    cc.release()
    cv2.destroyAllWindows()
    return 0
               
    
if __name__ == '__main__':
    print "Usage: python runcybercar.py [-f] [-mp]"
    print "-f : show fps\n-mp: use multi-processing"
    run_cybercar()

