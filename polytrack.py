from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from PIL import Image
import pytesseract
import numpy as np
import time
import io

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
options = Options()
#options.add_argument("--headless=new")
options.add_argument("--window-size=780,580")
driver = webdriver.Chrome(options=options)

keyIndex = {
    "a": Keys.ARROW_LEFT,
    "d": Keys.ARROW_RIGHT,
    "s": Keys.ARROW_DOWN,
    "w": Keys.ARROW_UP
}
combos = [
    ["a"],
    ["d"],
    ["w"],
    ["a","w"],
    ["d","w"],
    ["a","s","w"],
    ["d","s","w"]
]

def setup_map():
    game = ActionChains(driver)
    game.move_by_offset(600,300).click().pause(0.1)
    game.move_by_offset(-450,-150).click().pause(0.1)
    game.move_by_offset(350,250).click().perform()
    time.sleep(0.5)

def get_image(scale=None):
    png_bytes = driver.get_screenshot_as_png()
    img = Image.open(io.BytesIO(png_bytes)).convert("RGB")
    if scale:
        img = img.resize((scale,scale))
        img = np.array(img)/255.0
        img = np.expand_dims(img,axis=0).astype(np.float32)
    return img

def get_data():
    base_img = get_image()
    img = base_img.crop((1035,615,1100,640))
    text = pytesseract.image_to_string(img)
    speed = int(text)
    img = base_img.crop((40,612,100,642))
    text = pytesseract.image_to_string(img)
    checkpoints = [int(i) for i in text.split('/')]
    return [checkpoints,speed]

def move(num,currentKeys=[],wait=0.01):
    currentKeys = [i for i in currentKeys]
    x = ActionChains(driver)
    listed = []
    for i in currentKeys:
        if not i in combos[num]:
            x.key_up(keyIndex[i])
            listed.append(i)
    for i in listed:
        currentKeys.remove(i)
    if num != 0:
        num -= 1
        for i in combos[num]:
            if not i in currentKeys:
                x.key_down(keyIndex[i])
                currentKeys.append(i)
    print(currentKeys)
    x.pause(wait).perform()
    return currentKeys

def runtime(num,func):
    try:
        driver.get("https://www.yoosfuhl.com/game/polytrack/index.html")
        time.sleep(3.1)
        setup_map()
        time.sleep(3)
        print('\nSYS')
        func(num)
        time.sleep(1)
        print('\nDATA')
        data = get_data()
        print(f"Checkpoints: {data[0][0]}/{data[0][1]}\nSpeed: {data[1]}")
    finally:
        driver.quit()