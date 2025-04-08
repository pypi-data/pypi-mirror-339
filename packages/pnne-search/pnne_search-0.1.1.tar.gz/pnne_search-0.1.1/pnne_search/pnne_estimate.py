import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'   
os.environ['XLA_FLAGS'] = '--xla_gpu_autotune_level=0'

import absl.logging
absl.logging.set_verbosity(absl.logging.ERROR)

import numpy as np
import pandas as pd
import scipy.sparse
from scipy.stats import zscore, skew, mode
import warnings
from joblib import Parallel, delayed
import tensorflow as tf
from tensorflow.keras.models import load_model
import json
import pickle

from . import masked_mse
from .utils import *
from .moments import moments
from .data_checks import data_checks
from .predict_tree import *

base_dir = os.path.dirname(__file__)

model_net = load_model(os.path.join(base_dir, 'nne_matlab.keras'))

with open(os.path.join(base_dir, "nne_info.json"), "r") as f:
    nne = json.load(f)

with open(os.path.join(base_dir,'tree_matlab.pkl'), 'rb') as f:
    model_tree = pickle.load(f)

curve = pd.read_csv(os.path.join(base_dir,"curve.csv"))


def pnne_estimate(Y, Xp, Xa, Xc, consumer_idx, checks=True, se=False, use_parallel=True):

    p = Xp.shape[1]
    a = Xa.shape[1]
    c = Xc.shape[1]

    i_par = []
    for name in nne['name']:
        if name == "\\alpha_0":
            i_par.append(True)
        elif name.startswith("\\alpha_") and int(name.split("_")[1]) <= a:
            i_par.append(True)
        elif name == "\\eta_0":
            i_par.append(True)
        elif name.startswith("\\eta_") and int(name.split("_")[1]) <= c:
            i_par.append(True)
        elif name.startswith("\\beta_") and int(name.split("_")[1]) <= p:
            i_par.append(True)
        else:
            i_par.append(False)
    i_par = np.array(i_par)
    
    Zp = zscore(Xp, axis=0)
    Za = zscore(Xa, axis=0)
    Zc = zscore(Xc, axis=0)
    
    mu_p = np.mean(Xp, axis=0); sigma_p = np.std(Xp, axis=0)
    mu_a = np.mean(Xa, axis=0); sigma_a = np.std(Xa, axis=0)
    mu_c = np.mean(Xc, axis=0); sigma_c = np.std(Xc, axis=0)

    n = consumer_idx[-1].item()
    J = len(consumer_idx) // n

    if Xa.size == 0:
        Xa = np.zeros((n * J, 0))
    if Xc.size == 0:
        Xc = np.zeros((n, 0))
    if Y.shape[1] > 2:
        Y = Y[:, :2]

    if checks:
        _, buy_rate, srh_rate, num_srh, buy_n, srh_n = data_checks(Y, Zp, Za, Zc, consumer_idx)
        if buy_rate == 0:
            raise ValueError("There are no purchases.")
        if Xp.shape[1] < nne['dim']['p'][0]:
            raise ValueError(f"Number of attributes in Xp must be at least {nne['dim']['p'][0]}")
        if Xp.shape[1] > nne['dim']['p'][1]:
            raise ValueError(f"Number of attributes in Xp must be at most {nne['dim']['p'][1]}")
        if Xa.shape[1] > nne['dim']['a'][1]:
            raise ValueError(f"Number of attributes in Xa must be at most {nne['dim']['a'][1]}")
        if Xc.shape[1] > nne['dim']['c'][1]:
            raise ValueError(f"Number of attributes in Xc must be at most {nne['dim']['c'][1]}")

        if n < nne['dim']['n'][0]:
            warnings.warn(f"Sample size n must be at least: {nne['dim']['n'][0]}")
        if J < nne['dim']['J'][0]:
            warnings.warn(f"Number of options J must be at least: {nne['dim']['J'][0]}")
        if J > nne['dim']['J'][1]:
            warnings.warn(f"Number of options J must be at most: {nne['dim']['J'][1]}")

        if buy_n < nne['stat']['buy_n'][0]:
            warnings.warn("Very few consumers made purchases.")
        if srh_n < nne['stat']['srh_n'][0]:
            warnings.warn("Very few consumers made non-free searches.")

        if buy_rate < nne['stat']['buy_rate'][0]:
            warnings.warn("Buy rate is too small.")
        if buy_rate > nne['stat']['buy_rate'][1]:
            warnings.warn("Buy rate is too large.")

        if srh_rate < nne['stat']['srh_rate'][0]:
            warnings.warn("Search rate (non-free) is too small.")
        if srh_rate > nne['stat']['srh_rate'][1]:
            warnings.warn("Search rate (non-free) is too large.")

        if num_srh < nne['stat']['num_srh'][0]:
            warnings.warn("Average number of searches is too small.")
        if num_srh > nne['stat']['num_srh'][1]:
            warnings.warn("Average number of searches is too large.")

        Z = np.hstack([Zp, Za, Zc[consumer_idx-1]])

        q = np.percentile(Z, [2.5, 50, 97.5], axis=0)

        if np.any(np.max(Z, axis=0) > 2 * q[2] - q[1]) or np.any(np.min(Z, axis=0) < 2 * q[0] - q[1]):
            warnings.warn("X has extreme values; winsorizing may help.")
        if np.any(np.logical_and(np.abs(skew(Z, axis=0)) > 2, np.abs(mode(np.round(Z, 1), axis=0)[0]) > 0.5)):
            warnings.warn("X has highly skewed attributes.")

        A = scipy.sparse.csr_matrix((np.ones(n * J), (consumer_idx-1, np.arange(n * J))), shape=(n, n * J))
        Zp_t = A.dot(Zp) / J
        Za_t = A.dot(Za) / J

        if np.any(np.std(Zp - Zp_t[consumer_idx-1], axis=0) < 0.01):
            warnings.warn("Xp lacks variation within consumers.")
        if np.any(np.std(Za - Za_t[consumer_idx-1], axis=0) < 0.01):
            warnings.warn("Xa lacks variation within consumers.")
        if np.any(np.std(Za - Zp.dot(np.linalg.pinv(Zp.T.dot(Zp)).dot(Zp.T).dot(Za)), axis=0) < 0.01):
            warnings.warn("Xa lacks variation independent of Xp.")

    par = {}

    # check data size
    if n <= nne['dim']['n'][1]:

        mmt, sens = moments(Y, Zp, Za, Zc, consumer_idx, nne)
        pred_net = model_net.predict(mmt.reshape(1,-1), verbose=0).flatten()[i_par]
        pred_tree = predict_ensemble_multi(model_tree['ensemble'], model_tree['weights'], mmt).flatten()[i_par]

    else: # large data
        n = len(Xc)
        blocks = int(np.ceil(n / nne['dim']['n'][1]))

        rng = np.random.RandomState(1)
        permuted = np.argsort(rng.random_sample(n)) + 1
        block_idx = np.ceil(permuted / n * blocks).astype(int)

        if use_parallel:
            results = Parallel(n_jobs=-1)(
                delayed(split_moments)(b, block_idx, Y, Zp, Za, Zc, consumer_idx)
                for b in range(1, blocks + 1)
                )
            all_mmt, all_sens = zip(*results)
            all_mmt = np.squeeze(np.array(all_mmt), axis=1)
        else:
            all_mmt = []; all_sens = []
            for b in range(1, blocks + 1):
                mmt, sens = split_moments(b, block_idx, Y, Zp, Za, Zc, consumer_idx)
                all_mmt.append(mmt)
                all_sens.append(sens)
            all_mmt = np.array(all_mmt)
        sens = np.mean(np.array(all_sens), axis=0)
        pred_net_all = model_net.predict(all_mmt, verbose=0)
        pred_net = np.mean(pred_net_all, axis=0).flatten()[i_par]
        pred_tree_all = predict_ensemble_multi(model_tree['ensemble'], model_tree['weights'], all_mmt)
        pred_tree = np.mean(pred_tree_all, axis=0).flatten()[i_par]

    diff = np.mean(np.array(nne['diff']['w'])[i_par] * np.abs(pred_net - pred_tree))
    tree_weight = np.clip((diff - nne['diff']['q1']) / (nne['diff']['q2'] - nne['diff']['q1']), 0, 1)

    par['pred'] = pred_net + (pred_tree - pred_net) * tree_weight
    par['mmt_sens'] = sens

    # Post-estimation checks
    if checks:
        if par['mmt_sens'] > 1:
            warnings.warn("Reduced-form patterns are unstable; estimates are likely inaccurate.")
        elif par['mmt_sens'] > 0.5:
            warnings.warn("Reduced-form patterns are not very stable; estimates may be inaccurate.")
        
        if 'diff' in nne:
            if diff > nne['diff']['q2']:
                warnings.warn("The data is probably ill-suited for this search model.")
            elif diff > nne['diff']['q1']:
                warnings.warn("The data might be ill-suited for this search model.")

    # warnings.filterwarnings('default', category=UserWarning)

    # Bootstrap SE
    if se:
        se_repeats = 50

        if n <= nne['dim']['n'][1]:
            locators = [np.arange((i-1)*J, i*J) for i in range(1, n+1)] 

            if use_parallel:
                results = Parallel(n_jobs=-1)(
                    delayed(bootstrap_moments)(r, n, locators, Y, Zp, Za, Zc, consumer_idx, nne)
                    for r in range(se_repeats)
                    )
                all_mmt = np.squeeze(np.array(results), axis=1)
            else:
                all_mmt = []
                for r in range(se_repeats):
                    mmt = bootstrap_moments(r, n, locators, Y, Zp, Za, Zc, consumer_idx, nne)
                    all_mmt.append(mmt)
                all_mmt = np.squeeze(np.array(all_mmt), axis=1)

            pred_net = model_net.predict(all_mmt, verbose=0)
            if tree_weight > 0:
                pred_tree = predict_ensemble_multi(model_tree['ensemble'], model_tree['weights'], all_mmt)
                pred = pred_net + (pred_tree - pred_net) * tree_weight
            else:
                pred = pred_net

            par['se'] = np.std(pred, axis=0)[i_par]
        else: # large data
            locators = [np.arange((i-1)*J, i*J) for i in range(1, n+1)] 
            all_mmt = []
            if use_parallel:
                all_mmt = Parallel(n_jobs=-1)(
                    delayed(bootstrap_split_moments)(r, n, locators, block_idx, Y, Zp, Za, Zc, consumer_idx, nne)
                    for r in range(se_repeats)
                    )
                all_mmt = np.squeeze(np.array(all_mmt), axis=2)
            else:
                for r in range(se_repeats):
                    mmt = bootstrap_split_moments(r, n, locators, block_idx, Y, Zp, Za, Zc, consumer_idx, nne)
                    all_mmt.append(mmt)
                all_mmt = np.array(all_mmt)

            pred_net = []
            for b in range(1, blocks + 1):
                pred_net_b = model_net.predict(all_mmt[:,b-1,:], verbose=0)
                pred_net.append(pred_net_b)
            pred_net = np.mean(np.array(pred_net), axis=0)
            if tree_weight > 0:
                pred_tree = []
                for b in range(1, blocks + 1):
                    pred_tree_b = predict_ensemble_multi(model_tree['ensemble'], model_tree['weights'], all_mmt[:,b-1,:])
                    pred_tree.append(pred_tree_b)
                pred_tree = np.mean(np.array(pred_tree), axis=0)
                pred = pred_net + (pred_tree - pred_net) * tree_weight
            else:
                pred = pred_net

            par['se'] = np.std(pred, axis=0)[i_par]

    alpha0 = par['pred'][0]
    alpha = par['pred'][1:a+1]
    eta0 = par['pred'][a+1]
    eta = par['pred'][a+2:a+2+c]
    beta = par['pred'][a+2+c:a+2+c+p]

    par['val'] = np.concatenate([
        [alpha0 - np.sum(alpha / sigma_a * mu_a)],
        alpha / sigma_a,
        [eta0 - np.sum(eta / sigma_c * mu_c) + np.sum(beta / sigma_p * mu_p)],
        eta / sigma_c,
        beta / sigma_p
    ])
    del par['pred']
    del par['mmt_sens']

    par['name'] = np.array(nne['name'])[i_par]

    out = {'Name': par['name'], 'Estimate': par['val']}
    if 'se' in par:
        out['SE'] = par['se']

    out = pd.DataFrame(out)

    return out


