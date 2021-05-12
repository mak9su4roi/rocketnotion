import matplotlib.pyplot as plt
from math import sqrt, ceil
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
