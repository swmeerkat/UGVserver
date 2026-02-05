#!/usr/bin/python3
import time

import serial

print("CobraFlex UART test")

serial_port = serial.Serial(
    port="/dev/ttyACM2",
    baudrate=115200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
)
time.sleep(1)

try:
    serial_port.write("{\"T\":1,\"L\":200,\"R\":200}\n".encode())
    while True:
        if serial_port.in_waiting > 0:
            data = serial_port.readline().strip().decode("utf-8")
            print(data)

except KeyboardInterrupt:
    print("Exiting program")

except Exception as exception_error:
    print("Exit program error: %s", exception_error)

finally:
    serial_port.close()
    print('Done!')
