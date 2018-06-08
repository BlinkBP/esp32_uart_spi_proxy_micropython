import serial

def open_serial(port, baud):
    return serial.Serial(port, baud)

def send(ser, data):
    ser.write(data)

def close_serial(ser):
    ser.close()

def send_once(port, baud, data):
    #port = "/dev/ttySX"
    ser = open_serial(port, baud)
    ser.write(data)
    ser.close()

def read(ser):
    while True:
        data = ser.read(4096)
        if len(data) > 0:
            return data
