#!/usr/bin/env python3
import requests
import json


#
# References:
#  - https://www.waveshare.com/wiki/UGV02
#  - https://www.waveshare.com/wiki/2-Axis_Pan-Tilt_Camera_Module
#
class UgvEsp32:

  def __init__(self, ip="0.0.0.0"):
    self.ip = ip
    self.actPan = 0
    self.actTilt = 0

  # Retrieve IMU data
  # Output:
  #  3D orientation angles
  #    - r (roll, rotation about x-axis)
  #    - p (pitch, rotation about y-axis)
  #    - y (yaw, rotation about z-axis)
  #  accelerometer
  #    - ax, ay, az
  #  gyroscope
  #    - gx, gy, gz
  #  magnetometer
  #    - mx, my, mz
  #
  #  - temp
  def get_imu_data(self):
    cmd = "{\"T\":130}"
    return self.do_get(cmd)

  # CMD_BASE_FEEDBACK
  # Output:
  #  - L, R
  #  3D orientation angles
  #    - r, p, y
  #  Voltage:
  #    - v
  def get_base_feedback(self):
    cmd = "{\"T\":126}"
    return self.do_get(cmd)

  #
  # Set servo middle position
  # Sets the actual servo position as new middle position
  # Input:
  #  - id: 1 - tilt servo, 2 - pan servo
  def new_middle_position(self):
    servo = "1"
    cmd = "{\"T\":502,\"id\":" + servo + "}"
    self.do_get(cmd)
    servo = "2"
    cmd = "{\"T\":502,\"id\":" + servo + "}"
    return self.do_get(cmd)

  #
  # CMD_SPEED_CTRL
  # Input:
  #  - left, right: speed of the wheel, value range 0.5 - -0.5
  def ugv_speed_control(self, left, right):
    cmd = "{\"T\":1,\"L\":" + str(left) + ",\"R\":" + str(right) + "}"
    return self.do_get(cmd)

  # CMD_GIMBAL_CTRL_SIMPLE
  # Input:
  #  - X: PAN, value range -180 to 180
  #  - Y: Tilt, value range -30 to 90
  #  - SPD: Speed, 0 means fastest
  #  - ACC: Acceleration, 0 means fastest
  def gimbal_ctrl_simple(self, pan, tilt):
    cmd = "{\"T\":133,\"X\":" + str(pan) + ",\"Y\":" + str(tilt) + ",\"SPD\":0,\"ACC\":0} "
    self.actPan = pan
    self.actTilt = tilt
    return self.do_get(cmd)

  #
  # CMD_GIMBAL_CTRL_STOPE
  # Stops the pan-tilt movement at any time
  def gimbal_ctrl_stop(self):
    cmd = "{\"T\":133} "
    self.do_get(cmd)

  # pan one step to right
  def pan_right(self):
    if self.actPan < 180:
      self.actPan += 2
    self.gimbal_ctrl_simple(self.actPan, self.actTilt)

  # pan one step to left
  def pan_left(self):
    if self.actPan > -180:
      self.actPan -= 2
    self.gimbal_ctrl_simple(self.actPan, self.actTilt)

  # tilt one step up
  def tilt_up(self):
    if self.actTilt < 90:
      self.actTilt += 2
    self.gimbal_ctrl_simple(self.actPan, self.actTilt)

  # tilt one step down
  def tilt_down(self):
    if self.actTilt > -30:
      self.actTilt -= 2
    self.gimbal_ctrl_simple(self.actPan, self.actTilt)

  # execute ugv command
  def do_get(self, cmd):
    url = "http://" + self.ip + "/js?json=" + cmd
    print(url)
    response = requests.get(url)
    return json.dumps(response.json())
