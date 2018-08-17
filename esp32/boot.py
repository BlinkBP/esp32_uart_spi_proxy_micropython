def connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('<YOUR WIFI SSID>', '<YOUR WIFI PASS>')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

def no_debug():
    import esp
    # this can be run from the REPL as well
    esp.osdebug(None)

connect()
#import isp_server
import isp_server
from time import sleep
#self_addr, addr, serial, baud, launch_serial, receive, send, reverse
server = isp_server.ISP_Server("192.168.0.17", "192.168.0.14", None, 115200, True, True, True, True)
while True:
    sleep(0.5)
