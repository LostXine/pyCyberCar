#!/usr/bin/python
# -*- coding: utf-8 -*-

from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from run_server import *


clients = []
class wbsocket(WebSocket):
    def handleMessage(self):
        server_log("Recv: %s from %s:%d" % (self.data, self.address[0], self.address[1]))
        # self.sendMessage(self.data)

    def handleConnected(self):
        server_log("%s:%d connected" % (self.address[0], self.address[1]))
        clients.append(self)

    def handleClose(self):
        clients.remove(self)
        server_log("%s:%d closed" % (self.address[0], self.address[1]))

def websocket_syn():
    server = SimpleWebSocketServer('', 8000, wbsocket)
    print "WebSocketServer Online"
    server.serveforever()

if __name__ == '__main__':
    websocket_syn()


