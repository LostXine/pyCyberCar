#!/usr/bin/python
# -*- coding: utf-8 -*-

from config import *
from driver import controller
from websocket import *
import socket, json, sys, time, datetime
import threading
import traceback


dt = 0

def server_log(info):
    print "%s %s" % (datetime.datetime.now().strftime('%M:%S.%f'), info)

def websock_loop(wb):
    while dt >= 0:
        wb.serveonce()
    wb.close()

def watchdog(c, const):
    global dt
    global clients
    has_stop = False
    while dt >= 0:
        if time.time() - dt > const['dog']:
            if not has_stop:
                server_log('STOP')
                c.emergency()
                has_stop = True
        elif has_stop:
            # dog refeed
            has_stop = False
        # update web socket info
        for client in clients:
            client.sendMessage(unicode(c.getStatus()))
        time.sleep(0.1)

def run_server():
    print "----------Server Init----------"
    
    # set watchdog
    global dt
    dt = time.time()
    print "Start at %s" % time.asctime(time.localtime(dt))

    # check debug mode
    debug = False
    for i in sys.argv:
        if i == '-d':
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
        # setup web socket
        wbs = SimpleWebSocketServer('', 8000, wbsocket)
        wb = threading.Thread(target=websock_loop, args=(wbs,))
        wb.start()
    except:
        traceback.print_exc() 
        print "----------Server Init Failed----------"
        return 1
    print "----------Server Init Done----------"
    try:
        # setup watchdog
        t = threading.Thread(target=watchdog, args=(c, const,))
        t.start()

        sender = None
        while True:
            res = sock.recvfrom(1024)
            if debug:
                server_log("recv: %s, from: %s:%d" % (res[0], res[1][0], res[1][1]))
            if sender != res[1]:
                sender = res[1]
                server_log("Sender changed to: %s:%d" % res[1])
            if c.parse(res[0]):
                server_log("Error cmd: %s" % res[0])
            else:
                # feed the watchdog
                dt = time.time()
    except KeyboardInterrupt:
        pass
    except : 
        traceback.print_exc()
    # clean watchdog 
    dt = -1
    t.join()
    # clean web socket
    wb.join()
    # release udp port
    sock.close()
    # close car
    del c
    print "----------Server End----------"

if __name__=='__main__':
    print "----------Cyber Car Server----------"
    run_server()
    print "------------------------------"

