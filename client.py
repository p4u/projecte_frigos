import sys
import connection as CN
import serial
import os
import time

host = "127.0.0.1"
port=7645
serial_device_basename = "/dev/ttyACM"
serial_device_init = 3
baudrate = 9600

def open_serial():
    #serial.tools.list_ports
    serial_device = False
    for i in range(serial_device_init,8):
        try: 
            os.stat(serial_device_basename+str(i))
            serial_device = serial_device_basename+str(i)
            break
        except FileNotFoundError:
            pass
    if not serial_device:
        print("Error, cannot find a valid serial device")
        sys.exit(2)
    print("Opening serial device " + serial_device)
    return serial.Serial(serial_device, baudrate, timeout=0)

def read(s):
    while not s.inWaiting(): pass
    line = s.readline().decode('utf-8')
    return line

def connect():
    socket = CN.Client(host,port)
    socket.connect()
    return socket

serial_con = open_serial()
try:
    client = connect()
except ConnectionRefusedError:
    print("Cannot connect to server")
    sys.exit(2)

while True:
    data = read(serial_con)
    print(data)
    client.send(data.encode())
    time.sleep(0.2)

client.close()

