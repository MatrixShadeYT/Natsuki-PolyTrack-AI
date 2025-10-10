from tensorflow import keras
import tensorflow as tf
import numpy as np

def reward_loss(y_true,y_pred):
    return -reduce_mean(y_true*math.log(y_pred+1e-10))

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
        self.model.optimizer = keras.optimizers.Adam()
    def predict(self,img: np.array):
        value = self.model.predict(img)
        return value
    def save(self,filename):
        self.model.save_weights(f"{filename}.h5")
    def load(self,filename):
        self.model.load_weights(f"{filename}.h5")
    def train(self,r):
        with tf.GradientTape() as tape:
            base_reward = tf.cast(r,tf.float32)
            weight_contrib = tf.add_n([tf.reduce_sum(tf.abs(w)) for w in self.model.trainable_variables])
            reward = base_reward+0.001*weight_contrib
            loss = -tf.reduce_mean(reward)
        grads = tape.gradient(loss,self.model.trainable_variables)
        self.model.optimizer.apply_gradients(zip(grads,self.model.trainable_variables))