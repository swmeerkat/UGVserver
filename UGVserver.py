#!/usr/bin/env python3
import Ups3sIna219
from functools import cached_property
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse


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
    response = "{}"
    match self.url.path:
      case "/ugv_power_status":
        response = ups3s.get_power_status()
      case _:
        response = "{ \"error\": \"unknown command: " + self.path  + "\"}"
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
  ugvServer = HTTPServer(("0.0.0.0", 8000), UGVserver)
  ugvServer.serve_forever()
