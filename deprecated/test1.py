import machine
import time
import uinput

uart = machine.UART(0, baudrate=115200)
device = uinput.Device([
    uinput.BTN_LEFT,
    uinput.REL_X,
    uinput.REL_Y,
])

def simulate_keyboard_action(action):
    if action == "click":
        device.emit(uinput.BTN_LEFT, 1)
        device.emit(uinput.BTN_LEFT, 0)
    elif action == "ctrl_alt_1":
        device.emit(uinput.KEY_LEFTCTRL, 1)
        device.emit(uinput.KEY_LEFTALT, 1)
        device.emit(uinput.KEY_1, 1)
        device.emit(uinput.KEY_1, 0)
        device.emit(uinput.KEY_LEFTALT, 0)
        device.emit(uinput.KEY_LEFTCTRL, 0)
    elif action == "w":
        device.emit(uinput.KEY_W, 1)
        device.emit(uinput.KEY_W, 0)

while True:
    if uart.any():
        data = uart.read()
        action = data.decode().strip()
        print("Received action:", action)
        simulate_keyboard_action(action)
    time.sleep(0.1)
