from PIL import Image
import numpy as np
import natsuki
import time

model = natsuki.imgModel(outs=8,scale=128)
runLen = int(input("TIME (SECS): "))

print("STARTING...")
import polytrack
def program(num):
    totalRewards = 0
    running = False
    keys = polytrack.move(3)
    prevSpeed = 0
    keys = polytrack.move(0,keys)
    x = time.time()
    while running or time.time() - x < num:
        running = True
        keys = [i for i in keys]
        img = polytrack.get_image(128)
        pred = model.predict(img)[0]
        print(f"PRED: {pred}")
        move = np.argmax(pred)
        print(f"MOVE: {move}")
        keys = polytrack.move(move,keys,0.05)
        data = polytrack.get_data()
        reward = 100*(int(data[0][0])+int(data[1]-prevSpeed)-1)
        print(f"REWARD: {reward}\n")
        totalRewards += reward
        prevSpeed = data[1]
        model.train(reward)
        running = False
    print(f"DATA\nTOTAL REWARDS: {totalRewards}")
    data = polytrack.get_data()
polytrack.runtime(runLen,program)