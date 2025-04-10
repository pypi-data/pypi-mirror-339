import numpy as np

def accuracy(output, tags):
    pred_class = np.argmax(output, axis=1)
    true_class = np.argmax(tags, axis=1)
    return np.mean(pred_class == true_class) * 100
