# web_gamepad
WEB mobile gamepad controller 

Control emulators or games or OS via mobile .
(retroarch, OpenEmu, nes, etc)

MacOs requaried to add Terminal.app to "Security & Privacy" -> "Privacy" -> "Accessibility"

clone repo

Install deps
% python3 -m venv web_gamepad
$ pip3 install -r requirements.txt


1 start server on mac
% python3 server.py
WEB SERVER STARTED
 http://127.0.0.1:8000    - check your local IP
WS SERVER STARTED
 ws://127.0.0.1:8765      - check your local IP


 2 navigate to WEB SERVER on your mobile

 3 connect to WS SERVER 


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


TODO:
0 convert script to app (Automator??)
1 add second gamepad
2 add sega gamepad