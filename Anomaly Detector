from numpy import array
import tensorflow
from tensorflow import keras
from tensorflow.keras.layers import Conv1D, Dense, Flatten, MaxPooling1D
from tensorflow.keras.models import Model, load_model
import pandas as pd
import numpy
import time
import os, os.path
from pathlib import Path

features = 1
# choose a number of time steps
steps = 3

df = pd.read_csv('sample.csv')

humedad1_historia     = df['Humedad 1'].tolist()
humedad2_historia     = df['Humedad 2'].tolist()
temperatura1_historia = df['Temperatura 1'].tolist()
temperatura2_historia = df['Temperatura 2'].tolist()
presion1_historia     = df['Presion 1'].tolist()
presion2_historia     = df['Presion 2'].tolist()

print(type(humedad1_historia))
print(humedad1_historia)


model = tensorflow.keras.Sequential()
model.add(Conv1D(filters=64, kernel_size=2, activation='relu', input_shape=(steps,
features)))
model.add(MaxPooling1D(pool_size=2))
model.add(Flatten())
model.add(Dense(100, activation='relu'))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')
model.summary()

print('Saving Model')
model.save('anomalyModel.h5')
print('Model Saved!')
 

'''
# load model 
savedModel=load_model('anomalyModel.h5')
savedModel.summary()
'''

# split a univariate sequence into samples
def split_sequence(sequence, steps):
  X, y = list(), list()
  for start in range(len(sequence)):
    # define the end index of the sequence
    end_index = start + steps
    # to check if end_index stays in the allowable limit
    if end_index > len(sequence)-1:
      break
    # extract input and output parts of the sequence
    sequence_x, sequence_y = sequence[start : end_index], sequence[end_index]
    X.append(sequence_x)
    y.append(sequence_y)
  return array(X), array(y)





def train_and_save(name_of_weight,raw_sequence):
    # split into samples
    X, y = split_sequence(raw_sequence, steps)
    X = X.reshape((X.shape[0], X.shape[1], features))
    #model.fit(X, y, epochs=10000, verbose=0)
    model.fit(X, y, epochs=2000) #Increase for accuracy
    Path("./saved_weights").mkdir(parents=True, exist_ok=True)
    model.save_weights('./saved_weights/'+name_of_weight)

train_and_save("humedad1_weights",humedad1_historia)
train_and_save("humedad2_weights",humedad2_historia)
train_and_save("temperatura1_weights",temperatura1_historia)
train_and_save("temperatura2_weights",temperatura2_historia)
train_and_save("presion1_weights",presion1_historia)
train_and_save("presion2_weights",presion2_historia)
