#!/usr/bin/python
# -*- coding: utf-8 -*-

from config import *
import socket, json


def run_server():
    print "----------Server Init----------"
    try:
        # load config
        const = getDefaultConst()
        conf = getDefaultConfig()
        # listening udp
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('127.0.0.1', const['port']))
    except Exception, e:
        print repr(e)
        print "----------Server Init Failed----------"
        return 1
    print "----------Server Init Done----------"
    try:
        while True:
            res = sock.recvfrom(1024)
            print "recv: %s, from: %s" % res
    except KeyboardInterrupt:
        return 0
    except Exception, e:
        return 2
    finally:
        sock.close()
        print "\n----------Server End----------"

if __name__=='__main__':
    print "----------Cyber Car Server----------"
    run_server()
    print "------------------------------"

