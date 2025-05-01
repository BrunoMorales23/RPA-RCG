from RPA.Browser.Selenium import Selenium
import random
import cv2
import time
from PIL import Image, ImageDraw
from colorama import Fore

def generate_number(limit):
    integer = (random.randrange((-1*int(limit)),limit))
    decimal = (random.randrange(1,99999999))
    final_number = str(integer) + '.' + str(decimal)
    return final_number

browser = Selenium()
umbral = 0.7
match = False

while match == False:

    latitude = float(generate_number(90))
    lenght = float(generate_number(180))

    url = "https://www.google.com/maps/place/@"+str(latitude)+','+str(lenght)+',10z'
    browser.open_available_browser(url=url, headless=False, browser_selection='chrome')
    time.sleep(1)
    browser.capture_page_screenshot('./outputs/screenshot.png')
    browser.close_browser()

    img = cv2.imread('./outputs/screenshot.png',cv2.IMREAD_GRAYSCALE)
    water_template = cv2.imread('./templates/water_template.png', cv2.IMREAD_GRAYSCALE)
    water_template_w_extras = cv2.imread('./templates/water_template_w_extras.png', cv2.IMREAD_GRAYSCALE)

    result = cv2.matchTemplate(img, water_template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val <= umbral:
        print(Fore.RED , max_val)
        print('---------------------------')
        result = cv2.matchTemplate(img, water_template_w_extras, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val <= umbral:
            print(Fore.RED , max_val)
            print('---------------------------')
            match = True
        else:
            browser.close_all_browsers()
    else: 
        browser.close_all_browsers()

print(Fore.GREEN + f"¡Tierra encontrada!")
url = "https://www.google.com/maps/place/@"+str(latitude)+','+str(lenght)+',3z'
browser.open_available_browser(url=url, headless=True, browser_selection='chrome')
browser.capture_page_screenshot('./outputs/final_screenshot.png')
final_img = Image.open('./outputs/final_screenshot.png')

width, height = final_img.size
center_x, center_y = width // 2, height // 2

radio = 15

box = (
    center_x - radio,
    center_y - radio,
    center_x + radio,
    center_y + radio
)

draw = ImageDraw.Draw(final_img)
draw.ellipse (box, fill="red", outline="red", width=1)
final_img.show()
final_img.save('./outputs/final_screenshot.png')
browser.close_all_browsers()