#using adbapiv2
import sys
import os
# Get the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the parent directory to sys.path
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from adbapi2 import Emulator, Phone, ImageOcr
from randomxy import get_random_tap, get_random_swipe
from PIL import ImageOps
import time as t
from elementlist import are_n_elements_present_set
import math

id = input("Id\nLeave blank for auto connect {5554}\n")
device = Emulator(id, -1) #port, number of devices
#slide coordiantes
x1,y1,x2,y2 = 1000,1170,1040,250
res_scalar_x = device.abs_res_scalar_x
res_scalar_y = device.abs_res_scalar_y
key_words = ['repeat','battling','has','ended.','ended']

def attempt_tap(ocr_instance, device, target_text: str, mode: str = "first", offset: int = 0):
    coordinates = ocr_instance.locate_text(target_text)
    if coordinates:
        selected = None
        if mode == "first":
            selected = coordinates[0]
        elif mode == "last":
            selected = coordinates[-1]

        try:
            x, y = get_random_tap(*selected)
            device.screenInput(x, y+offset)
            print(f"Tapped '{target_text}' ({mode}) at ({x}, {y+offset})")
            return True
        except Exception as e:
            print(f"Error tapping on '{target_text}': {e}")
            return False
    else:
        print(f"No coordinates found for '{target_text}'")
        return False
    
def get_ocr():
    im = device.screenshot()
    ocr = ImageOcr(im)
    return ocr

def get_ocr_crop():
    im = device.screenshot()
    im = ImageOcr(im).crop_image(0,0,1920,1020 ,res_scalar_x,res_scalar_y)
    ocr = ImageOcr(im)
    return ocr


try:
    gems = int(input("gems:"))
    if(gems == 0):
        raise ValueError("Encountered 0 value")

    amount_gems = gems #amount of gems to roll
    rolls = int(amount_gems/3)
except:
    raise TypeError("Int")

expected_covenant_summons = math.floor((gems*5/71)/5)*5
expected_mystic_summons = math.floor((gems*50/266)/50)*50

covenant_summons = 0
mystic_summons = 0
for roll in range(rolls):
    t.sleep(1)
    if(attempt_tap(get_ocr_crop(), device, ["184,000","184000"], mode="last", offset=75)):
        t.sleep(1)
        while True:
            if(attempt_tap(get_ocr(), device, "Buy", mode="last", offset=0)): 
                covenant_summons += 5 
                break
            else:
                attempt_tap(get_ocr(), device, ["184,000","184000"], mode="last", offset=75)
            t.sleep(0.3)
            

    if(attempt_tap(get_ocr_crop(), device, ["280,000","280000"], mode="last", offset=75)):
        t.sleep(1)
        while True:
            if(attempt_tap(get_ocr(), device, "Buy", mode="last", offset=0)): 
                mystic_summons += 50
                break
            else:
                attempt_tap(get_ocr(), device, ["280,000","280000"], mode="last", offset=75)
            t.sleep(0.3)

    x1_swipe,y_swipe1,x2_swipe,y2_swipe=get_random_swipe(x1,x2,y1,y2)
    device.screenSwipe(x1_swipe,y_swipe1,x2_swipe,y2_swipe)
    t.sleep(1)

    if(attempt_tap(get_ocr(), device, ["184,000","184000"], mode="last", offset=75)):
        t.sleep(1)
        while True:
            if(attempt_tap(get_ocr(), device, "Buy", mode="last", offset=0)): 
                covenant_summons += 5
                break
            else:
                attempt_tap(get_ocr(), device, ["184,000","184000"], mode="last", offset=75)
            t.sleep(0.3)


    if(attempt_tap(get_ocr(), device, ["280,000","280000"], mode="last", offset=75)):
        t.sleep(1)
        while True:
            if(attempt_tap(get_ocr(), device, "Buy", mode="last", offset=0)): 
                mystic_summons += 50
                break
            else:
                attempt_tap(get_ocr(), device, ["280,000","280000"], mode="last", offset=75)
            t.sleep(0.3)

    while True:
        if(attempt_tap(get_ocr(), device, "Refresh", mode="last", offset=0)):
            t.sleep(1)
            while True:
                if(attempt_tap(get_ocr(), device, "Confirm", mode="last", offset=0)): break
                else: 
                    attempt_tap(get_ocr(), device, "Refresh", mode="last", offset=0) 
                    continue
                    
            print(f"Refresh {roll+1} completed")
            print(f"Total Mystic Summons: {mystic_summons} - expected: {expected_mystic_summons}")
            print(f"Total Covenant Summons: {covenant_summons} - excpected: {expected_covenant_summons}")

            t.sleep(0.5)
            break
        else:
            if not attempt_tap(get_ocr(), device, "Confirm", mode="last", offset=0): break #error correction
            t.sleep(0.3)