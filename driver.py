import serial
import pyautogui
import serial.tools.list_ports

def search_pico():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        try:
            ser = serial.Serial(port.device, baudrate=115200, timeout=1)
            ser.write("identify_pico".encode())  # 发送识别指令
            response = ser.readline().decode().strip()
            ser.close()
            if response == "pico_detected":
                return port.device
        except serial.SerialException:
            pass
    return None

pico_port = search_pico()
if pico_port:
    print("树莓派 Pico已识别，位于串口设备：", pico_port)
    # 配置串口参数
    ser = serial.Serial(pico_port, 115200)
    # 循环接收指令并返回屏幕坐标
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode().strip()
            if data == "button_pressed":
                # 获取屏幕坐标
                x, y = pyautogui.position()
                # 发送坐标给树莓派
                ser.write(f"{x},{y}\n".encode())
else:
    print("未找到树莓派 Pico")



