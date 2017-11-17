#!/usr/bin/python
# -*- coding: utf-8 -*-

from config import *
import socket, json

class driver:
    __conf = None
    __const = None
    __sock = None
    __dst = None

    def __init__(self):
        print "----------Driver Init----------"
        try: 
            self.__const = getDefaultConst()
            self.__conf = getDefaultConfig()
            self.__dst = ('127.0.0.1', self.__const['port'])

            self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        finally:
            print "----------Driver Init Failed----------"
        print "----------Driver Init Done----------"

    def __del__(self):
        print "----------Driver End----------"

    def launch(self):
        self.__sock.sendto(json.dumps(self.__conf), self.__dst)

        

if __name__=='__main__':
    print "----------Cyber Car Driver----------"
    print "Usage: import driver.py and using driver() to start."
    print "------------------------------"

