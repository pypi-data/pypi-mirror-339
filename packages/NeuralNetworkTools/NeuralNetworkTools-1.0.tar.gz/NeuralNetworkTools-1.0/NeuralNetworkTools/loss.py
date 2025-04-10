import numpy as np

def cross_entropy(y_true, y_pred):
    epsilon = 1e-8
    y_pred = np.clip(y_pred, epsilon, 1. - epsilon)
    losses = -np.sum(y_true * np.log(y_pred), axis=1)
    return np.mean(losses)