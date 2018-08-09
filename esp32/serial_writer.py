from machine import UART

def open_serial(port, baud):
    uart = UART(1)
    uart.init(baud, bits=8, parity=None, stop=1, tx=17, rx=16)
    return uart

def write(ser, data):
    ser.write(data)

def write_once(port, baud, data):
    ser = open_serial(port, baud)
    ser.write(data)
    close_serial(ser)

def read(ser):
    return ser.read(64)
