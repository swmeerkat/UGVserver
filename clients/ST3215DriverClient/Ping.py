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

# Default setting
SERVO_ID = 2  # Servo ID : 1 (tilt), 2 (pan)
BAUDRATE = 1000000  # Servo default baudrate : 1000000
DEVICENAME = '/dev/ttyACM0'  # Check which port is being used on your controller

# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
# Get methods and members of Protocol
packetHandler = sts(portHandler)

# Open port
if portHandler.openPort():
  print("Port opened")
else:
  print("Open port failed")
  print("Press any key to terminate...")
  getch()
  quit()

# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
  print("Baudrate changed")
else:
  print("Change baudrate failed")
  print("Press any key to terminate...")
  getch()
  quit()

while 1:
  print("Press any key to continue! (or press ESC to quit!)")
  if getch() == chr(0x1b):
    break
  # Read Servo present position
  sts_present_position, sts_present_speed, sts_comm_result, sts_error = packetHandler.ReadPosSpeed(SERVO_ID)
  if sts_comm_result != COMM_SUCCESS:
    print(packetHandler.getTxRxResult(sts_comm_result))
  else:
    print("[ID:%03d] PresPos:%d PresSpd:%d" % (SERVO_ID, sts_present_position, sts_present_speed))
  if sts_error != 0:
    print(packetHandler.getRxPacketError(sts_error))

portHandler.closePort()
