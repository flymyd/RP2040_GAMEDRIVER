import time
import supervisor
import usb_hid
from absolute_mouse import Mouse
import board
import busio
import re

mouse = Mouse(usb_hid.devices)
# Screen resolution, default is 2K 16:9
base_resolution = [2560, 1440]

# 32767 = 100%
def transpose(x, y):
    return ((x * 32767) // base_resolution[0], (y * 32767) // base_resolution[1])

uart = busio.UART(board.GP0, board.GP1, baudrate=115200)
while True:
    if supervisor.runtime.serial_bytes_available:
        value = input().strip()
        if value == "":
            continue
        # Help client to find device
        if value == "IDENTIFY":
            print("DETECTED")
        # Set screen resolution
        if value.startswith("SETSCR:"):
            values = value[7:].split(',')
            if len(values) == 2:
                try:
                    base_resolution = [int(values[0]), int(values[1])]
                except ValueError:
                    print("Invalid width or height")
            else:
                print("Invalid SETSCR format, like SETSCR:2560,1440")
        # Mouse Move handler
        elif value.startswith("MM:"):
            values = value[3:].split(',')
            if len(values) == 2:
                try:
                    mouse.move(*transpose(int(values[0]), int(values[1])))
                except ValueError:
                    print("Invalid xCoord or yCoord")
            else:
                print("Invalid MouseMove format, like MM:1280,720")
        else:
            # mouse.click(Mouse.LEFT_BUTTON)
            print("UNHANDLED CMD")
