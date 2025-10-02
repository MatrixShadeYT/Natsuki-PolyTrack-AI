from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from PIL import Image
import time
import io


with open('instructions.txt','r') as file:
    moves = [int(i) for i in list(file.readlines()[0])]
options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=780,580")
driver = webdriver.Chrome(options=options)

def get_image():
    png_bytes = driver.get_screenshot_as_png()
    img = Image.open(io.BytesIO(png_bytes)).convert("RGB")
    return img

def game_loop():
    game = ActionChains(driver)
    game.move_by_offset(600,300).click().pause(0.01)
    game.move_by_offset(-450,-150).click().pause(0.01)
    game.move_by_offset(350,250).click().perform()
    time.sleep(0.5)
    ActionChains(driver).send_keys(",").perform()
    print("Start Encoding")
    actions = ActionChains(driver)
    actions.key_down(Keys.ARROW_UP)
    for i in range(len(moves)):
        if moves[i] == 1:
            actions.send_keys(Keys.ARROW_LEFT)
        if moves[i] == 2:
            actions.send_keys(Keys.ARROW_RIGHT)
        actions.pause(0.01)
    actions.key_up(Keys.ARROW_UP)
    actions.perform()
    print("End Encoding")

try:
    driver.get("https://www.yoosfuhl.com/game/polytrack/index.html")
    time.sleep(3)
    print("START")
    settings = ActionChains(driver)
    settings.move_by_offset(375,300).click() # (375,300)
    settings.move_by_offset(75,-200).click() # (450,100)
    settings.move_by_offset(140,0).click_and_hold().move_by_offset(0,85).release() # (590,100/185)
    settings.move_by_offset(-210,-120).click().move_by_offset(145,30).click() # (380/465,65/95)
    settings.move_by_offset(0,30).click().move_by_offset(0,30).click().move_by_offset(0,30).click() # (465,95/125/155/185)
    settings.move_by_offset(35,120).click_and_hold().move_by_offset(-210,0).release() # (500/290,305)
    settings.move_by_offset(210,30).click_and_hold().move_by_offset(-210,0).release() # (500/290,335)
    settings.move_by_offset(210,30).click_and_hold().move_by_offset(-210,0).release() # (500/290,365)
    settings.move_by_offset(300,-180).click_and_hold().move_by_offset(0,100).release() # (290/590,365/185/285) THIS ONE ISN'T WORKING
    settings.move_by_offset(-590,-285).perform()
    time.sleep(0.01)
    print("Grabbing Image")
    img = get_image()
    for x in range(9):
        for y in range(9):
            img.putpixel((590+x,185+y),(255,0,0))
            img.putpixel((590+x,285+y),(0,255,0))
    print("Obtained Image")
    img.save("output.png")
    print("Saved Image")
finally:
    driver.quit()