import machine
import time
import uos
import uinput
button_pin = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)
uart = machine.UART(0, baudrate=115200)
device = uinput.Device([
    uinput.BTN_LEFT,
    uinput.REL_X,
    uinput.REL_Y,
    uinput.KEY_LEFTCTRL,
    uinput.KEY_LEFTALT,
    uinput.KEY_1,
    uinput.KEY_W,
])
def button_callback(pin):
    # 发送指令给电脑
    uart.write("button_pressed")
button_pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=button_callback)
while True:
    if uart.any():
        data = uart.read()
        print("Received coordinates:", data)
        coordinates = data.decode().strip().split(",")
        x = int(coordinates[0])
        y = int(coordinates[1])
        device.emit(uinput.REL_X, x)
        device.emit(uinput.REL_Y, y)
        device.emit(uinput.BTN_LEFT, 1)
        device.emit(uinput.BTN_LEFT, 0)
        device.emit(uinput.KEY_LEFTCTRL, 1)
        device.emit(uinput.KEY_LEFTALT, 1)
        device.emit(uinput.KEY_1, 1)
        device.emit(uinput.KEY_1, 0)
        device.emit(uinput.KEY_LEFTALT, 0)
        device.emit(uinput.KEY_LEFTCTRL, 0)
        device.emit(uinput.KEY_W, 1)
        device.emit(uinput.KEY_W, 0)
    time.sleep(0.1)
