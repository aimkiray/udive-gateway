#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/4
# @Author  : aimkiray

import serial
import time

ser = serial.Serial("/dev/ttyUSB0", 115200)


def send_command():
    while True:
        recv = get_recv()
        if recv is not None:
            print(recv)
            ser.write(recv[0] + "\n")
        time.sleep(0.1)


def get_recv():
    cout = ser.inWaiting()
    if cout is not 0:
        line = ser.read(cout)
        recv = str.split(line)
        ser.reset_input_buffer()
        return recv
