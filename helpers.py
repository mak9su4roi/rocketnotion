import matplotlib.pyplot as plt
from math import sqrt, ceil
from sklearn import metrics
import numpy as np

def printm(data):
    dt = np.array(data)
    shape = dt.shape
    assert 1 <= len(shape) <= 2, "wrong shape"
    if len(shape) == 1:
        dt = [dt]
    edge = ceil(sqrt(shape[0]))
    for ind, img in enumerate(dt):
        plt.subplot(edge, edge, ind+1)
        plt.axis('off')
        plt.imshow(np.array(img).reshape(28, 28), cmap='gray_r')
        
class Statistics:
  def __init__(self, tr, ts, exp, real):
    self.training_time = tr
    self.testing_time = ts
    self.expected = exp
    self.real = real
  
  def process(self):
    self.abs_err = metrics.mean_absolute_error(self.expected, self.real)
    self.mse_err = metrics.mean_squared_error(self.expected, self.real)
    self.rmse_err = np.sqrt(metrics.mean_squared_error(self.expected, self.real))
    self.accuracy = metrics.accuracy_score(self.expected, self.real)\

  def __str__(self):
    return f"Training time:            |  {self.training_time}\n" +\
           f"Testing time:             |  {self.testing_time}\n" +\
            "="*50 + "\n" +\
           f"Mean Absolute Error:      |  {self.abs_err}\n" +\
           f"Mean Squared Error:       |  {self.mse_err}\n" +\
           f"Root Mean Squared Error:  |  {self.rmse_err}\n" +\
            "="*50 + "\n" +\
           f"Accuracy:                 |  {self.accuracy}"