#!/bin/bash
# some examples https://gstreamer.freedesktop.org/documentation/tools/gst-launch.html
gst-launch-1.0 nvarguscamerasrc sensor-id=0 ! \
 'video/x-raw(memory:NVMM), width=3280, height=2464, framerate=21/1, format=NV12' ! \
 nvvidconv flip-method=2 ! \
 x264enc tune=zerolatency bitrate=8000 speed-preset=superfast ! \
 rtph264pay pt=96 ! \
 udpsink host=192.168.178.24 port=5000 sync=false -e