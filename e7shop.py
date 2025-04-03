import os
import sys
# Get the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the parent directory to sys.path
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from adbapi2 import Emulator, Phone, ImageOcr
from randomxy import get_random_tap, get_random_swipe
from PIL import ImageOps
import time as t

def convert_seconds_to_hhmmss(seconds):
    return t.strftime("%H:%M:%S", t.gmtime(seconds))

id = input("Id\nLeave blank for auto connect {5554}\n")
device = Emulator(id, -1) #port, number of devices
exit()
#slide coordiantes
x1,y1,x2,y2 = 1000 ,1170,1040,250


#refresh coordinates
x1_refresh,y1_refresh,x2_refresh,y2_refresh = 130,975,520,1010
x1_refresh_confirm,y1_refresh_confirm,x2_refresh_confirm,y2_refresh_confirm = 1000,670,1135,680

#shop location coordinates, +220 ydir
#for tesseract, remember to scale
shop1_x1, shop1_y1, shop1_x2, shop1_y2 = 1670, 130, 1870, 200
shop2_x1, shop2_y1, shop2_x2, shop2_y2 = 1670, 345, 1870, 420
shop3_x1, shop3_y1, shop3_x2, shop3_y2 = 1670, 565, 1870, 640
shop4_x1, shop4_y1, shop4_x2, shop4_y2 = 1670, 785, 1870, 860

shop5_x1, shop5_y1, shop5_x2, shop5_y2 = 1670, 670, 1870, 745
shop6_x1, shop6_y1, shop6_x2, shop6_y2 = 1670, 890, 1870, 965

#shop purchase location coordinates, +220 ydir
shop_buy_confirm_x1,shop_buy_confirm_y1,shop_buy_confirm_x2,shop_buy_confirm_y2 = 888,735,1275,795
shop1_buy_x1, shop1_buy_y1, shop1_buy_x2, shop1_buy_y2 = 1605, 215, 1850, 270
shop2_buy_x1, shop2_buy_y1, shop2_buy_x2, shop2_buy_y2 = 1605, 435, 1850, 490
shop3_buy_x1, shop3_buy_y1, shop3_buy_x2, shop3_buy_y2 = 1605, 655, 1850, 710
shop4_buy_x1, shop4_buy_y1, shop4_buy_x2, shop4_buy_y2 = 1605, 875, 1850, 930

shop5_buy_x1, shop5_buy_y1, shop5_buy_x2, shop5_buy_y2 = 1605, 760, 1850, 815
shop6_buy_x1, shop6_buy_y1, shop6_buy_x2, shop6_buy_y2 = 1605, 980, 1850, 1025

