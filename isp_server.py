import socket
import threading
import serial_writer

class ISP_Server:
    #server socket = 2700
    #client socket = 2701

    def __init__(self, self_addr, addr, serial, baud):
        self.server = socket.socket()
        self.client = socket.socket()
        self.server.connect((addr, 2700))
        self.client.bind((self_addr, 2701))
        self.ser = serial_writer.open_serial(serial, baud)
        self.lock = False
        threading.Thread(target = self.listen).start()
        threading.Thread(target = self.send).start()

    def listen(self):
        self.client.listen()
        c, addr = self.client.accept()
        while True:
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
            if not self.lock:
                self.lock = True
                data = serial_writer.read(self.ser)
                self.lock = False
                #print(data)
                self.server.send(data)
