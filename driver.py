#!/usr/bin/python
# -*- coding: utf-8 -*-

from config import *
import threading
import socket, json, time , atexit
import RPi.GPIO as GPIO
import traceback


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
        except:
            traceback.print_exc() 
            print "Controller Init Error"
            return 
        print "Controller Init Done"

    def __del__(self):
        self.__motorb.stop()
        self.__motorf.stop()
        self.__setServo(0)
        self.__servop.stop()
        print "\nController End"

    def __setServo(self, ratio):
        # normalize ratio to [-1, 1]
        s = -min(max(float(ratio), -1), 1)
        mid = self.__const['servo_mid']
        dc = mid
        if s < 0:
            dc = mid + (mid - self.__const['servo_right']) * s
        else:
            dc = mid + (self.__const['servo_left'] - mid) * s
        # set servo
        self.__servop.ChangeDutyCycle(dc)
    
    def __setMotor(self, speed):
        # print speed
        forward = (speed >= 0)
        s = min(max(float(abs(speed)), 0), self.__const['motor_max']) * 100
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
            if not obj.has_key('uid'):
                print "Uid is needed."
                return 2
            elif self.__conf['uid'] > obj['uid']:
                print "uid %0.3f is behind %0.3f, drop %s" % (obj['uid'], self.__conf['uid'], js)
                return 3
            else:
                self.__conf['uid'] = float(obj['uid'])
            if obj.has_key('servo'):
                self.__setServo(obj['servo'])
            if obj.has_key('motor'):
                self.__setMotor(obj['motor'])
            return 0
        except:
            traceback.print_exc() 
            return 1

    def reset(self):
        self.parse(self.__conf)

    def emergency(self):
        self.__motorf.ChangeDutyCycle(0)
        self.__motorb.ChangeDutyCycle(0)


class driver:
    __conf = None
    __const = None
    __sock = None
    __dst = None
    __mutex = threading.Lock()
    
    def __init__(self):
        print "----------Driver No.%d Init----------" % id(self)
        try: 
            self.__const = getDefaultConst()
            self.__conf = getDefaultConfig()
            self.__dst = ('127.0.0.1', self.__const['port'])

            self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except:
            traceback.print_exc() 
            print "----------Driver Init Failed----------"
            return
        print "----------Driver Init Done----------"

    def __del__(self):
        print "\n----------Driver No.%d End----------" % id(self)

    def __launch(self):
        self.__sock.sendto(json.dumps(self.__conf), self.__dst)
    
    def __setMotor(self, motor):
        # motor: from -1 to 1
        self.__conf['motor'] = round(max(min(motor, 1), -1), 3)
    
    def __setSpeed(self, speed, forward=1):
        # speed level depends on motor_level
        num = len(self.__const['motor_level'])
        sp = max(min(num-1, int(speed)), 0)
        sp = self.__const['motor_level'][sp]
        if not forward:
            sp = -sp
        self.__setMotor(sp)

    def __setServo(self, steer):
        # steer: from -1 to 1
        self.__conf['servo'] = round(max(min(steer, 1), -1), 3)

    def setStatus(self,uid , **dt):
        if self.__mutex.acquire(1):
            self.__conf['uid'] = round(uid, 3)
            if dt.has_key('speed'):
                self.__setSpeed(dt['speed'])
            if dt.has_key('motor'):
                self.__setMotor(dt['motor'])
            if dt.has_key('servo'):
                self.__setServo(dt['servo'])
            self.__launch()
            self.__mutex.release()
            return 0
        else:
            return 1
        

if __name__=='__main__':
    print "----------Cyber Car Driver----------"
    print "Usage: import driver.py and using driver() to start."
    print "------------------------------"

