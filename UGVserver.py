#!/usr/bin/env python3
import Ups3sIna219
import UgvEsp32
from functools import cached_property
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse

# UGV02 ESP32 client address
UGVhost = "192.168.178.29"


class UGVserver(BaseHTTPRequestHandler):
  @cached_property
  def url(self):
    return urlparse(self.path)

  @cached_property
  def query_data(self):
    return dict(parse_qsl(self.url.query))

  @cached_property
  def post_data(self):
    content_length = int(self.headers.get("Content-Length", 0))
    return self.rfile.read(content_length)

  @cached_property
  def form_data(self):
    return dict(parse_qsl(self.post_data.decode("utf-8")))

  def do_GET(self):
    response = ""
    match self.url.path:
      case "/ugv_power_status":
        response = ups3s.get_power_status()
      case "/ugv_imu_data":
        response = ugvClient.get_imu_data()
      case "/ugv_base_feedback":
        response = ugvClient.get_base_feedback()
      case "/ugv_new_middle_position":
        response = ugvClient.new_middle_position()
      case _:
        response = "{}"
    self.send_response(200)
    self.send_header("Content-Type", "application/json")
    self.end_headers()
    self.wfile.write(response.encode("utf-8"))

  def do_POST(self):
    response = ""
    match self.url.path:
      case _:
        response = "{}"
    self.send_response(200)
    self.send_header("Content-Type", "application/json")
    self.end_headers()
    self.wfile.write(response.encode("utf-8"))


if __name__ == "__main__":
  ups3s = Ups3sIna219.Ups3sIna219()
  ugvClient = UgvEsp32.UgvEsp32(UGVhost)
  ugvClient.gimbal_ctrl_simple(0, 0)
  ugvServer = HTTPServer(("0.0.0.0", 8000), UGVserver)
  ugvServer.serve_forever()
