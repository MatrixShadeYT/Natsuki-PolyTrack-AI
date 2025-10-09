from tensorflow import keras
from PIL import Image
import numpy as np

class natsuki:
    self.type = null

class imgModel(natsuki):
    self.type = 'img'
    def __init__(self,scale=128):
        self.scale = scale
        self.model = keras.Sequential([
            keras.layers.Input(scale,scale,3),
            keras.layers.Conv2D(32,(3,3)
        ])
    def parseImage(self,img):
        img.resize(self.scale)
        return img