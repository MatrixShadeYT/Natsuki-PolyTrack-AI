from PIL import Image
import numpy as np
import natsuki
import time

model = natsuki.imgModel(outs=9,scale=128)
runLen = 30#int(input("TIME (SECS): "))

print("STARTING...")
import polytrack
def program(num):
    keys = polytrack.move(3)
    prevSpeed = polytrack.get_data()[1]
    time.sleep(1)
    keys = polytrack.move(0,keys)
    x = time.time()
    while time.time() - x < num:
        keys = [i for i in keys]
        img = polytrack.get_image(128)
        pred = model.predict(img)[0]
        print(f"PRED: {pred}")
        move = np.argmax(pred)
        print(f"MOVE: {move}")
        keys = polytrack.move(move,keys,0.05)
        data = polytrack.get_data()
        reward = 100*(int(data[0][0])+int(data[1]-prevSpeed)-1)
        print(f"REWARD: {reward}")
        prevSpeed = data[1]
        model.train(reward)
polytrack.runtime(runLen,program)