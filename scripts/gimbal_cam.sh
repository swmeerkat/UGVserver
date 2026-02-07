#!/bin/bash
# some examples https://gstreamer.freedesktop.org/documentation/tools/gst-launch.html

# Argus camera
#gst-launch-1.0 nvarguscamerasrc sensor-id=0 ! \
#  'video/x-raw(memory:NVMM), width=3280, height=2464, framerate=21/1, format=NV12' ! \
#  nvvidconv flip-method=2 ! \
#  x264enc tune=zerolatency bitrate=8000 speed-preset=superfast ! \
#  rtph264pay pt=96 ! \
#  udpsink host=192.168.178.24 port=5000 sync=false -e

# USB camera
gst-launch-1.0 v4l2src device=/dev/video0 ! 'video/x-raw, width=1280, height=720' ! \
  nvvidconv ! x264enc tune=zerolatency speed-preset=fast ! \
  rtph264pay pt=96 ! udpsink host=192.168.178.24 port=5000 sync=false -e

# Test
#gst-launch-1.0 -v videotestsrc pattern=smpte100 ! 'video/x-raw, width=1280, height=720, framerate=10/1' ! \
#  nvvidconv ! \
#  x264enc tune=zerolatency speed-preset=fast ! \
#  rtph264pay pt=96 ! udpsink host=192.168.178.24 port=5000 sync=false -e