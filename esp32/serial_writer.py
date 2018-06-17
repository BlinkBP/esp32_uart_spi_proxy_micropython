from machine import Pin, SPI

def open_serial(port, baud):
    spi = SPI(1, SPI.MASTER, baudrate=baud, polarity=1, phase=0, crc=None)
    #spi.init(baudrate=baud, polarity=1, phase=0, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
    return spi

def write(ser, data):
    ss = Pin(5, Pin.OUT)
    ss.value(0)
    ser.write(data)
    ss.value(1)

def close_serial(ser):
    ser.close()

def write_once(port, baud, data):
    ser = open_serial(port, baud)
    ss = Pin(5, Pin.OUT)
    ss.value(0)
    ser.write(data)
    ss.value(1)
    ser.close()

def read(ser):
    while True:
        ss = Pin(5, Pin.OUT)
        ss.value(0)
        data = ser.read(8)
        ss.value(1)
        if data and data[0] != b'\x00':
            return data

def send_recv(ser, data):
    ss = Pin(5, Pin.OUT)
    ss.value(0)
    resp = ser.send_recv(data)
    ss.value(1)
    return resp
