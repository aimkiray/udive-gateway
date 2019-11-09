#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/4
# @Author  : aimkiray

from app import create_app
from app.opencv import detect_motion, vs
from app.serial.zigbee import ser
import argparse
import threading
# from gevent.pywsgi import WSGIServer


if __name__ == '__main__':
    app = create_app()

    # construct the argument parser and parse command line arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--host", type=str, required=True,
                    help="ip address of the device")
    ap.add_argument("-o", "--port", type=int, required=True,
                    help="ephemeral port number of the server (1024 to 65535)")
    ap.add_argument("-f", "--frame-count", type=int, default=32,
                    help="# of frames used to construct the background model")
    args = vars(ap.parse_args())

    # start a thread that will perform motion detection
    t = threading.Thread(target=detect_motion, args=(
        args["frame_count"],))
    t.daemon = True
    t.start()

    # start the flask app
    app.run(host=args["host"], port=args["port"], debug=True,
            threaded=True, use_reloader=False)

    # http_server = WSGIServer(('0.0.0.0', 404), app)
    # http_server.serve_forever()


# release the video stream pointer & serial
vs.stop()
ser.close()
