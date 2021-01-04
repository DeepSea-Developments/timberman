#-----------------------
# Libraries 
# ----------------------

from ppadb.client import Client
import numpy as np
import time
import mss
import mss.tools
import cv2

def tap(dir):

    if dir: #Right
        phone.shell('input tap 850 1400')
    else:
        phone.shell('input tap 250 1400')


def GrabImage(Pos):
    if Pos: #Right
        box = {'top': 635, 'left': 638, 'width': 50, 'height':100}
    else:
        box = {'top': 635, 'left': 403, 'width': 50, 'height': 100}

    img = sct.grab(box)
    img = np.array(img)

    GrayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    return int(GrayImg.sum())



#-------------------------------
# Connection to Android Phone
#-------------------------------

client = Client(host="127.0.0.1", port=5037)
phones = client.devices()
phone = phones[0]

#-------------------------------
# Initial Parameters
#-------------------------------
sct = mss.mss()
Pos = 0 # Position indicator
change = 0  # Change Flag
Ima0 = GrabImage(Pos) # Initial image to compare sequence
tap(0) # Start the game

#-----------------------------
# Main
#-----------------------------

while True:
    Ima1 = GrabImage(Pos)

    if change == 1:
        Ima0 = Ima1
        change = 0

    val = abs(Ima1 - Ima0)
    print(f"{Ima0},{Ima1},{val}")
    if val > 5000:
        change = 1
        if Pos == 0:
            Pos = 1
        else:
            Pos = 0

    if Pos:
        print("Position: right")
    else:
        print("Position: left")

    Ima0 = Ima1
    #time.sleep(0.5)
    tap(Pos)