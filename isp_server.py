import socket
import _thread
import serial_writer
from time import sleep

class ISP_Server:
    #server socket = 2700
    #client socket = 2701

    def __init__(self, self_addr, addr, serial, baud, reverse):
        print("Starting ISP_Server!")
        port = [2700, 2701]
        if reverse:
            port = port[::-1]
        self.create_sockets()
        self.connect(self_addr, addr, port, serial, baud)
        self.lock = False
        _thread.start_new_thread(self.send, ())

    def __del__(self):
        self.client.close()
        self.server.close()

    def create_sockets(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def connect(self, self_addr, addr, port, serial, baud):
        print("Connecting...")
        self.client.bind((self_addr, port[1]))
        _thread.start_new_thread(self.listen, ())
        self.ser = serial_writer.open_serial(serial, baud)
        self.connected = False
        while not self.connected:
            try:
                self.server.connect((addr, port[0]))
                self.connected = True
                print("Connected with {} at {}".format(addr, port[0]))
            except Exception as e:
                print("Trying to connect to {} at {}...".format(addr, port[0]))
                sleep(0.1)

    def listen(self):
        print("Listening...")
        self.client.listen(1)
        c, addr = self.client.accept()
        print("Accepted connection from {}".format(addr))
        while True:
            sleep(0.1)
            try:
                data = c.recv(4096)
                if data:
                    while self.lock:
                        pass
                    self.lock = True
                    serial_writer.write(self.ser, data)
                    self.lock = False
                else:
                    raise error("Client disconnected!")
            except:
                c.close()
                self.client.close()
                self.server.close()
                return False

    def send(self):
        while True:
            sleep(0.1)
            if not self.lock:
                self.lock = True
                data = serial_writer.read(self.ser)
                self.lock = False
                print(data)
                #self.server.sendall(data)

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("Error! Too few arguments!")
    server = ISP_Server(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    while len(threading.enumerate()) > 0:
        time.sleep(0.5)
