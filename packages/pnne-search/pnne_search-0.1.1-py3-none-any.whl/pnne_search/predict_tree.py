import numpy as np
import pickle

def predict_tree(tree, x):
    node = 0  

    while True:
        if not tree['IsBranchNode'][node][0]:
            break

        predictor = tree['CutPredictor'][node][0]
        feature_idx = int(predictor[0][1:]) - 1  # "x1" → 0, "x2" → 1, etc.
        threshold = tree['CutPoint'][node][0]
        children = tree['Children'][node].flatten() - 1  # Convert MATLAB 1-based to 0-based

        if x[feature_idx] < threshold:
            node = children[0]
        else:
            node = children[1]
            
    return tree['NodeMean'][node][0]


def predict_ensemble(all_ensemble, all_weights, x):
    val = []
    
    for k in range(len(all_ensemble)):
        pred = 0.0
        ensemble = all_ensemble[k]
        weights = all_weights[k]

        num_trees = ensemble.shape[1]

        for i in range(num_trees):
            tree = ensemble[0][i]
            weight = weights[i][0]
            pred += weight * predict_tree(tree, x)

        val.append(pred)

    return np.array(val)

def predict_ensemble_multi(all_ensemble, all_weights, X):

    num_samples = X.shape[0]
    val = []
    for i in range(num_samples):
        x = X[i, :]
        val.append(predict_ensemble(all_ensemble, all_weights, x))

    return np.array(val)