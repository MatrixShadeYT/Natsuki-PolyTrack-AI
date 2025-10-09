from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from PIL import Image
import random
import time
import os
import io

if os.path.exists('polytrack.txt'):
    with open('polytrack.txt','r') as file:
        moves = [int(i) for i in list(file.readlines()[0])]
else:
    moves = '0'
valuable = f"{random.randint(1000000000000000000000000000000,99999999999999999999999999999999999999999999999999999999999999)}".replace('9',f"{random.randint(0,8)}")
x = ""
for i in range(len(moves)):
    x = f"{x}{moves[i]}"
choiceMoves = input(f"VALUABLE (type value): {valuable}\nPREVIOUS: {x}\nMOVES (blank/previous): ").replace('value',valuable)
show = input("SHOW SCREEN (YES/web, NO/save, other/show): ")
if choiceMoves != "":
    with open('polytrack.txt','w') as file:
        file.write(choiceMoves)
    moves = [int(i) for i in list(choiceMoves)]
else:
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

def commands(cmds):
    currentKeys = []
    actions = ActionChains(driver)
    for i in range(len(cmds)):
        currentKeys = currentKeys.copy()
        if cmds[i] != 0:
            key = combos[cmds[i]-1]
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
        actions.pause(0.2)
    return actions

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

try:
    driver.get("https://www.yoosfuhl.com/game/polytrack/index.html")
    time.sleep(3.1)
    setup_map()
    time.sleep(2)
    commands(moves).perform()
    time.sleep(1)
    if show == "no":
        get_image().save("polytrack.png")
    elif show == "yes":
        data = [i for i in get_data()]
        print(f"Checkpoints: {data[0][0]}/{data[0][1]}\nSpeed: {data[1]}")
    else:
        get_image().show()
finally:
    driver.quit()