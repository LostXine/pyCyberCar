#!/usr/bin/python
# -*- coding: utf-8 -*-

def getDefaultConst():
    const = {
            'port': 61551,
            'motor_min': 0.0,
            'motor_max': 100.0,
            'servo_left': 40.0,
            'servo_right': 60.0
            }
    return const

def getDefaultConfig():
    config = {
            'motor': 0.0,
            'forward' : 1,
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

