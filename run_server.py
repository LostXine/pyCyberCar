#!/usr/bin/python
# -*- coding: utf-8 -*-

from config import *
from driver import controller
import socket, json, sys


def run_server():
    print "----------Server Init----------"
    debug = False
    if len(sys.argv) > 1 and sys.argv[1] == '-d':

        print "**********DEBUG MODE**********"
        debug = True
    try:
        # load config
        const = getDefaultConst()
        conf = getDefaultConfig()
        # setup controller
        c = controller()
        # listening udp
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('127.0.0.1', const['port']))
        print "Listenning port:%d" % const['port']
    except Exception, e:
        print repr(e)
        print "----------Server Init Failed----------"
        return 1
    print "----------Server Init Done----------"
    try:
        sender = None
        while True:
            res = sock.recvfrom(1024)
            if debug:
                print "recv: %s, from: %s" % res
            if sender != res[1]:
                sender = res[1]
                print "Sender changed to: %s:%d" % res[1]
            if c.parse(res[0]):
                print "Unknown cmd: %s" % res[0]
    except KeyboardInterrupt:
        return 0
    except Exception, e:
        print repr(e)
        return 2
    finally:
        sock.close()
        del c
        print "\n----------Server End----------"

if __name__=='__main__':
    print "----------Cyber Car Server----------"
    run_server()
    print "------------------------------"

