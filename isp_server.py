import socket
import _thread
import serial_writer
from time import sleep

class ISP_Server:
    #server socket = 2700
    #client socket = 2701

    def __init__(self, self_addr, addr, serial, baud, launch_serial, receive, send, reverse):
        print("Starting ISP_Server!")
        self.server = None
        self.client = None
        self.lock = False
        port = [2700, 2701]
        if reverse:
            port = port[::-1]
        if launch_serial:
            self.ser = serial_writer.open_serial(serial, baud)
        else:
            self.ser = None
        if receive:
            _thread.start_new_thread(self.receive, (self_addr, addr, port[0], serial, baud))
        if send:
            _thread.start_new_thread(self.send, (self_addr, addr, port[1], serial, baud))

    def __del__(self):
        if self.server is not None:
            self.server.close()
        if self.client is not None:
            self.client.close()

    def get_socket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s

    def receive(self, self_addr, addr, port, serial, baud):
        print("Starting client...")
        self.client = self.get_socket()
        self.connected = False
        sleep(10)
        print("Trying to connect to {}:{}...".format(addr, port))
        while not self.connected:
            try:
                self.client.connect((addr, port))
                self.connected = True
                print("Connected with {} at {}".format(addr, port))
            except Exception as e:
                sleep(1)
        while True:
            sleep(0.1)
            try:
                data = self.client.recv(64)
                if data:
                    while self.lock:
                        pass
                    self.lock = True
                    print("Writing to own serial: {}".format(bytes(data)))
                    serial_writer.write(self.ser, data)
                    self.lock = False
                else:
                    raise error("Client disconnected!")
            except:
                return False

    def send(self, self_addr, addr, port, serial, baud):
        print("Starting server...")
        self.server = self.get_socket()
        self.server.bind((self_addr, port))
        print("Started server at {}:{}".format(self_addr, port))
        print("Listening for a client...")
        self.server.listen(1)
        c, addr = self.server.accept()
        print("Accepted connection from {}".format(addr))
        while True:
            sleep(0.1)
            if not self.lock:
                self.lock = True
                data = serial_writer.read(self.ser)
                self.lock = False
                print("Read data from own serial: {}".format(bytes(data))).encode()
                c.sendall(data)

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("Error! Too few arguments!")
    server = ISP_Server(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    while len(threading.enumerate()) > 0:
        sleep(0.5)
