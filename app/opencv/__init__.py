#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/4
# @Author  : aimkiray

from app.opencv.motion_detection import SingleMotionDetector
from imutils.video import VideoStream
import imutils
import datetime
import threading
import time
import cv2
import configparser

# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful when multiple browsers/tabs
# are viewing the stream)
outputFrame = None
lock = threading.Lock()

# initialize the video stream and allow the camera sensor to
# warmup
config = configparser.ConfigParser()
config.read('config.ini')
piCamera = config['DEFAULT']['PiCamera']
if piCamera == 'yes':
    vs = VideoStream(usePiCamera=1).start()
else:
    vs = VideoStream(src=0).start()
time.sleep(2.0)

# motionFlag = False
motionCount = 0
img_path = None


def detect_motion(frameCount):
    # grab global references to the video stream, output frame, and
    # lock variables
    global vs, outputFrame, lock, img_path, motionCount

    # initialize the motion detector and the total number of frames
    # read thus far
    md = SingleMotionDetector(accumWeight=0.1)
    total = 0

    # loop over frames from the video stream
    while True:
        # read the next frame from the video stream, resize it,
        # convert the frame to grayscale, and blur it
        frame = vs.read()
        image = frame
        frame = imutils.resize(frame, width=600)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        # grab the current timestamp and draw it on the frame
        timestamp = datetime.datetime.now()
        cv2.putText(frame, timestamp.strftime(
            "%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

        # if the total number of frames has reached a sufficient
        # number to construct a reasonable background model, then
        # continue to process the frame
        if total > frameCount:
            # detect motion in the image
            motion = md.detect(gray)

            # check to see if motion was found in the frame
            if motion is not None:
                motionCount += 1
                if motionCount > 999:
                    motion_path = config['DEFAULT']['MotionPath']
                    img_path = motion_path + timestamp.strftime("%A %d %B %Y %I:%M:%S%p") + '.jpg'
                    cv2.imwrite(img_path, image)
                    # motionFlag = True
                    motionCount = 0

                # unpack the tuple and draw the box surrounding the
                # "motion area" on the output frame
                (thresh, (minX, minY, maxX, maxY)) = motion
                cv2.rectangle(frame, (minX, minY), (maxX, maxY),
                              (0, 0, 255), 2)

        # update the background model and increment the total number
        # of frames read thus far
        md.update(gray)
        total += 1

        # acquire the lock, set the output frame, and release the
        # lock
        with lock:
            outputFrame = frame.copy()


def generate():
    # grab global references to the output frame and lock variables
    global outputFrame, lock

    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        with lock:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            if outputFrame is None:
                continue

            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

            # ensure the frame was successfully encoded
            if not flag:
                continue

        # yield the output frame in the byte format
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(encodedImage) + b'\r\n')


def get_path():
    global img_path
    return img_path


def reset_path():
    global img_path
    img_path = None
