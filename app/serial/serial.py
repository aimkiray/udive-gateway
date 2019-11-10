#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/4
# @Author  : aimkiray

# import serial
# import time
#
# ser = serial.Serial("/dev/ttyUSB0", 115200)
#
#
# def send_command(command):
#     ser.write(command + "\n")
#
#
# def get_recv():
#     cout = ser.inWaiting()
#     if cout is not 0:
#         line = ser.read(cout)
#         recv = str.split(line)
#         ser.reset_input_buffer()
#         return recv
