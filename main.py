from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from keras.preprocessing.image import img_to_array
from selenium import webdriver
import numpy as np
import keras
import time
import PIL
import io

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=780,580")
driver = webdriver.Chrome(options=options)
model = keras.Sequential([
    keras.layers.Conv2D(32,(3,3),activation='relu',input_shape=(780,580,3)),
    keras.layers.MaxPooling2D((2,2)),
    keras.layers.Conv2D(64,(3,3),activation='relu'),
    keras.layers.MaxPooling2D((2,2)),
    keras.layers.Conv2D(128,(3,3),activation='relu'),
    keras.layers.MaxPooling2D((2,2)),
    keras.layers.Flatten(),
    keras.layers.Dense(128,activation='relu')
    keras.layers.Dense(2,activation='softmax')
])
model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])
model.summary()

def process(img):
    img = img.resize((780,580))
    img_array = img_to_array(img)
    img_array = img_array.astype("float32")/255.0
    img_array = np.expand_dims(img_array,axis=0)
    return model.predict(img_array)

def get_image():
    png_bytes = driver.get_screenshot_as_png()
    img = PIL.Image.open(io.BytesIO(png_bytes)).convert("RGB")
    return img

def loop(time,dist):
    for i in range(time):
        img = get_image()
        pred = process(img)
        size = driver.get_window_size()
        ActionChains(driver).move_by_offset(size['width'],size['height']).click().move_by_offset((size['width']*-1),(size['height']*-1)).perform()
        time.sleep(dist)

try:
    driver.get("https://webosu.online/search.html?q=2382142")
    time.sleep(5)
    ActionChains(driver).move_by_offset(300,265).click().pause(1).click().move_by_offset(-300,-265).perform()
    time.sleep(10)
    loop(600,0.1)
    png_bytes = driver.get_screenshot_as_png()
    PIL.Image.open(io.BytesIO(png_bytes)).show()
finally:
    driver.quit()