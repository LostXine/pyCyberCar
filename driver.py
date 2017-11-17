#!/usr/bin/python
# -*- coding: utf-8 -*-

from config import *
import socket, json, time, atexit
import RPi.GPIO as GPIO

class controller:
    __conf = None
    __const = None

    __motorf = None
    __motorb = None
    __servop = None

    def __init__(self):
        print "Controller Init"
        try: 
            # load config
            self.__const = getDefaultConst()
            self.__conf = getDefaultConfig()
            # enable gpio
            atexit.register(GPIO.cleanup)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.__const['motor_fpin'], GPIO.OUT, initial=False)
            GPIO.setup(self.__const['motor_bpin'], GPIO.OUT, initial=False)
            GPIO.setup(self.__const['servo_pin'], GPIO.OUT, initial=False)
            self.__motorb = GPIO.PWM(self.__const['motor_fpin'], self.__const['motor_feq'])

            self.__motorf = GPIO.PWM(self.__const['motor_bpin'], self.__const['motor_feq'])
            self.__servop = GPIO.PWM(self.__const['servo_pin'], self.__const['servo_feq'])
            self.__motorb.start(0)
            self.__motorf.start(0)
            self.__servop.start(self.__const['servo_mid'])
        finally:
            "Controller Init Error"
        print "Controller Init Done"

    def __del__(self):
        self.__motorb.stop()
        self.__motorf.stop()
        self.__servop.stop()
        print "Controller End"

    def __setServo(self, ratio):
        # normalize ratio to [-1, 1]
        s = min(max(float(ratio), -1), 1)
        mid = self.__const['servo_mid']
        dc = mid
        if s < 0:
            dc = mid + (mid - self.__const['servo_left']) * s
        else:
            dc = mid + (self.__const['servo_right'] - mid) * s
        # set servo
        self.__servop.ChangeDutyCycle(dc)
    
    def __setMotor(self, speed):
        forward = (speed >= 0)
        s = min(max(float(abs(speed)), self.__const['motor_min']), self.__const['motor_max'])
        if forward:
            self.__motorb.ChangeDutyCycle(0)
            self.__motorf.ChangeDutyCycle(s)
        else:
            self.__motorf.ChangeDutyCycle(0)
            self.__motorb.ChangeDutyCycle(s)


    def parse(self, js):
        try:
            obj = json.loads(js)
            # parse servo
            if obj.has_key('servo'):
                self.__setServo(obj['servo'])
            if obj.has_key('motor'):
                self.__setMotor(obj['motor'])
            return 0
        except Exception, e:
            print repr(e)
            return 1

    def reset(self):
        self.parse(self.__conf)

    def emergency(self):
        self.__motorf.ChangeDutyCycle(0)
        self.__motorb.ChangeDutyCycle(0)
        print "Emergency Stop"



class driver:
    __conf = None
    __const = None
    __sock = None
    __dst = None

    def __init__(self):
        print "----------Driver No.%d Init----------" % id(self)
        try: 
            self.__const = getDefaultConst()
            self.__conf = getDefaultConfig()
            self.__dst = ('127.0.0.1', self.__const['port'])

            self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        finally:
            print "----------Driver Init Failed----------"
        print "----------Driver Init Done----------"

    def __del__(self):
        print "----------Driver No.%d End----------" % id(self)

    def reset(self):
        if self.__sock is not None:
            self.__sock.sendto(json.dumps(self.__conf), self.__dst)
        else:
            print "Driver's sock is empty."

        

if __name__=='__main__':
    print "----------Cyber Car Driver----------"
    print "Usage: import driver.py and using driver() to start."
    print "------------------------------"

