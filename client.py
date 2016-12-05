#!/usr/bin/env python2.7
import sys
import connection as CN
import serial
import os
import time
import argparse
import logging

serial_device_basename = "/dev/ttyACM"
serial_device_init = 0

def set_log(logname):
    logging.basicConfig(filename=logname,
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(message)s',
                            datefmt='%d/%m/%y %H:%M:%S',
                            level=logging.DEBUG)
    global logger
    logger = logging.getLogger("monitor")

def parse_args():
  parser = argparse.ArgumentParser(
      description='Trastos monitor')
  parser.add_argument(
      '-d',
      dest='serial_device',
      type=str,
      default=None,
      help='Serial device')
  parser.add_argument(
      '-i',
      dest='recolector_id',
      type=str,
      default=0,
      help='Recolector identifier')
  parser.add_argument(
      '-l',
      dest='logname',
      type=str,
      default='/tmp/monitor.log',
      help='Log file')
  parser.add_argument(
      '-s',
      dest='host',
      default='127.0.0.1',
      type=str,
      help='Server host or IP')
  parser.add_argument(
      '-p',
      dest='port',
      type=int,
      default=7645,
      help='Server port')
  parser.add_argument(
      '-b',
      dest='baudrate',
      type=int,
      default=9600,
      help='Baudrate for the serial device')
  return parser.parse_args()

def open_serial(device):
    #serial.tools.list_ports
    if device == None:
      serial_device = False
      for i in range(serial_device_init,8):
          try: 
              os.stat(serial_device_basename+str(i))
              serial_device = serial_device_basename+str(i)
              break
          except Exception as e:
              print(e)
              pass

      if not serial_device:
          print("Error, cannot find a valid serial device.")
          logger.error("Cannot find a valid serial device")
          sys.exit(2)

    else: serial_device = device
    print("Opening serial device " + serial_device)
    logger.info("Opening serial device " + serial_device)
    return serial.Serial(serial_device, baudrate, timeout=0)

def read(s):
    while not s.inWaiting(): pass
    line = s.readline().decode('utf-8')
    return line

def connect():
    socket = CN.Client(host,port)
    socket.connect()
    return socket

def send_id_info():
    data = "RECOLECTOR_ID:%s\n" %(recolector_id)
    client.send(data.encode())
    time.sleep(0.2)

args = parse_args()
set_log(args.logname)
recolector_id = args.recolector_id
baudrate = args.baudrate
port = args.port
host = args.host
serial_con = open_serial(args.serial_device)

try:
    client = connect()
except ConnectionRefusedError:
    print("Cannot connect to server")
    logger.error("Cannot connect to server")
    sys.exit(2)

send_id_info()
while True:
    data = read(serial_con)
    logger.info("Send: " + data)
    client.send(data.encode())
    time.sleep(0.2)

client.close()

