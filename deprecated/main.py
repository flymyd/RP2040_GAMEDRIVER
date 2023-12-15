# Author: flymyd@foxmail.com
# A custom keyboard driver for emulate keyboard / mouse macro
# Based on RP2040-Zero, also compatible with Raspberry Pi Pico. 

import machine
import time
import uos


# Configure the switch pins
button_pin0 = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
button_pin1 = machine.Pin(1, machine.Pin.IN, machine.Pin.PULL_UP)
button_pin2 = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)
button_pin3 = machine.Pin(3, machine.Pin.IN, machine.Pin.PULL_UP)

# Configure UART
uart = machine.UART(0, baudrate=115200)

# Create a virtual mouse device
v_mouse = uinput.Device([
    uinput.BTN_LEFT,
    uinput.REL_X,
    uinput.REL_Y,
])

# IRQ callback
def button_callback(pin):
    uart.write("button_pressed_" + pin)

# Configure IRQ trigger
button_pin0.irq(trigger=machine.Pin.IRQ_FALLING, handler=button_callback(0))
button_pin1.irq(trigger=machine.Pin.IRQ_FALLING, handler=button_callback(1))
button_pin2.irq(trigger=machine.Pin.IRQ_FALLING, handler=button_callback(2))
button_pin3.irq(trigger=machine.Pin.IRQ_FALLING, handler=button_callback(3))

while True:
    if uart.any():
        data = uart.read()
        print("Received uart data:", data)
        formatted_data = data.decode().strip()
        

        coordinates = data.decode().strip().split(",")
        x = int(coordinates[0])
        y = int(coordinates[1])

        # 使用虚拟鼠标设备模拟鼠标移动和点击操作
        v_mouse.emit(uinput.REL_X, x)
        v_mouse.emit(uinput.REL_Y, y)
        v_mouse.emit(uinput.BTN_LEFT, 1)
        v_mouse.emit(uinput.BTN_LEFT, 0)

    time.sleep(0.1)
