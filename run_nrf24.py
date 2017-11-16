#!/usr/bin/python
# raspberry pi nrf24l01 hub
# more details at http://blog.riyas.org
# Credits to python port of nrf24l01, Joao Paulo Barrac & maniacbugs original c library

from nrf24 import NRF24
import time
from time import gmtime, strftime


pipes = [0xf0, 0xf0, 0xf0, 0xf0, 0xe1]

def run_nrf24():
    print "----------------NRF24 Init-----------------"
    radio = NRF24()
    radio.begin(0, 0,25,18) #set gpio 25 as CE pin
    
    radio.setPayloadSize(32)
    radio.setChannel(40)
    radio.setDataRate(NRF24.BR_250KBPS)
    radio.setAutoAck(0)
    radio.openReadingPipe(0, pipes)
    radio.printDetails()
    
    print "----------------NRF24 Start-----------------"
    radio.startListening()
    try:
        while True:
            while not radio.available(pipes, True):
                time.sleep(1000/1000000.0)
            recv_buffer = []
            radio.read(recv_buffer)
    except:
        pass
    finally:
        print "----------------NRF24 Interrupted-----------------"
        radio.stopListening()
        radio.end()
        print "----------------NRF24 Ended-----------------"

if __name__=='__main__':
    run_nrf24()
