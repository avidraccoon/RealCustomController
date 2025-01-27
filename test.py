import usb_hid
from hid_gamepad import Gamepad
import time
import wifi
import os

import adafruit_requests

ssid = os.getenv("CIRCUITPY_WIFI_SSID")
password = os.getenv("CIRCUITPY_WIFI_PASSWORD")

IP = "10.80.65.133"
JSON_GET_URL = "https://httpbin.org/get"

dt = 0.5
gp = Gamepad(usb_hid.devices)

while True:
    
    time.sleep(dt)