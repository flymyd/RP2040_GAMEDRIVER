import time
import serial
import pyautogui
import serial.tools.list_ports

baudrate = 115200

def send_package(port, payload):
    try:
        ser = serial.Serial(port, baudrate=baudrate)
        command = f'{payload}\n\r'.encode()
        ser.write(command)
        reply = b''
        for _ in range(len(command)):
            a = ser.read()
        while True:
            a = ser.read()
            if a== b'\r':
                break
            else:
                reply += a
            time.sleep(0.01)
        response = reply.decode("ascii")
        ser.close()
        return response
    except serial.SerialException:
        return ""

def search_pico():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        response = send_package(port.device, "identify_pico")
        if response == "pico_detected":
            return port.device
        else:
            pass
    return None

pico_port = search_pico()

# Listen serial example
# ser = serial.Serial(
#              '/dev/ttyACM0',
#              baudrate=115200,
#              timeout=0.01)

# ser.write(b'HELLO from CircuitPython\n')
# x = ser.readlines()
# print("received: {}".format(x))

if pico_port:
    print("Pico已识别，位于串口设备：", pico_port)
    res = send_package(pico_port, "ACCEED")
    print(res)
    # while True:
    #     if ser.in_waiting > 0:
    #         data = ser.readline().decode().strip()
    #         print(data)
    #         if data == "button_pressed":
    #             # 获取屏幕坐标
    #             x, y = pyautogui.position()
    #             # 发送坐标给树莓派
    #             ser.write(f"{x},{y}\n".encode())
else:
    print("未找到树莓派 Pico")



