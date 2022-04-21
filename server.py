#!/usr/bin/env python
import sys
import asyncio
import websockets

import http.server
import socketserver
from threading import Thread

import socket
import json

from pynput.keyboard import Key, Controller,KeyCode
import time

import qrcode


PORT = 8000
WSPORT = 8765

# https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent/keyCode
keyCodeMap = {
  37:Key.left,
  38:Key.up,
  39:Key.right,
  40:Key.down, 
  13:Key.enter,
  9: Key.tab, 
  90:KeyCode.from_char("z"), #  btn a  . Z
  88:KeyCode.from_char("x"), #  btn b  . X
  65:KeyCode.from_char("a"), #  btn turbo a . A 
  83:KeyCode.from_char("s"), #  btn turbo b. S
}

keyboard = Controller()
def pressKeyboardCode(key, isKyeUp=False):
    global keyCodeMap
    # print(f"{key} {isKyeUp}")
    vk = keyCodeMap[key]
    if isKyeUp:
        keyboard.release(vk)
    else:
        keyboard.press(vk)



st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:       
    st.connect(('8.8.8.8', 1))
    local_ip = st.getsockname()[0]
except Exception:
    local_ip = '127.0.0.1'
finally:
    st.close()

# = = = = = = ==  ==  
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(f"http://{local_ip}:{PORT}")
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
img.show()
# = = = = = = ==  ==  

keyState = {}


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # self.path = f'index.html'
            self.path = f'v2.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

async def echo(websocket):
    global keyState
    try:
        async for message in websocket:
            keyState = json.loads(message)
            await websocket.send("1")
    except:
        pass

def monitor_thread():
    handler_object = MyHttpRequestHandler 
    try:
        with socketserver.TCPServer(("", PORT), handler_object) as httpd:
            print( f"WEB SERVER STARTED\n http://{local_ip}:{PORT}" )
            httpd.serve_forever()
    except:
        pass

def keydown_thread():
    global keyState
    procesed={}

    try:
        while True:
            for k, v in keyState.items():
                key = int(k)
                isEvent = False

                if k in procesed:
                    p_v = procesed[k]
                    
                    if p_v != v or v == 1:
                        procesed[k] = v
                        isEvent = True                    
                else:
                    if v == 1:
                        isEvent = True
                    procesed[k] = v
                    
                if isEvent:
                    pressKeyboardCode(key, v == 0 )
            time.sleep(0.1)
    except:
        pass


async def main():
    Thread(target=monitor_thread, daemon=True).start()
    Thread(target=keydown_thread, daemon=True).start()
    try:
        async with websockets.serve(echo, "", WSPORT):
            print( f"WS SERVER STARTED\n ws://{local_ip}:{WSPORT}" )
            await asyncio.Future()  # run forever
    except:
        pass

asyncio.run(main())
