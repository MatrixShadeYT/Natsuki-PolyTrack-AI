from tensorflow import keras
from PIL import Image
import numpy as np

class imgModel(natsuki):
    self.type = 'img'
    def __init__(self,file=None,scale=128):
        self.scale = scale
        self.createModel()
        if file:
            self.load(file)
    def createModel(self):
        self.model = keras.Sequential([
            keras.layers.Input(scale,scale,3),
            keras.layers.Conv2D(scale/4,(3,3),activation='relu'),
            keras.layers.MaxPooling2D(),
            keras.layers.Flatten(),
            keras.layers.Dense(scale,activation='relu'),
            keras.layers.Dense(9,activation='sigmoid')
        ])
        self.model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
    def predict(self,img: Image.Image):
        img = self.parseImage(img)
        value = self.model.predict(img)[0]
        return value
    def parseImage(self,img: Image.Image):
        x = (self.scale,self.scale)
        img.resize(x)
        img = np.array(img)/255.0
        img = np.expand_dims(img,axis=0)
        return img
    def save(self,filename):
        self.model.save_weights(f"{filename}.h5")
    def load(self,filename):
        self.model.load_weights(f"{filename}.h5")