#!/usr/bin/env python3

import json
import logging

from .STservo_sdk import *  # Uses ST Servo SDK library

TILT_SERVO_ID = 1
PAN_SERVO_ID = 2
BAUDRATE = 1000000  # Servo default baudrate : 1000000
DEVICE_NAME = '/dev/ttyTHS1'
MAX_SERVO_SPEED = 3400
DEF_SERVO_SPEED = 700
MAX_SERVO_ACC = 150
MAX_TILT = 2490
MIN_TILT = 965
MAX_TILT_STEP = 100  # + -> down, - -> up
MAX_PAN = 4095
MIN_PAN = 0
MAX_PAN_STEP = 1000  # + -> right, - -> left


class ST3215Driver:

  def __init__(self):
    self.baudrate = BAUDRATE
    self.device_name = DEVICE_NAME
    self.portHandler = PortHandler(self.device_name)
    self.servo = sts(self.portHandler)
    if self.portHandler.openPort():
      pass
    else:
      logging.log(COMM_NOT_AVAILABLE, "Open port failed")
    if self.portHandler.setBaudRate(self.baudrate):
      pass
    else:
      logging.log(COMM_NOT_AVAILABLE, "Change baudrate failed")
    pan_position = self.servo.ReadPos(PAN_SERVO_ID)
    tilt_position = self.servo.ReadPos(TILT_SERVO_ID)
    print("pan: " + str(pan_position) + " tilt: " + str(tilt_position))

  def middle_position(self):
    # goto gimbal middle position
    self.servo.WritePosEx(TILT_SERVO_ID, 2048, DEF_SERVO_SPEED, MAX_SERVO_ACC)
    self.servo.WritePosEx(PAN_SERVO_ID, 2048, DEF_SERVO_SPEED, MAX_SERVO_ACC)

  # data: {"pan": step, "tilt:": step}
  def do_gimbal_step(self, data):
    cmd = json.loads(data)
    pan_step = cmd["pan"]
    tilt_step = cmd["tilt"]
    if pan_step != 0: self.pan_step(pan_step)
    if tilt_step != 0: self.tilt_step(tilt_step)

  def pan_step(self, step):
    if step < -MAX_PAN_STEP:
      step = -MAX_PAN_STEP
    elif step > MAX_PAN_STEP:
      step = MAX_PAN_STEP
    position = self.servo.ReadPos(PAN_SERVO_ID)
    new_position = position[0] + step
    if new_position > MAX_PAN:
      new_position = MAX_PAN
    elif new_position < MIN_PAN:
      new_position = MIN_PAN
    print("pan position: " + str(position) + " new_position: " + str(new_position))
    self.servo.WritePosEx(PAN_SERVO_ID, new_position, DEF_SERVO_SPEED,
                          MAX_SERVO_ACC)

  def tilt_step(self, step):
    if step < -MAX_TILT_STEP:
      step = -MAX_TILT_STEP
    elif step > MAX_TILT_STEP:
      step = MAX_TILT_STEP
    position = self.servo.ReadPos(TILT_SERVO_ID)
    new_position = position[0] + step
    if new_position > MAX_TILT:
      new_position = MAX_TILT
    elif new_position < MIN_TILT:
      new_position = MIN_TILT
    print("tilt position: " + str(position) + " new_position: " + str(new_position))
    self.servo.WritePosEx(TILT_SERVO_ID, new_position, DEF_SERVO_SPEED,
                          MAX_SERVO_ACC)

  def __exit__(self, exception_type, exception_value, exception_traceback):
    self.portHandler.closePort()
    pass
