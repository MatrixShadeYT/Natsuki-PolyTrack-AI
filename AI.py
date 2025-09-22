import numpy as np

class module:
  def __init__(self,layers):
    self.layers = layers
  def run(self,inputs):
    x = inputs
    for layer in self.layers:
      x = layer.forward(x)
    return x

class layer_dense:
  def __init__(self,inputs=3,type=None,biases=3,weights=3):
    self.inputs, self.type = inputs, type
    if isinstance(biases,int):
      self.biases = np.random.randn(biases)
    else:
      self.biases = biases
    if isinstance(weights,int):
      self.weights = np.random.randn(biases,weights)
    else:
      self.weights = weights
  def forward(self,inputs):
    x = np.dot(inputs,self.weights)+self.biases
    if self.type == "RELU":
      value = x if x>= 0 else 0
    elif self.type == "softmax":
      value = np.exp(x)/np.sum(np.exp(x))
    elif self.type == "sigmoid":
      value = 1/1+np.exp(-x)
    else:
      value = x
    self.output = value
    return value
