import socket
import _thread
#import isp_writer
import serial_writer as isp_writer
from time import sleep

class ISP_Server:
    #server socket = 2700
    #client socket = 2701

    def __init__(self, self_addr, addr, serial, baud, launch_serial, receive, send, slave):
        print("Starting ISP_Server!")
        self.connected = False
        self.client_connected = False
        self.server = None
        self.client = None
        port = [2700, 2701]

        if slave:
            from ucollections import deque
            port = port[::-1]
        else:
            from collections import deque
        self.d_to_send = deque((), 128)
        self.d_to_write = deque((), 128)

        if receive:
            _thread.start_new_thread(self.connect, (self_addr, addr, port[0]))
        if send:
            _thread.start_new_thread(self.start_server, (self_addr, addr, port[1]))

        self.ser = isp_writer.open_serial(serial, baud)
        while not self.connected and not self.client_connected:
            sleep(0.2)
        _thread.start_new_thread(self.send, ())
        _thread.start_new_thread(self.read_serial, ())
        _thread.start_new_thread(self.receive, ())
        _thread.start_new_thread(self.write_serial, ())
        print("ISP_Server started!")

    def __del__(self):
        if self.server is not None:
            self.server.close()
        if self.client is not None:
            self.client.close()

    def get_socket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s

    def read_serial(self):
        while True:
            data = None
            data = isp_writer.read(self.ser)
            if data is not None and len(data) > 0:
                self.d_to_send.append(data)

    def write_serial(self):
        while True:
            try:
                data = self.d_to_write.popleft()
                print("Received and writing to serial:{}".format(data))
                isp_writer.write(self.ser, data)
            except:
                pass

    def send(self):
        while True:
            try:
                data = self.d_to_send.popleft()
                print("Read and sending to client:{}".format(data))
                self.c.sendall(data)
            except:
                pass

    def receive(self):
        while True:
            data = None
            try:
                data = self.client.recv(64)
            except:
                pass
            if data is not None and len(data) > 0:
                self.d_to_write.append(data)


    def sendcmd(self, cmd):
        if self.c:
            self.c.send(cmd)

    def readcmd(self):
        if self.client:
            try:
                return self.client.recv(64)
            except:
                return "Timed out..."

    def connect(self, self_addr, addr, port):
        print("Starting client...")
        self.client = self.get_socket()
        self.connected = False
        print("Trying to connect to {}:{}...".format(addr, port))
        while not self.connected:
            try:
                self.client.connect((addr, port))
                self.connected = True
                #self.client.settimeout(0.1)
                print("Connected with {} at {}".format(addr, port))
            except Exception as e:
                sleep(0.5)

    def start_server(self, self_addr, addr, port):
        print("Starting server...")
        self.server = self.get_socket()
        self.client_connected = False
        self.server.bind((self_addr, port))
        print("Started server at {}:{}".format(self_addr, port))
        print("Listening for a client...")
        self.server.listen(1)
        self.c, addr = self.server.accept()
        print("Accepted connection from {}".format(addr))
        self.client_connected = True

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("Error! Too few arguments!")
    server = ISP_Server(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    while len(_thread.enumerate()) > 0:
        sleep(1)
