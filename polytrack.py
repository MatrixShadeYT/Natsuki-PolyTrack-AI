from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from PIL import Image
import numpy as np
import time
import io

options = Options()
options.add_argument("--headless=new")
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
    try:
        data = driver.execute_script("return 'x,y'.replace('x',document.querySelector('.checkpoint>div>span').innerHTML).replace('y',document.querySelector('.speedometer>div>span').innerHTML)")
        data = data.split(',')
    except Exception as e:
        print(f"ERR: {e}")
        data = ['0/3','<span>0</span>']
    speed = int(data[1].replace('<span>','').replace('</span>',''))
    checkpoints = [int(i) for i in data[0].split('/')]
    print(f"Checkpoints: {checkpoints}\nSpeed: {speed}")
    return [checkpoints,speed]

def move(num,currentKeys=[],wait=0.01):
    currentKeys = [i for i in currentKeys]
    x = ActionChains(driver)
    listed = []
    for i in currentKeys:
        if not i in combos[num-1]:
            x.key_up(keyIndex[i])
            listed.append(i)
    for i in listed:
        currentKeys.remove(i)
    if num != 0:
        for i in combos[num-1]:
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
    finally:
        driver.quit()