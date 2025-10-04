from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from PIL import Image
import time
import io

def get_image():
    png_bytes = driver.get_screenshot_as_png()
    img = Image.open(io.BytesIO(png_bytes)).convert("RGB")
    return img

def settings_change():
    settings = ActionChains(driver)
    settings.move_by_offset(375,300).click() # (375,300)
    settings.move_by_offset(75,-200).click() # (450,100)
    settings.move_by_offset(140,0).click_and_hold().move_by_offset(0,85).release() # (590,100/185)
    settings.move_by_offset(-210,-120).click().move_by_offset(145,30).click() # (380/465,65/95)
    settings.move_by_offset(0,30).click().move_by_offset(0,30).click().move_by_offset(0,30).click() # (465,95/125/155/185)
    settings.move_by_offset(35,120).click_and_hold().move_by_offset(-210,0).release() # (500/290,305)
    settings.move_by_offset(210,30).click_and_hold().move_by_offset(-210,0).release() # (500/290,335)
    settings.move_by_offset(210,30).click_and_hold().move_by_offset(-210,0).release() # (500/290,365)
    settings.move_by_offset(-290,-365).perform()
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR,"button.button.apply").click()

def setup_map():
    game = ActionChains(driver)
    game.move_by_offset(600,300).click().pause(0.1)
    game.move_by_offset(-450,-150).click().pause(0.1)
    game.move_by_offset(350,250).click().perform()
    time.sleep(0.5)

def game_loop():
    currentKeys = []
    ActionChains(driver).send_keys(",").perform()
    actions = ActionChains(driver)
    for i in range(len(moves)):
        if i != 0:
            key = combos[moves[i]]
            for i in range(len(key)):
                if not key[i] in currentKeys:
                    actions.key_down(keyIndex[key[i]])
                    currentKeys.append(key[i])
            listed = []
            for i in range(len(currentKeys)):
                if not currentKeys[i] in key:
                    actions.key_up(keyIndex[currentKeys[i]])
                    listed.append(currentKeys[i])
            for i in range(len(listed)):
                currentKeys.remove(listed[i])
        else:
            for x in range(len(currentKeys)):
                actions.key_up(currentKeys[x])
            currentKeys = []
        actions.pause(0.01)
    actions.perform()

moves = input("MOVES: ")
if moves == "":
    with open('instructions.txt','r') as file:
        moves = [int(i) for i in list(file.readlines()[0])]
else:
    with open('instructions.txt','w') as file:
        file.write(moves)
    moves = [int(i) for i in list(moves)]
options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
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
    setup_map()
    time.sleep(1)
    game_loop()
    time.sleep(0.01)
    get_image().save("output.png")
finally:
    driver.quit()