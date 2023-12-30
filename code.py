import ipaddress
import ssl
import wifi
import socketpool
import adafruit_requests
import time
import json
import board
import terminalio
from adafruit_display_text import bitmap_label

white = 0xFFFFFF
orange = 0xF9580C

# URLs to fetch from
JSON_DATA_URL = 'https://webservices.umoiq.com/api/pub/v1/agencies/sfmta-cis/stopcodes/15018/predictions?key=0be8ebd0284ce712a63f29dcaf7798c4'

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

wifi.radio.connect(secrets["ssid"], secrets["password"])
print("Connected to %s!"%secrets["ssid"])
print("My IP address is", wifi.radio.ipv4_address)

pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

while True:
    response = requests.get(JSON_DATA_URL)
    # response = requests.get(REQ_URL)
    try: 
        for route in response.json(): 
            routeID = route['route']['id']
            if routeID == "22": 
                routeName = route['route']['title']
                first_eta = route['values'][0]['minutes']
                second_eta = route['values'][1]['minutes']
                break
        
        text = f"Next 22: \n{first_eta}, {second_eta}" 
    except: 
        print(response.json())
        text = "Error"

    scale = 4

    text_area = bitmap_label.Label(terminalio.FONT, text=text, scale=scale, color=white)
    text_area.x = 10
    text_area.y = 20
    board.DISPLAY.show(text_area)

    time.sleep(15)