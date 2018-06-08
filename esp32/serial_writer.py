from machine import Pin, SPI
import serial

def open_serial(port, baud):
    spi = SPI(1)
    spi.init(baudrate=115200, polarity=1, phase=0, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
    return spi

def write(ser, data):
    ss = Pin(15, Pin.OUT)
    ss.value(0)
    ser.write(data)
    ss.value(1)

def close_serial(ser):
    ser.close()

def write_once(port, baud, data):
    ser = open_serial(port, baud)
    ss = Pin(15, Pin.OUT)
    ss.value(0)
    ser.write(data)
    ss.value(1)
    ser.close()

def read(ser):
    while True:
        ss = Pin(15, Pin.OUT)
        ss.value(0)
        data = ser.read(4096)
        ss.value(1)
        if len(data) > 0:
            return data
