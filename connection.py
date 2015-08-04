import socket
import time

class Client():
    def __init__(self, host, port):
        global dns
        self.host = host
        self.ip = host
        self.port = int(port)
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.setblocking(1)

    def connect(self):
        self.conn.connect((self.ip, self.port))
        return self.conn

    def send(self, msg):
        return self.conn.sendall(msg)

    def recv(self):
        return self.conn.recv(1024)

    def close(self):
        self.conn.close()


class Server():
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.setblocking(1)
        self.conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.conn.bind((self.host, self.port))

    def listen(self):
        print('waiting for new connections on %s:%s' %
                      (self.host, self.port))
        self.conn.listen(5)
        try:
            current_conn, addr = self.conn.accept()
        except InterruptedError:
            return False
        current_conn.setblocking(1)
        return current_conn

    def recive(self):
        data = self.current_conn.recv(1024).decode()
        return data

    def send(self, msg):
        data = self.current_conn.recv(1024).decode()
        return data

    def close(self):
        self.conn.shutdown(2)
        self.conn.close()
