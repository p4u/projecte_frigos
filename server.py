import connection as CN
import threading
import select
import time
import sys
import string

server = CN.Server("0.0.0.0",7645)

class Service(object):
    """
    Service for managing the TCP network socket. It is designed to be used as a thread.
    It keeps listening for input data, once something arrives, it calls the analyze method
    which tries to extract the fields.
    """
    def __init__(self,sock):
        self.shutdown = False
        self.socket = sock
        self.socket.setblocking(1)

    def analyze(self,data):
        try:
            data_colon = data.split(":")
            id = data_colon[0].strip()
            data_coma = data_colon[1].split(",")
            current = data_coma[0].strip()
            temp1 = data_coma[1].strip()
            temp2 = data_coma[2].strip()
            potential = data_coma[3].strip()
            print("ID=%s I=%s T1=%s T2=%s V=%s" %(id,current,temp1,temp2,potential))
        except:
            print("Cannot understand: %s" %data)


    def start(self):
        while not self.shutdown:
            try:
                ready_to_read, ready_to_write, in_error = \
                        select.select([self.socket,], [self.socket,], [], 5)
            except select.error:
                self.socket.shutdown(2)
                self.socket.close()
                self.shutdown = True
                print("Closing socket...")

            if not self.shutdown and len(ready_to_read) > 0:
                    #data = self.socket.recv(1024).decode()
                    fs = self.socket.makefile()
                    data = fs.readline()
                    if data: self.analyze(data)
            time.sleep(0.2)

while True:
    try:
        server_listen = server.listen()
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit(0)
    connection = Service(server_listen)
    t = threading.Thread(target=connection.start, args=[])
    t.daemon = True
    t.start()
