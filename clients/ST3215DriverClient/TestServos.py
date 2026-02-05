#!/usr/bin/env python
#
# See also
# * https://www.waveshare.com/wiki/Bus_Servo_Adapter_(A)
# * https://files.waveshare.com/wiki/Bus_Servo_Adapter_A/STServo_Python.zip

import sys
import termios
import tty

fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)


def getch():
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


sys.path.append("STservo_sdk")
from STservo_sdk import *  # Uses ST Servo SDK library

# Settings
SERVO_ID = 2  # 1 (tilt), 2 (pan)
BAUDRATE = 1000000  # Servo default baudrate : 1000000
DEVICE_NAME = '/dev/ttyACM0'
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
TARGET_POSITION = 1500

# Initialize packetHandler
portHandler = PortHandler(DEVICE_NAME)
servo = sts(portHandler)
# Use default baudrate
if portHandler.openPort():
    print("Port opened")
else:
    print("Open port failed")
    print("Press any key to quit")
    getch()
    quit()

comm_result, com_error = servo.WritePosEx(SERVO_ID, TARGET_POSITION, DEF_SERVO_SPEED, DEF_SERVO_ACC)
if comm_result != COMM_SUCCESS:
    print("WritePosEx: %s" % servo.getTxRxResult(comm_result))
elif com_error != 0:
    print("WritePosEx: %s" % servo.getRxPacketError(com_error))
while 1:
    print("Press any key to continue or ESC to quit")
    if getch() == chr(0x1b):
        break
    present_position, present_speed, comm_result, com_error = servo.ReadPosSpeed(SERVO_ID)
    if comm_result != COMM_SUCCESS:
        print("ReadPosSpeed: %s" % servo.getTxRxResult(comm_result))
    else:
        print(
            "ID:%03d GoalPos:%d PresPos:%d PresSpd:%d" % (SERVO_ID, TARGET_POSITION, present_position, present_speed))
    if com_error != 0:
        print("ReadPosSpeed: %s" % servo.getRxPacketError(com_error))

comm_result, com_error = servo.WritePosEx(SERVO_ID, MIDDLE_POSITION, DEF_SERVO_SPEED, DEF_SERVO_ACC)

portHandler.closePort()
print("Done!")
