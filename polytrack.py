from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from PIL import Image
import random
import time
import io

def get_image():
    png_bytes = driver.get_screenshot_as_png()
    img = Image.open(io.BytesIO(png_bytes)).convert("RGB")
    return img

def setup_map():
    game = ActionChains(driver)
    game.move_by_offset(600,300).click().pause(0.1)
    game.move_by_offset(-450,-150).click().pause(0.1)
    game.move_by_offset(350,250).click().perform()
    time.sleep(0.5)

def game_loop():
    currentKeys = []
    actions = ActionChains(driver)
    for i in range(len(moves)):
        currentKeys = currentKeys.copy()
        if moves[i] != 0:
            key = combos[moves[i]-1]
            for x in range(len(key)):
                if not key[x] in currentKeys:
                    actions.key_down(keyIndex[key[x]])
                    currentKeys.append(key[x])
            listed = []
            for x in range(len(currentKeys)):
                if not currentKeys[x] in key:
                    actions.key_up(keyIndex[currentKeys[x]])
                    listed.append(currentKeys[x])
            for x in range(len(listed)):
                currentKeys.remove(listed[x])
        else:
            currentKeys = currentKeys.copy()
            for x in range(len(currentKeys)):
                actions.key_up(currentKeys[x])
            currentKeys = []
        actions.pause(0.25)
    actions.perform()
with open('instructions.txt','r') as file:
    moves = [int(i) for i in list(file.readlines()[0])]
valuable = f"{random.randint(1000000000000000000000000000000,99999999999999999999999999999999999999999999999999999999999999)}".replace('9',f"{random.randint(0,8)}")
moves = input(f"PREVIOUS: {moves}\nVALUABLE:{valuable}\nMOVES (can skip to use previous): ").replace('value',valuable)
show = input("SHOW SCREEN (YES to show): ")
if moves != "":
    with open('instructions.txt','w') as file:
        file.write(moves)
    moves = [int(i) for i in list(moves)]
options = Options()
if show != "yes":
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
    ["s"],
    ["w"],
    ["a","w"],
    ["d","w"],
    ["a","s","w"],
    ["d","s","w"]
]

try:
    driver.get("https://www.yoosfuhl.com/game/polytrack/index.html")
    time.sleep(3)
    print("setup")
    setup_map()
    time.sleep(2)
    print("game")
    game_loop()
    time.sleep(1)
    print("image")
    get_image().save("output.png")
    print("done")
finally:
    driver.quit()