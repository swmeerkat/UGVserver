#!/usr/bin/env python3

import json
import logging

from .STservo_sdk import *  # Uses ST Servo SDK library

TILT_SERVO_ID = 1
PAN_SERVO_ID = 2
BAUDRATE = 1000000  # Servo default baudrate : 1000000
DEVICE_NAME = '/dev/ttyTHS1'
MAX_SERVO_SPEED = 3400
DEF_SERVO_SPEED = 2400
MAX_SERVO_ACC = 150
DEF_SERVO_ACC = 50
MAX_TILT = 2490
MIN_TILT = 1024
MAX_TILT_STEP = 100  # + -> down, - -> up
MAX_PAN = 4095
MIN_PAN = 0
MIDDLE_POSITION = 2048
MAX_PAN_STEP = 1000  # + -> right, - -> left


class ST3215Driver:

    def __init__(self):
        self.baudrate = BAUDRATE
        self.device_name = DEVICE_NAME
        self.portHandler = PortHandler(self.device_name)
        self.servo = sts(self.portHandler)
        if self.portHandler.openPort():
            # default baudrate
            pass
        else:
            logging.log(COMM_NOT_AVAILABLE, "Open port failed")
        time.sleep(1)
        self.middle_position()
        print("ST3215 Driver Initialized")
        # pan_position = self.servo.ReadPos(PAN_SERVO_ID)
        # tilt_position = self.servo.ReadPos(TILT_SERVO_ID)
        # print("pan: " + str(pan_position) + " tilt: " + str(tilt_position))

    def middle_position(self):
        # goto gimbal middle position
        self.goto_position(PAN_SERVO_ID, MIDDLE_POSITION)
        self.goto_position(TILT_SERVO_ID, MIDDLE_POSITION)

    def goto_position(self, servo_id, position):
        com_result, com_error = self.servo.WritePosEx(servo_id, position, DEF_SERVO_SPEED, DEF_SERVO_ACC)
        if com_result != COMM_SUCCESS:
            print("WritePosEx: %s" % self.servo.getTxRxResult(com_result))
        elif com_error != 0:
            print("WritePosEx: %s" % self.servo.getRxPacketError(com_error))
        while 1:
            present_position, present_speed, com_result, com_error = self.servo.ReadPosSpeed(servo_id)
            if com_result != COMM_SUCCESS:
                print("ReadPosSpeed: %s" % self.servo.getTxRxResult(com_result))
            else:
                print(
                    "ID:%03d GoalPos:%d PresPos:%d PresSpd:%d" % (servo_id, position, present_position, present_speed))
            if com_error != 0:
                print("ReadPosSpeed: %s" % self.servo.getRxPacketError(com_error))
            moving, com_result, com_error = self.servo.ReadMoving(servo_id)
            if com_result != COMM_SUCCESS:
                print("ReadPosSpeed: %s" % self.servo.getTxRxResult(com_result))
            if moving == 0:
                break

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
        self.goto_position(PAN_SERVO_ID, new_position)

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
        self.goto_position(TILT_SERVO_ID, new_position)

    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.portHandler.closePort()
        pass
