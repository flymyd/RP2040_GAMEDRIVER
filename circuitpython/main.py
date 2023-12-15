import time
import usb_hid
from absolute_mouse import Mouse

m = Mouse(usb_hid.devices)

# mouse_abs accept value from 0 to 32767 for both X and Y
# Note: Values are NOT pixels! 32767 = 100% (to right or to bottom)


def transpose(x, y):
    return ((x * 32767) // 2560, (y * 32767) // 1440)


positions = [(1, 1), (1280, 720)]

while True:
    for position in positions:
        print("MOVE", position, transpose(*position))
        m.move(*transpose(*position))
        time.sleep(2)
    # time.sleep(10)
    break