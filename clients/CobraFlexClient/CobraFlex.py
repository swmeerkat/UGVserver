#!/usr/bin/env python3
import logging
import time

import serial


class CobraFlex:

    def __init__(self):
        self.serial_port = serial.Serial(
            port="/dev/ttyACM2",
            baudrate=115200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE
        )
        time.sleep(1)
        print("CobraFlex driver initialized")

    def read(self):
        try:
            self.serial_port.reset_input_buffer()
            response = ' '
            while response[0] != "{":
                response = self.serial_port.readline().strip().decode("utf-8")
            return response
        except Exception as exception_error:
            logging.error("ESP32 communication error: " + str(exception_error))
        finally:
            pass

    def write(self, data):
        try:
            self.serial_port.write(bytes(data + "\r\n", "utf-8"))
        except Exception as exception_error:
            logging.error("ESP32 communication error: " + str(exception_error))
        finally:
            pass

    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.serial_port.flush()
        self.serial_port.reset_input_buffer()
        self.serial_port.reset_output_buffer()
        self.serial_port.close()
