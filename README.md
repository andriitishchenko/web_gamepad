# web_gamepad
WEB based mobile gamepad controller.

Control emulators or games or OS via mobile .
(retroarch, OpenEmu, nes, etc)

MacOs requaried to add Terminal.app to "Security & Privacy" -> "Privacy" -> "Accessibility"



Still three optimizations for the game process: 
* Arrow buttons have been replaced with a joystick;
* Joystick replaced with swipe gestures;


### How to

- Clone repo;

- Install deps
```python
% python3 -m venv web_gamepad
% pip3 install -r requirements.txt
```

1. start server on mac
```python
% python3 server.py
WEB SERVER STARTED
 http://127.0.0.1:8000    - check your local IP
WS SERVER STARTED
 ws://127.0.0.1:8765      - check your local IP
```

 2. navigate to WEB SERVER on your mobile (sacn QR)

 3. connect to WS SERVER IP

```python
Hardcoded keys:
  1: 37, // left
  2: 38, // up
  3: 39, // right
  4: 40, // down
  5: 13, // start . Enter
  6: 9, // select . Tab
  7: 90, // btn a  . Z
  8: 88, // btn b  . X
  9: 65, // btn turbo a. A 
  10:83, // btn turbo b. S
  ```

  ### Known issue 
  Big Sur: Key codes do not work for uppercase letters


### TODO:

0. convert script to app (Automator??)
1. add second gamepad
2. add sega gamepad
3. add qr code for URL to connect