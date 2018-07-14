from machine import Pin, SPI

def open_serial(port, baud):
    spi = SPI(1, baudrate=baud, polarity=0, phase=0)
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
        data = ser.read(64)
        ss.value(1)
        if data and data[0] != b'\x00':
            return data

def send_recv(ser, data, buff):
    ss = Pin(5, Pin.OUT)
    ss.value(0)
    ser.write_readinto(data, buff)
    ss.value(1)
    return buff
