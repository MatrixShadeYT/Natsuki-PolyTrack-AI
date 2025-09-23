from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from PIL import Image
import time
import io

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=780,580")
driver = webdriver.Chrome(options=options)

def get_image():
    png_bytes = driver.get_screenshot_as_png()
    img = Image.open(io.BytesIO(png_bytes)).convert("RGB")
    return img

try:
    driver.get("https://webosu.online/search.html?q=2382142")
    time.sleep(5)
    ActionChains(driver).move_by_offset(300,265).click().pause(1).click().move_by_offset(-300,-265).perform()
    time.sleep(15)
    img = get_image()
    img.show()
finally:
    driver.quit()