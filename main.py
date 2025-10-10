import polytrack
import natsuki
import time

runLen = int(input("TIME (SECS): "))
model = natsuki.imgModel(scale=128)

def program(*args):
    x = time.time()
    while time.time() - x < args[0]:
        img = polytrack.get_image()
        pred = model.predict(img)
        move = pred.index(max(pred))
        polytrack.move(move)

while True:
    polytrack.runtime(runLen,program)