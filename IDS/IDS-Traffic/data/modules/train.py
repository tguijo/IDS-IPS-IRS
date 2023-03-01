import tensorflow as tf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from .constants import *
from os.path import exists
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from tensorflow import lite

# This function scans the dataset and predicts the result using tenserflow lite model
def perform_scan(test: pd.DataFrame):
    global logistic_model
    print(LOG_HEAD + "Performing anamoly scan on the input data.")
    sc_x = StandardScaler()
    sc_x.fit_transform(test)
    X_test = sc_x.transform(test)
    qda = QuadraticDiscriminantAnalysis()
    X_test = np.array(X_test, dtype=np.float32)
    X_test = np.expand_dims(X_test, axis=1)
    Y_test = []
    for x in range(
        len(X_test)
    ):  # Tensor flow lite interpreter is used for predicting the output
        _interpreter.set_tensor(_model_inputs[0]["index"], X_test[x])
        _interpreter.invoke()
        output_data = _interpreter.get_tensor(_model_outputs[0]["index"])
        Y_test.append((test.iloc[x], output_data[0]))
        Y_test = qda.fit(X_test, y_test)
    print(LOG_HEAD + ">>> Anamoly scan completed.")
    return Y_test
