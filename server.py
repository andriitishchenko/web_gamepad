#!/usr/bin/env python
import sys
import asyncio
# from turtle import right
import websockets

import http.server
import socketserver
from threading import Thread

import socket
import json


from pynput.keyboard import Key, Controller,KeyCode
import time

# https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent/keyCode
keyCodeMap = {
  37:Key.left,
  38:Key.up,
  39:Key.right,
  40:Key.down, 
  13:Key.enter,
  9: Key.tab, 
  90:KeyCode.from_char("Z"), #  btn a  . Z
  88:KeyCode.from_char("X"), #  btn b  . X
  65:KeyCode.from_char("A"), #  btn turbo a . A 
  83:KeyCode.from_char("S"), #  btn turbo b. S
}

keyboard = Controller()
def pressKeyboardCode(key, isKyeUp=False):
    global keyCodeMap
    # print(f"{key}")
    vk = keyCodeMap[key]
    if isKyeUp:
        keyboard.release(vk)
    else:
        keyboard.press(vk)

PORT = 8000

WSPORT = 8765

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)


keyState = {}


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = f'index.html'
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


# a = 122
# print(a)
# k = hex(a)
# print(k)

# print(int(90, 16))
# kk = KeyCode.from_vk(int(k, 16))
# # kk = KeyCode.from_vk(0x5a)
# print(kk)

# k2 = KeyCode.from_char("z")
# print(k2)

# k4 = KeyCode.from_vk(Key.down)
# print(k4.vk)

# for k in range(0, 256) :
#     k3 = KeyCode.from_vk(hex(k))
#     k4 = KeyCode.from_vk(Key.down)

#     # print(f"{k}    {k3} ==== {k4}")

#     if k3 == k4:
#         print(k)


# vv = Key.up.value
# print(vv)

# print(hex(int(vv))
# print(chr(vv))



# k3 = KeyCode.from_vk(Key.up)
# k3 = KeyCode.from_vk(int('0x5a', 16) )
# k3 = KeyCode.from_char(chr(13))
# k3 = KeyCode.from_char("z")
# print(k3)

# keyboard.press(Key.up)
# keyboard.press(k3)
# keyboard.press(k3)
# keyboard.press(k3)
# keyboard.press(k3)
# keyboard.press(k3)
# keyboard.press(k3)
# keyboard.press(k3)

# keyboard.release(k3)

# # if kk == KeyCode.from_char("z"):
# #     print("EQAL")

