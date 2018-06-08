import socket
import threading
import serial_writer
import time

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

    def __del__(self):
        self.client.close()
        self.server.close()

    def listen(self):
        self.client.listen()
        c, addr = self.client.accept()
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
                self.server.send(data)

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Error! Too few arguments!)
    server = ISP_Server(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    while len(threading.enumerate()) > 0:
        time.sleep(0.5)
