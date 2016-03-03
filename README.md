# projecte_frigos
Projecte frigos

### Server

Listen for network connection and save the client info into the database

  python2.7 server.py


### Client

Read serial Input and send it to the Server

```sh
python2.7 client.py -h
usage: client.py [-h] [-d SERIAL_DEVICE] [-i RECOLECTOR_ID] [-s HOST]
                 [-p PORT] [-b BAUDRATE]

Trastos monitor

optional arguments:
  -h, --help        show this help message and exit
  -d SERIAL_DEVICE  Serial device
  -i RECOLECTOR_ID  Recolector identifier
  -s HOST           Server host or IP
  -p PORT           Server port
  -b BAUDRATE       Baudrate for the serial device
```
