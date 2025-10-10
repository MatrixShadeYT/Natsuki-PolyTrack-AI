import numpy as np
import polytrack
import natsuki
import time

runLen = 5#int(input("TIME (SECS): "))
model = natsuki.imgModel(scale=128)

def program(num):
    x = time.time()
    while time.time() - x < num:
        img = polytrack.get_image(128)
        pred = model.predict(img)[0]
        print(f"PRED: {pred}")
        move = np.argmax(pred)
        print(f"MOVE: {move}")
        polytrack.move(move)

polytrack.runtime(runLen,program)