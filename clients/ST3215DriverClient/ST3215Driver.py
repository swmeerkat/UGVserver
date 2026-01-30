#!/usr/bin/env python3
#
# max position value: 4095
# max speed value: 3400??
# max acceleration value: 150
#

import logging

from .STservo_sdk import *  # Uses ST Servo SDK library

SERVO_ID = 2  # Servo ID : 1 (tilt), 2 (pan)
BAUDRATE = 1000000  # Servo default baudrate : 1000000
DEVICE_NAME = '/dev/ttyACM0'


class ST3215Driver:

  def __init__(self):
    self.sts_id = SERVO_ID
    self.baudrate = BAUDRATE
    self.device_name = DEVICE_NAME
    self.portHandler = PortHandler(self.device_name)
    self.packetHandler = sts(self.portHandler)
    self.servo = sts(self.packetHandler)
    if self.portHandler.openPort():
      pass
    else:
      logging.log(COMM_NOT_AVAILABLE, "Open port failed")
    if self.portHandler.setBaudRate(self.baudrate):
      pass
    else:
      logging.log(COMM_NOT_AVAILABLE, "Change baudrate failed")
    pass

  def middle_position(self):
    # goto pan middle position
    self.servo.WritePosEx(1, 2048, 1000, 30)
    self.servo.WritePosEx(2, 2048, 1000, 30)
    pass

  def __exit__(self, exception_type, exception_value, exception_traceback):
    self.portHandler.closePort()
