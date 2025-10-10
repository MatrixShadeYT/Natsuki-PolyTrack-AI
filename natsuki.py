from tensorflow import keras
import numpy as np

class imgModel:
    def __init__(self,file=None,scale=128):
        self.createModel(scale)
        if file:
            self.load(file)
    def createModel(self,scale):
        self.model = keras.Sequential([
            keras.layers.Input((scale,scale,3)),
            keras.layers.Conv2D(32,(3,3),activation='relu'),
            keras.layers.MaxPooling2D(),
            keras.layers.Flatten(),
            keras.layers.Dense(64,activation='relu'),
            keras.layers.Dense(9,activation='softmax')
        ])
        #self.model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])
    def predict(self,img: np.array):
        value = self.model.predict(img)
        return value
    def save(self,filename):
        self.model.save_weights(f"{filename}.h5")
    def load(self,filename):
        self.model.load_weights(f"{filename}.h5")