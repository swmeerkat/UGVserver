#!/usr/bin/env python3
import requests
import json

class UgvEsp32:

  def __init__(self, ip="0.0.0.0"):
    self.ip = ip

  def get_imu_data(self):
    cmd = "{\"T\":130}"
    return self.do_GET(cmd)

  def do_get(self, cmd):
    url = "http://" + self.ip + "/js?json=" + cmd
    print (url)
    response = requests.get(url)
    return json.dumps(response.json())