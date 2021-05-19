from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from time import time
from helpers import printm, Statistics
from bin_model import MyModel
import numpy as np


def forest_bench(train: dict, test: dict):
  scaler = StandardScaler().fit(train['data'])
  train_data = scaler.transform(train['data'])
  test_data = scaler.transform(test['data'])
    
  clf = RandomForestClassifier()
  training_begin = time()
  clf.fit(train_data, train['label'])
  training_time = time() - training_begin

  expected = test['label']

  testing_begin = time()
  real = clf.predict(test_data)
  testing_time = time() - testing_begin

  stat = Statistics(training_time, testing_time, expected, real)
  stat.process()
  return stat


def forest_pca_bench(PCAImplementation, label, components, train, test):
  scaler = StandardScaler().fit(train['data'])
  train_data = scaler.transform(train['data'])
  test_data = scaler.transform(test['data'])

  pca_begin = time()
  pca = PCAImplementation(components)
  pca.fit(train['data'])

  train_transformed = { 
        'data':  pca.transform(train_data),
        'label': train['label']
  }
  test_transformed = {
        'data':  pca.transform(test_data),
        'label': test['label']
  }
  pca_time = time() - pca_begin
  clf = RandomForestClassifier()
  training_begin = time()
  clf.fit(train_transformed['data'], train_transformed['label'])
  training_time = time() - training_begin

  expected = test['label']

  testing_begin = time()
  real = clf.predict(test_transformed['data'])
  testing_time = time() - testing_begin
  stat = Statistics(training_time, testing_time, expected, real)
  stat.process()
  return {"abs_err": stat.abs_err, 
          "mse_err": stat.mse_err, 
          "rmse_err": stat.rmse_err, 
          "accuracy": stat.accuracy,
          "pca_time": pca_time,
          "training_time": training_time,
          "testing_time": testing_time,
          "x": components,
          "label": label}

def not_LA_bench(test: dict):
  model = MyModel(6)

  testing_begin = time()
  predicted = model.predict(test['data'])
  testing_time = time() - testing_begin

  stat = Statistics(0, testing_time, test['label'], predicted)
  stat.process()
  return stat