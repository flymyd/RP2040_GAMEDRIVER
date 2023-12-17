import time
import serial
import pyautogui
import serial.tools.list_ports

baudrate = 115200

def send_package(ser, payload):
    try:
        # ser = serial.Serial(port, baudrate=baudrate)
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
        # ser.close()
        return response
    except serial.SerialException:
        return serial.SerialException

def search_pico():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        try:
            ser = serial.Serial(port.device, baudrate=baudrate)
            response = send_package(ser, "IDENTIFY")
            ser.close()
            if response == "DETECTED":
                print(port.device)
                return port.device
            else:
                pass
        except serial.SerialException:
            print(serial.SerialException)
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
    try:
        ser = serial.Serial(pico_port, baudrate=baudrate)
        commands = ["MM:1,1", "MC:L", "MM:640,860", "MC:L", "MM:1920,470","MC:L"]
        for command in commands:
            res = send_package(ser, command)
            print(res.strip())
            time.sleep(1)
        time.sleep(5)
        commands = ["MM:1,1", "MM:650,420", "MC:L", "KP:W", "KR:W", "KC:F"]
        for command in commands:
            res = send_package(ser, command)
            print(res.strip())
            time.sleep(1)
        ser.close()
    except serial.SerialException:
        print(serial.SerialException)
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



