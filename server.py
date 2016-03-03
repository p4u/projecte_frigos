import connection as CN
import threading
import select
import time
import sys
import string
import database
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
        self.db = database.database()
        self.debug = True

    def _check_trasto_exist(self,id,type,create=True):
      if self.db.select("count(*) FROM Trasto WHERE ID='%s'" %(id))[0][0] == 0:
        if create:
          #Hardcoded recolector_id for testing
          r = self.db.insert("Trasto (ID,recolector_id,tipus) VALUES ('%s',3,'%s')" %(id,type))
          if self.debug:
            print("Add new device %s/%s:%s" %(id,type,r))
        return False
      return True

    def _insert_data_frigo(self,id,current,temp1,temp2,potential):
      self._check_trasto_exist(id,"frigo")
      r = self.db.insert("Lectura (trasto_id,intensitat,tensio,temperatura1,temperatura2) VALUES ('%s',%f,%f,%f,%f)" %(id,current,potential,temp1,temp2))
      if self.debug:
        print("Add new data for %s/%s with values I=%f V=%f T1=%f T2=%f: %s" %(id,"frigo",current,potential,temp1,temp2,r))

    def analyze(self,data):
        try:
            data_colon = data.split(":")
            id = data_colon[0].strip()
            data_coma = data_colon[1].split(",")
            current = float(data_coma[0].strip())
            temp1 = float(data_coma[1].strip())
            temp2 = float(data_coma[2].strip())
            potential = float(data_coma[3].strip())
            #print("ID=%s I=%s T1=%s T2=%s V=%s" %(id,current,temp1,temp2,potential))
            self._insert_data_frigo(id,current,temp1,temp2,potential)
        except Exception as e:
            print("Cannot understand: %s" %data)
            print(e)


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
