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
from flask import current_app


class CV:

    def __init__(self):
        # default args
        # initialize the output frame and a lock used to ensure thread-safe
        # exchanges of the output frames (useful when multiple browsers/tabs
        # are viewing the stream)
        self.lock = threading.Lock()
        self.output_frame = None
        self.vs = None
        self.motion_count = 0
        self.img_path = None
        self.motion_path = "app/static/motion/"
        self.pi_camera = 1

    def detect_motion(self, frame_count):
        # initialize the motion detector and the total number of frames
        # read thus far
        md = SingleMotionDetector(accumWeight=0.1)
        total = 0

        # initialize the video stream and allow the camera sensor to warmup
        if self.pi_camera == 1:
            self.vs = VideoStream(usePiCamera=1).start()
        else:
            self.vs = VideoStream(src=0).start()

        # time.sleep(2.0)

        # loop over frames from the video stream
        while True:
            # read the next frame from the video stream, resize it,
            # convert the frame to grayscale, and blur it
            frame = self.vs.read()
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
            if total > frame_count:
                # detect motion in the image
                motion = md.detect(gray)

                # check to see if motion was found in the frame
                if motion is not None:
                    self.motion_count += 1
                    if self.motion_count > 999:
                        self.img_path = self.motion_path + timestamp.strftime("%A %d %B %Y %I:%M:%S%p") + '.jpg'
                        cv2.imwrite(self.img_path, image)
                        # motionFlag = True
                        self.motion_count = 0

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
            with self.lock:
                self.output_frame = frame.copy()

    def generate(self):
        # loop over frames from the output stream
        while True:
            # wait until the lock is acquired
            with self.lock:
                # check if the output frame is available, otherwise skip
                # the iteration of the loop
                if self.output_frame is None:
                    continue

                # encode the frame in JPEG format
                (flag, encodedImage) = cv2.imencode(".jpg", self.output_frame)

                # ensure the frame was successfully encoded
                if not flag:
                    continue

            # yield the output frame in the byte format
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                   bytearray(encodedImage) + b'\r\n')

    def get_path(self):
        return self.img_path

    def reset_path(self):
        self.img_path = None

    def stop(self):
        self.vs.stop()


class OpenCV:
    def __init__(self, app=None):
        self.cv = CV()
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.cv.pi_camera = app.config.get("PI_CAMERA")
        self.cv.motion_path = app.config.get("MOTION_PHOTOS_DEST")

    def generate(self):
        self.cv.generate()

    def get_path(self):
        self.cv.get_path()

    def reset_path(self):
        self.cv.reset_path()

    def detect_motion(self, frame_count):
        self.cv.detect_motion(frame_count)

    def stop(self):
        self.cv.stop()
