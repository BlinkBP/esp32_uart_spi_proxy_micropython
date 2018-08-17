# esp32_uart_isp_proxy
UART/ISP proxy for ESP32 running Micropython


The idea was to communicate with a 3d printer via Wi-Fi but instead of using an expensive RPi I wanted to use a cheap ESP32.
Code in its current state worked. Talking to the 3d printer through UART, with a server running on PC and on ESP32.
The communication on PC is going through a virtual serial connection (used com0com to create the virtual com ports).
Octoprint connected to the 3d printer but printing didn't work well enough for the gcode commands weren't coming quick enough.
I blame the Micropython headway and am going to rewrite the code in C in a different repo.
