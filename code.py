import usb_hid # type: ignore
from hid_gamepad import Gamepad
import time
import digitalio
import board
print("Hello")
gp = Gamepad(usb_hid.devices)
print("done")

import wifi
import os
import adafruit_requests
import adafruit_connection_manager


pin0 = digitalio.DigitalInOut(board.GP0)
pin0.direction = digitalio.Direction.INPUT
pin0.pull = digitalio.Pull.DOWN
backlog = []

def log(message):
    backlog.append(message)

ssid = os.getenv("mCIRCUITPY_WIFI_SSID")
password = os.getenv("mCIRCUITPY_WIFI_PASSWORD")

ip = os.getenv("mCIRCUITPY_IP")
port = os.getenv("mCIRCUITPY_PORT")
BASE_URL = "http://"+ip+":"+port
JSON_GET_URL = "/get_status"
LOG_URL = "/log/"
CHECK_URL ="/should_update"
PRESS_URL = "/press_button/"
RELEASE_URL = "/release_button/"
pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
requests = adafruit_requests.Session(pool, ssl_context)


#log(f"\nConnecting to {ssid}...")
try:
    # Connect to the Wi-Fi network
    wifi.radio.connect(ssid, password)
except OSError as e:
    log(f"❌ OSError: {e}")
#log("✅ Wifi!")

def get(url):
    print(f"Get {url}")
    return requests.get(url)

print(BASE_URL+LOG_URL)

def log(message):
    print(message)
    with get(BASE_URL+LOG_URL+message) as response:
        pass



for m in backlog:
    log(m)
print("Success")
dt = 0.05
buttons = [False for i in range(16)]
def getJson(url):
    with get(url) as response:
        return response.json()
def getw(url):
    with get(url) as response:
        pass
def update_gamepad():
    global buttons
    with get(BASE_URL+JSON_GET_URL) as response:
        status = response.json()
        press = []
        release = []
        for i in range(16):
            if status['buttons'][i]:
                press.append(i+1)
            else:
                release.append(i+1)
        buttons = status['buttons']
        gp._press_buttons_internal(*press)
        gp._release_buttons_internal(*release)
        gp._send()
while True:
    with get(BASE_URL+CHECK_URL) as response:
        if (response.json()["should_update"]):
            update_gamepad()
    if buttons[0] and not pin0.value:
        getw(BASE_URL+RELEASE_URL+"1")
    elif not buttons[0] and pin0.value:
        getw(BASE_URL+PRESS_URL+"1")
    # print(pin0.value)
    if pin0.value:
        gp.press_buttons(1)
    else:
        gp.release_buttons(1)
    #time.sleep(dt)