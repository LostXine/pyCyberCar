#!/usr/bin/python
# -*- coding: utf-8 -*-

def getDefaultConst():
    const = {
            'port': 61551,

            'motor_fpin': 16,
            'motor_bpin': 20,
            'motor_level': [0.0, 70, 80, 90, 100],
            'motor_max': 100.0,
            'motor_feq': 200,

            'servo_pin': 21,
            'servo_left': 65.0,
            'servo_mid': 50,
            'servo_right': 35.0,
            'servo_feq': 300
            }
    return const

def getDefaultConfig():
    config = {
            'motor': 0.0,
            'servo' : 0.0
            }
    return config

if __name__=='__main__':
    print "----------Default Const Begin----------"
    print getDefaultConst()
    print "----------Default Const End----------"

    print "----------Default Config Begin----------"
    print getDefaultConfig()
    print "----------Default Config End----------"

