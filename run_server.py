#!/usr/bin/python
# -*- coding: utf-8 -*-

from config import *
from driver import controller
import socket, json, sys, time
import threading


dt = 0

def server_log(info):
    print "%s %s" % (time.strftime('%H:%M:%S', time.localtime(time.time())), info)

def watchdog(c, const):
    global dt
    has_stop = False
    while True:
        if time.time() - dt > const['dog']:
            if not has_stop:
                server_log('STOP')
                c.emergency()
                has_stop = True
        elif has_stop:
            # dog refeed
            has_stop = False
        time.sleep(1)



def run_server():
    print "----------Server Init----------"
    
    # set watchdog
    global dt
    dt = time.time()
    print "Start at %s" % time.asctime(time.localtime(dt))

    # check debug mode
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
        # setup watchdog
        t = threading.Thread(target=watchdog, args=(c, const,))
        t.setDaemon(True)
        t.start()

        sender = None
        while True:
            res = sock.recvfrom(1024)
            if debug:
                server_log("recv: %s, from: %s" % (res[0], res[1][0], res[1][1]))
            if sender != res[1]:
                sender = res[1]
                server_log("Sender changed to: %s:%d" % res[1])
            if c.parse(res[0]):
                server_log("Unknown cmd: %s" % res[0])
            else:
                # feed the watchdog
                dt = time.time()
    except KeyboardInterrupt:
        return 0
    except Exception, e:
        print repr(e)
        return 2
    finally:
        del t
        sock.close()
        del c
        print "\n----------Server End----------"

if __name__=='__main__':
    print "----------Cyber Car Server----------"
    run_server()
    print "------------------------------"

