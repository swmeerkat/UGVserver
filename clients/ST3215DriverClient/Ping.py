#!/usr/bin/env python
#
# modified from
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

# Initialize packetHandler
portHandler = PortHandler(DEVICE_NAME)
packetHandler = sts(portHandler)
# Use default baudrate
if portHandler.openPort():
    print("Port opened")
else:
    print("Open port failed")
    print("Press any key to quit")
    getch()
    quit()

while 1:
    print("Press any key to continue or ESC to quit")
    if getch() == chr(0x1b):
        break
    present_position, present_speed, comm_result, error = packetHandler.ReadPosSpeed(SERVO_ID)
    if comm_result != COMM_SUCCESS:
        print("ReadPosSpeed: %s", packetHandler.getTxRxResult(comm_result))
    else:
        print("Servo:%03d PresPos:%d PresSpd:%d" % (SERVO_ID, present_position, present_speed))
    if error != 0:
        print("ReadPosSpeed: %s", packetHandler.getRxPacketError(error))

portHandler.closePort()
print("Done!")
