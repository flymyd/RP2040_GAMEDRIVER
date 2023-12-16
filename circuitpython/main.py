# @author flymyd@foxmail.com
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

# Mapping absolute coord to relative coord. CONST 32767 = 100%
def transpose(x, y):
    return ((x * 32767) // base_resolution[0], (y * 32767) // base_resolution[1])

button_map = {
    "L": Mouse.LEFT_BUTTON,
    "R": Mouse.RIGHT_BUTTON,
    "M": Mouse.MIDDLE_BUTTON
}

uart = busio.UART(board.GP0, board.GP1, baudrate=115200)

while True:
    if supervisor.runtime.serial_bytes_available:
        value = input().strip()
        if value:
            cmd, _, args = value.partition(':')
            # Device find helper
            if cmd == "IDENTIFY":
                print("DETECTED")
            # Set vScreen resolution
            elif cmd == "SETSCR":
                args = args.split(',')
                if len(args) == 2:
                    try:
                        base_resolution = list(map(int, args))
                    except ValueError:
                        print("Invalid width or height")
                else:
                    print("Invalid SETSCR value, like SETSCR:2560,1440")
            # MouseMove handler
            elif cmd == "MM":
                args = args.split(',')
                if len(args) == 2:
                    try:
                        mouse.move(*transpose(int(args[0]), int(args[1])))
                    except ValueError:
                        print("Invalid xCoord or yCoord")
                else:
                    print("Invalid MouseMove value, like MM:1280,720")
            # MouseClick handler
            elif cmd == "MC":
                if args in ("L", "R", "M"):
                    mouse.click(button_map[args])
                else:
                    print("Invalid MouseClick value, like MC:L or R or M")
            else:
                print("UNHANDLED CMD")
