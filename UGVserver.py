#!/usr/bin/env python3
import subprocess
from functools import cached_property
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse

from clients.CobraFlexClient import CobraFlex
from clients.ST3215DriverClient import ST3215Driver


def gimbal_cam_on():
    command = "./scripts/start_gimbal_cam.sh"
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return process.stdout.decode("utf-8").strip()


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
            case "/cobraflex/feedback":
                response = CobraFlex.read()
            case _:
                response = "{ \"error\": \"unknown command: " + self.path + "\"}"
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(response.encode("utf-8"))

    def do_POST(self):
        response = "{}"
        match self.url.path:
            case "/cobraflex/cmd":
                CobraFlex.write(self.post_data.decode("utf-8"))
            case "/gimbal/middle_position":
                ST3215Driver.middle_position()
            case "/gimbal/step":
                ST3215Driver.do_gimbal_step(self.post_data.decode("utf-8"))
            case "/gimbal/camera/on":
                pid = gimbal_cam_on()
                response = "{ \"gimbal_pid\": \"" + str(pid) + "\"}"
            case _:
                response = "{ \"error\": \"unknown command: " + self.path + "\"}"
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(response.encode("utf-8"))


if __name__ == "__main__":
    CobraFlex = CobraFlex.CobraFlex()
    ST3215Driver = ST3215Driver.ST3215Driver()
    ugvServer = HTTPServer(("0.0.0.0", 8000), UGVserver)
    print("UGV server started at http://0.0.0.0:8000")
    try:
        ugvServer.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        ugvServer.server_close()
        print("UGV server stopped")
