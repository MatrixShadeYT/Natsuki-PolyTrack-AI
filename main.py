import polytrack
import natsuki
import time

runLen = 5#int(input("TIME (SECS): "))
model = natsuki.imgModel(scale=128)

def program(num):
    x = time.time()
    while time.time() - x < num:
        img = polytrack.get_image(128)
        pred = model.predict(img)
        print(f"PRED: {pred[0]}")

polytrack.runtime(runLen,program)