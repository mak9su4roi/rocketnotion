import numpy as np
from random import randint

class CustomPCA:

# Limit of iteration to be made when aproximating eigenpair
  ITER_LIM = 50
# The expected accuracy of aprpoximation of eignvalue
  EPSILON = 1e-15

  def __init__(self, features_num):
# Number of eigenpairs to exptract
    self.features = features_num

# Normalization of vector (to unit length)
  @staticmethod
  def __unitify(vec):
    return vec/np.linalg.norm(vec)

# Return random vector of size n with unit length
  @staticmethod
  def __get_unit_vector(n):
    return CustomPCA.__unitify(np.array([randint(0, n) for _ in range(n)]))

# Find largest eigenpair
  def __largest_eigen(self, cov_m):
    size = len(cov_m)
    vector_prev = vector_cur = self.__get_unit_vector(size)
    value_prev = value_cur = None

    for _ in range(CustomPCA.ITER_LIM):
      vector_prev = vector_cur
      vector_cur = self.__unitify(np.dot(cov_m, vector_prev))
      value_cur = np.inner(vector_cur, np.dot(cov_m, vector_cur))
      if value_prev is None:
        value_prev = value_cur
        continue
      if 1 - CustomPCA.EPSILON < abs(value_cur/value_prev) < 1 + CustomPCA.EPSILON:
        break
      value_prev = value_cur
    return value_prev, vector_cur

  def __top_eigen(self, cov_m):
    A = np.array(cov_m, copy=True, dtype=float)
    eigen_pairs = [(self.__largest_eigen(np.array(cov_m, copy=True)))]
    for _ in range(self.features-1):
      large = eigen_pairs[-1]

# Hotelling deflation method for nullify certain eigenvalue
      A -= large[0]*np.outer(large[1], large[1])
      eigen_pairs += [(self.__largest_eigen(np.array(A, copy=True)))]
    return eigen_pairs

# Create transformation matrix
  def fit(self, A):
    mean = np.mean(A, axis=0)
    cov_m = (A - mean).T.dot((A - mean)) / (A.shape[0]-1)
    self.all_features = len(cov_m)
    pairs = self.__top_eigen(cov_m)
    self.values = [el[0] for el in pairs]
    self.vectors = [el[1] for el in pairs]
    self.projection = np.hstack([el.reshape(self.all_features, 1) for el in self.vectors])

# Transform data sin
  def transform(self, data):
    return np.array(data).dot(self.projection)
