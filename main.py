import numpy as np
import natsuki
import time

runLen = int(input("TIME (SECS): "))
model = natsuki.imgModel(scale=128)

import polytrack

def program(num):
    polytrack.move(4)
    prevSpeed = polytrack.get_data()[1]
    x = time.time()
    while time.time() - x < num:
        img = polytrack.get_image(128)
        pred = model.predict(img)[0]
        print(f"PRED: {pred}")
        move = np.argmax(pred)
        print(f"MOVE: {move}")
        polytrack.move(move)
        data = polytrack.get_data()
        reward = 100*(int(data[0][0])+int(data[1]-prevSpeed))
        prevSpeed = data[1]
        model.train(reward)

polytrack.runtime(runLen,program)