#!/usr/bin/env python3
import requests
import json

class UgvEsp32:

  def __init__(self, ip="0.0.0.0"):
    self.ip = ip

  # Retrieve IMU data
  def get_imu_data(self):
    cmd = "{\"T\":130}"
    return self.do_get(cmd)

  # CMD_BASE_FEEDBACK
  def get_base_feedback(self):
    cmd = "{\"T\":126}"
    return self.do_get(cmd)

  def do_get(self, cmd):
    url = "http://" + self.ip + "/js?json=" + cmd
    print (url)
    response = requests.get(url)
    return json.dumps(response.json())