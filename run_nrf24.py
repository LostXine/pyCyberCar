#!/usr/bin/python
# -*- coding: utf-8 -*-
# raspberry pi nrf24l01 hub
# more details at http://blog.riyas.org
# Credits to python port of nrf24l01, Joao Paulo Barrac & maniacbugs original c library

from nrf24 import NRF24
import time
import os,  sys, threading
from driver import driver
import traceback

byteNum = 0

def rerun_nrf24():
    py = sys.executable
    os.execl(py, py, *sys.argv)

def cal_unit(byte):
    unitList = ["B","kB","MB","GB"]
    num = len(unitList)
    unit = 0
    while unit < num and byte > 768:
        unit += 1
        byte /= 1024 
    return (byte, unitList[unit])

def cal_speed():
    global byteNum
    timeInv = 0.5
    while byteNum >= 0:
        speed = byteNum / timeInv
        byteNum = 0      
        f = sys.stdout
        f.write("Current speed: %.2f %s/s" % cal_unit(speed))
        f.flush()
        time.sleep(timeInv)
        f.write('\r')

def parse_check(info):
    s = 0;
    for t in range(0, 30):
        s += info[t]
    return info[30] == s&0xff and info[31] == (s>>8)& 0xff

def parse_num(bits):
    return bits[0] + (bits[1]<<8)

def parse_nrf(info, driver):
    try:
        if not parse_check(info):
            print "Check sum failed."
            return 2
        #print "Left:%d %d, YAW:%d %d, PIT:%d %d, ROW:%d %d" %\
        #        tuple(info[2:10])
        #print "Mask: %d, Thro: %d, STEER: %d" \
        #       % (parse_num(info[2:4]), parse_num(info[6:8]), parse_num(info[8:10]))
        motor_value = float(parse_num(info[2:4]))/1024
        # 0.0 - 1.0
        if abs(motor_value) < 0.05:
            motor_value = 0
        servo_value = (float(parse_num(info[8:10]))/1024 - 0.5) * 2 
        driver.setStatus(time.time(), servo=servo_value, motor=motor_value /2)
    except:
        traceback.print_exc() 
        return 1
    else:
        return 0

def run_nrf24():
    d = driver()
    pipes = [0xf0, 0xf0, 0xf0, 0xf0, 0xe1]
    print "----------------NRF24 Init-----------------"
    radio = NRF24()
    radio.begin(0, 0,25,18) #set gpio 25 as CE pin
    
    radio.setPayloadSize(32)
    radio.setChannel(40)
    radio.setDataRate(NRF24.BR_250KBPS)
    radio.setAutoAck(0)
    radio.openWritingPipe(pipes)
    radio.openReadingPipe(0, pipes)

    radio.printDetails()
    print "----------------NRF24 Start-----------------"
    # check debug mode
    debug = False
    restart = False
    for i in sys.argv:
        if i == '-d':
            print "**********DEBUG MODE**********"
            debug = True
    radio.startListening()
    if not debug:
        t = threading.Thread(target=cal_speed)
        t.start()
    try:
        ct = 0
        while True:
            while not radio.available(pipes, True):
                time.sleep(1000/1000000.0)
            recv_buffer = []
            radio.read(recv_buffer)
            byteNum += len(recv_buffer)
            if debug:
                print recv_buffer
            ct += 1
            if ct > 1:
                ct = 0
                if parse_nrf(recv_buffer, d):
                    restart = True
                    break
    except KeyboardInterrupt:
        pass
    except:
        traceback.print_exc()
        print "\n----------------NRF24 Interrupted-----------------"
    if not debug:
        byteNum = -1
        t.join()
    radio.stopListening()
    radio.end()
    del d
    print "----------------NRF24 Ended-----------------"
    if restart:
        rerun_nrf24()

if __name__=='__main__':
    run_nrf24()