#start of script
gems = input("gems:")
amount_gems = gems #amount of gems to roll
covenant_summons = 0
mystic_summons = 0
rolls = int(amount_gems/3)
for roll in range(rolls):
    #shop images, first 4
    start = t.time()
    im = device.screenshot()
    res_scalar_x = 1#device.abs_res_scalar_x
    res_scalar_y = 1#device.abs_res_scalar_y

    #shop1_im = im.crop((shop1_x1, shop1_y1, shop1_x2, shop1_y2))
    #shop2_im = im.crop((shop2_x1, shop2_y1, shop2_x2, shop2_y2))
    #shop3_im = im.crop((shop3_x1, shop3_y1, shop3_x2, shop3_y2))
    #shop4_im = im.crop((shop4_x1, shop4_y1, shop4_x2, shop4_y2))

    shop1_im = ImageOcr(im).crop_image(shop1_x1, shop1_y1, shop1_x2, shop1_y2,res_scalar_x,res_scalar_y)
    shop2_im = ImageOcr(im).crop_image(shop2_x1, shop2_y1, shop2_x2, shop2_y2,res_scalar_x,res_scalar_y)
    shop3_im = ImageOcr(im).crop_image(shop3_x1, shop3_y1, shop3_x2, shop3_y2,res_scalar_x,res_scalar_y)
    shop4_im = ImageOcr(im).crop_image(shop4_x1, shop4_y1, shop4_x2, shop4_y2,res_scalar_x,res_scalar_y)

    shop1_im = ImageOps.grayscale(shop1_im)
    shop2_im = ImageOps.grayscale(shop2_im)
    shop3_im = ImageOps.grayscale(shop3_im)
    shop4_im = ImageOps.grayscale(shop4_im)

    shop1_text = ImageOcr(shop1_im).get_text()
    shop2_text = ImageOcr(shop2_im).get_text()
    shop3_text = ImageOcr(shop3_im).get_text()
    shop4_text = ImageOcr(shop4_im).get_text()
    shop_text_list = [shop1_text,shop2_text,shop3_text,shop4_text]
    shop_text_list_new = [] #error correction
    for i in shop_text_list:
        if(i == ['1', '84,000'] or i == ['1', '84,', '000']):
            shop_text_list_new.append('184,000')
        elif(i == ['2', '80,000'] or i == ['2', '80,', '000']):
            shop_text_list_new.append('280,000')
        else:
            shop_text_list_new.append(i)

    for n,item in enumerate(shop_text_list_new):
        buy = False
        if('184,000' in item):
            covenant_summons += 5
            buy = True
        if('280,000' in item):
            mystic_summons += 50
            buy = True

        if(buy == True):
            x_buy, y_buy = get_random_tap(shop1_buy_x1, (shop1_buy_y1+220*n), shop1_buy_x2, (shop1_buy_y2+220*n))
            device.screenInput(x_buy,y_buy)
            t.sleep(0.9)
            x_buy_confirm, y_buy_confirm = get_random_tap(shop_buy_confirm_x1,shop_buy_confirm_y1,shop_buy_confirm_x2,shop_buy_confirm_y2)
            device.screenInput(x_buy_confirm,y_buy_confirm)
            t.sleep(0.5)
        else:
            print(f'Shop: {n+1} Price: {item}')

        t.sleep(0.6)

    #swipe
    x1_swipe,y_swipe1,x2_swipe,y2_swipe=get_random_swipe(x1,x2,y1,y2)
    device.screenSwipe(x1_swipe,y_swipe1,x2_swipe,y2_swipe)
    t.sleep(2)
    im2 = device.screenshot()

    shop5_im = ImageOcr(im2).crop_image(shop5_x1, shop5_y1, shop5_x2, shop5_y2,res_scalar_x,res_scalar_y)
    shop6_im = ImageOcr(im2).crop_image(shop6_x1, shop6_y1, shop6_x2, shop6_y2,res_scalar_x,res_scalar_y)

    shop5_im = ImageOps.grayscale(shop5_im)
    shop6_im = ImageOps.grayscale(shop6_im)

    shop5_text = ImageOcr(shop5_im).get_text()
    shop6_text = ImageOcr(shop6_im).get_text()

    shop_text_list = [shop5_text,shop6_text]
    shop_text_list_new = [] #error correction
    for i in shop_text_list:
        if(i == ['1', '84,000'] or i == ['1', '84,', '000']):
            shop_text_list_new.append('184,000')
        elif(i == ['2', '80,000'] or i == ['2', '80,', '000']):
            shop_text_list_new.append('280,000')
        else:
            shop_text_list_new.append(i)

    for n,item in enumerate(shop_text_list_new):
        buy = False
        if('184,000' in item):
            covenant_summons += 5
            buy = True
        if('280,000' in item):
            mystic_summons += 50
            buy = True

        if(buy == True):
            x_buy, y_buy = get_random_tap(shop5_buy_x1, (shop5_buy_y1+220*n), shop5_buy_x2, (shop5_buy_y2+220*n))
            device.screenInput(x_buy,y_buy)
            t.sleep(0.9)
            x_buy_confirm, y_buy_confirm = get_random_tap(shop_buy_confirm_x1,shop_buy_confirm_y1,shop_buy_confirm_x2,shop_buy_confirm_y2)
            device.screenInput(x_buy_confirm,y_buy_confirm)
            t.sleep(0.5)
        else:
            print(f'Shop: {n+5} Price: {item}')

        t.sleep(0.6)
    
    #shop1_im.save('shop1.png')
    #shop2_im.save('shop2.png')
    #shop3_im.save('shop3.png')
    #shop4_im.save('shop4.png')
    #shop5_im.save('shop5.png')
    #shop6_im.save('shop6.png')
    #exit() #for testing purposes
    
    #refresh shop
    #updated for reliability
    x_refresh_random,y1_refresh_random = get_random_tap(x1_refresh,y1_refresh,x2_refresh,y2_refresh)
    device.screenInput(x_refresh_random,y1_refresh_random)
    t.sleep(1)
    x_refresh_confirm_random,y1_refresh_confirm_random = get_random_tap(x1_refresh_confirm,y1_refresh_confirm,x2_refresh_confirm,y2_refresh_confirm)
    device.screenInput(x_refresh_confirm_random,y1_refresh_confirm_random)

    end = t.time()
    print(f'Rolled: {roll+1}/{rolls}')
    print(f'Covenant medals: {covenant_summons}')
    print(f'Mystic medals: {mystic_summons}')
    print(f'Time left: {convert_seconds_to_hhmmss((end-start)*(rolls-roll+1))}')
    print(f'Cycle: {end-start}')
    t.sleep(4)