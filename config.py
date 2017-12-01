#!/usr/bin/python
# -*- coding: utf-8 -*-

def getDefaultConst():
    const = {
            'port': 61551,
            'dog': 3,
            'processor': 4,

            'motor_fpin': 16,
            'motor_bpin': 20,
            'motor_level': [0, 0.7, 0.8, 0.9, 0.95, 1.0],
            'motor_max': 1.0,
            'motor_feq': 200,

            'servo_pin': 21,
            'servo_left': 65.0,
            'servo_mid': 48,
            'servo_right': 35.0,
            'servo_feq': 300
            }
    return const

def getDefaultConfig():
    config = {
            'uid': 0.0,
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

