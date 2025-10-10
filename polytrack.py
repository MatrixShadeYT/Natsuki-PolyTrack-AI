from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from threading import Thread
from PIL import Image
import numpy as np
import time
import io

options = Options()
#options.add_argument("--headless=new")
options.add_argument("--window-size=780,580")
driver = webdriver.Chrome(options=options)

currentKeys = []
keyIndex = {
    "a": Keys.ARROW_LEFT,
    "d": Keys.ARROW_RIGHT,
    "s": Keys.ARROW_DOWN,
    "w": Keys.ARROW_UP
}
combos = [
    ["a"],
    ["d"],
    ["s"],
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
    checkpoints = [i for i in driver.execute_script("return document.getElementsByClassName('checkpoint')[0].children[0].children[1].innerHTML").split('/')]
    speed = 0
    length = int(driver.execute_script("return document.getElementsByClassName('speedometer')[0].children[0].children[0].children.length;"))
    li = [[1],[10,1],[100,10,1],[1000,100,10,1]]
    for i in range(length):
        time.sleep(0.1)
        val = driver.execute_script(f"return document.getElementsByClassName('speedometer')[0].children[0].children[0].children[{i}].innerHTML")
        speed += li[length-1][i]*int(val)
    return [checkpoints,speed]

def move(num,wait=0.01):
    x = ActionChains(driver)
    if num == 0:
        for i in range(len(currentKeys)):
            x.key_up(currentKeys[i])
    else:
        for i in range(len(currentKeys)):
            if not currentKeys[i] in combos[num]:
                x.key_up(currentKeys[i])
        for i in range(len(combos[num])):
            if not combos[num][i] in currentKeys:
                x.key_down(combos[num][i])
    x.pause(wait).perform()

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