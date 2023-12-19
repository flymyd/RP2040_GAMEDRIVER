# @author flymyd@foxmail.com
import supervisor
import usb_hid
import board
import busio
import time
from absolute_mouse import Mouse
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

mouse = Mouse(usb_hid.devices)
keyboard = Keyboard(usb_hid.devices)
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
                        print(f"SETSCR:{base_resolution}")
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
                        print(f"MM:{args}")
                    except ValueError:
                        print("Invalid xCoord or yCoord")
                else:
                    print("Invalid MouseMove value, like MM:1280,720")
            # MouseClick handler
            elif cmd == "MC":
                if args in ("L", "R", "M"):
                    mouse.click(button_map[args])
                    print(f"MC:{args}")
                else:
                    print("Invalid MouseClick value, like MC:L or R or M")
            # MousePress handler
            elif cmd == "MP":
                if args in ("L", "R", "M"):
                    mouse.press(button_map[args])
                    print(f"MP:{args}")
                else:
                    print("Invalid MousePress value, like MP:L or R or M")
            # MouseRelease handler
            elif cmd == "MR":
                if args in ("L", "R", "M"):
                    mouse.release(button_map[args])
                    print(f"MR:{args}")
                else:
                    print("Invalid MouseRelease value, like MR:L or R or M")
            # MouseReleaseAll handler
            elif cmd == "MRA":
                mouse.release_all()
                print("MRA")
            # KeyboardClick handler
            elif cmd == "KC":
                args = args.split(",")
                for key_name in args:
                    try:
                        keycode = getattr(Keycode, key_name)
                        keyboard.press(keycode)
                        time.sleep(0.01)
                        keyboard.release(keycode)
                    except AttributeError as e:
                        print(f"Error: {e}. '{key_name}' may not be a valid keycode.")
                keyboard.release_all()
                print(f"KC:{args}")
            # KeyboardPress handler
            elif cmd == "KP":
                args = args.split(",")
                for key_name in args:
                    try:
                        keycode = getattr(Keycode, key_name)
                        keyboard.press(keycode)
                    except AttributeError as e:
                        print(f"Error: {e}. '{key_name}' may not be a valid keycode.")
                print(f"KP:{args}")
            # KeyboardRelease handler
            elif cmd == "KR":
                args = args.split(",")
                for key_name in args:
                    try:
                        keycode = getattr(Keycode, key_name)
                        keyboard.release(keycode)
                    except AttributeError as e:
                        print(f"Error: {e}. '{key_name}' may not be a valid keycode.")
                print(f"KR:{args}")
            # KeyboardReleaseAll handler
            elif cmd == "KRA":
                keyboard.release_all()
                print("KRA")
            else:
                print("UNHANDLED CMD")
