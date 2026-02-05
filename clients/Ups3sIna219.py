#!/usr/bin/env python3
import json

import smbus2

# Read INA219 data from USP3S module of UGV02
# For more information see: https://www.waveshare.com/wiki/UPS_Module_3S
# -> Sample demo
#
# default UGV UPS3S configuration register setup
# 0x399f (14751) -> 32V, 320mV, 12bit 0,532ms


# Config Register (R/W)
_REG_CONFIG = 0x00
# SHUNT VOLTAGE REGISTER (R)
_REG_SHUNTVOLTAGE = 0x01
# BUS VOLTAGE REGISTER (R)
_REG_BUSVOLTAGE = 0x02
# POWER REGISTER (R)
_REG_POWER = 0x03
# CURRENT REGISTER (R)
_REG_CURRENT = 0x04
# CALIBRATION REGISTER (R/W)
_REG_CALIBRATION = 0x05


class Ups3sIna219:
    # default wiring of UPS3S on I2C: bus=1, addr=0x41
    def __init__(self, i2c_bus=1, addr=0x41):
        self.bus = smbus2.SMBus(i2c_bus)
        self.addr = addr
        # Set according config values of the UGV
        self._cal_value = 4096
        self._shunt_mV_lsb = 0.01  # 0.01mV
        self._bus_V_lsb = 0.004  # always 4mV
        self._current_lsb = .1  # mA
        self._power_lsb = .002  # W

    def read(self, address):
        data = self.bus.read_i2c_block_data(self.addr, address, 2)
        return (data[0] * 256) + data[1]

    def write(self, address, data):
        temp = [0, 0]
        temp[1] = data & 0xFF
        temp[0] = (data & 0xFF00) >> 8
        self.bus.write_i2c_block_data(self.addr, address, temp)

    # shunt voltage in mV
    def get_shunt_voltage(self):
        self.write(_REG_CALIBRATION, self._cal_value)
        value: int = self.read(_REG_SHUNTVOLTAGE)
        if value > 32767: value -= 65535
        return value * self._shunt_mV_lsb

    # bus voltage in V
    def get_bus_voltage(self):
        self.write(_REG_CALIBRATION, self._cal_value)
        self.read(_REG_BUSVOLTAGE)
        return (self.read(_REG_BUSVOLTAGE) >> 3) * self._bus_V_lsb

    # current in mA
    def get_current(self):
        value = self.read(_REG_CURRENT)
        if value > 32767: value -= 65535
        return value * self._current_lsb

    # power in W
    def get_power(self):
        self.write(_REG_CALIBRATION, self._cal_value)
        value = self.read(_REG_POWER)
        if value > 32767:
            value -= 65535
        return value * self._power_lsb

    def get_power_status(self):
        print("INA219 config: 0x{:4x}".format(self.read(0)))  # config register
        bus_voltage = self.get_bus_voltage()  # voltage on V- (load side)
        shunt_voltage = self.get_shunt_voltage() / 1000
        current = self.get_current() / 1000  # current in A
        power = self.get_power()  # power in W
        p = (bus_voltage - 9) / 3.6 * 100  # 3 x 3V V min batterie, 3.6V target
        if p > 100: p = 100
        if p < 0: p = 0
        return json.dumps(
            {
                "ups3s": {
                    "v_psu": '{:6.3f}'.format(bus_voltage + shunt_voltage),
                    "v_load": '{:6.3f}'.format(bus_voltage),
                    "current": '{:7.4f}'.format(current),
                    "power": '{:6.3f}'.format(power),
                    "percent": '{:3.1f}'.format(p)
                }
            }
        )
