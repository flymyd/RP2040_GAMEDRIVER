import time
import supervisor
import usb_hid
from absolute_mouse import Mouse
import board
import busio

mouse = Mouse(usb_hid.devices)

# 32767 = 100%
def transpose(x, y):
    return ((x * 32767) // 2560, (y * 32767) // 1440)

positions = [(1, 1), (1280, 720)]
uart = busio.UART(board.GP0, board.GP1, baudrate=115200)
while True:
    if supervisor.runtime.serial_bytes_available:
        value = input().strip()
        if value == "":
            continue
        if value == "identify_pico":
            print("pico_detected")
        elif value == "114514":
            for position in positions:
                print("MOVE", position, transpose(*position))
                mouse.move(*transpose(*position))
                time.sleep(2)
        else:
            print("1919810")