def bootstrap_moments(r, n, locators, Y, Zp, Za, Zc, consumer_idx, nne):
    rng = np.random.RandomState(r + 1)
    k = np.floor(rng.random_sample(n) * n).astype(int)
    i = np.concatenate([locators[idx] for idx in k])
    mmt, sens = moments(Y[i], Zp[i], Za[i], Zc[k], consumer_idx, nne)
    return mmt

## Large data splitter 

def split_moments(b, block_idx, Y, Zp, Za, Zc, consumer_idx):

    k = np.where(block_idx == b)[0]
    i = np.isin(consumer_idx, k + 1)
    repeated_idx = np.repeat(np.arange(len(k)), J) + 1
    mmt, sens = moments(Y[i], Zp[i], Za[i], Zc[k], repeated_idx, nne)

    return mmt, sens


def bootstrap_split_moments(r, n, locators, block_idx, Y, Zp, Za, Zc, consumer_idx, nne):
    rng = np.random.RandomState(r + 1)
    k = np.floor(rng.random_sample(n) * n).astype(int)
    i = np.concatenate([locators[idx] for idx in k])
    all_mmt = []
    for b in range(1, blocks + 1):
        mmt,_ = split_moments(b, block_idx, Y[i], Zp[i], Za[i], Zc[k], consumer_idx)
        all_mmt.append(mmt)
    return np.array(all_mmt)