import numpy as np
import pandas as pd
import scipy.sparse
from scipy.optimize import minimize
from scipy.interpolate import interp1d




def interpolate(query, x, v):
    interp_func = interp1d(x, v, kind='linear', bounds_error=False, fill_value='extrapolate')
    return interp_func(query)

def search_model(par, curve, Xp, Xa, Xc, consumer_idx, seed=0):
    rng = np.random.RandomState(seed)

    p = Xp.shape[1]
    a = Xa.shape[1]
    c = Xc.shape[1]
    
    par = np.array(par).flatten()
    consumer_idx = np.array(consumer_idx).flatten()
    
    if len(par) != p + a + c + 2:
        raise ValueError("Incorrect number of parameters.")
    
    n = Xc.shape[0]  # number of consumers
    J = Xp.shape[0] // n  # number of search options
    
    alpha0 = par[0]
    alpha = par[1:a+1]
    eta0 = par[a+1]
    eta = par[a+2:a+c+2]
    beta = par[a+c+2:a+c+p+2]
    delta = 0
    
    u1 = rng.random_sample(n)  
    u2 = rng.random_sample(n)
    err_o = np.sqrt(-2 * np.log(u1)) * np.cos(2 * np.pi * u2) 

    u1 = rng.random_sample(n*J)  
    u2 = rng.random_sample(n*J)
    err_v = np.sqrt(-2 * np.log(u1)) * np.cos(2 * np.pi * u2) 

    u1 = rng.random_sample(n*J)  
    u2 = rng.random_sample(n*J)
    err_u = np.sqrt(-2 * np.log(u1)) * np.cos(2 * np.pi * u2) 
    # o = eta0 + Xc @ eta + np.random.randn(n)
    # v = Xp @ beta - o[consumer_idx-1] + np.random.randn(n * J) * np.exp(delta)
    # u = v + np.random.randn(n * J)
    o = eta0 + Xc @ eta + err_o
    v = Xp @ beta - o[consumer_idx-1] + err_v * np.exp(delta)
    u = v + err_u
    
    r = v + interpolate(alpha0 + Xa @ alpha, curve['log_cost'], curve['utility'])
    
    sort_idx = np.lexsort((-r, consumer_idx))
    u = u[sort_idx]
    r = r[sort_idx]
    
    Y_sorted = np.full((n * J, 2), np.nan)
    
    for i in range(n):
        k = slice(i * J, (i + 1) * J)
        r_i = r[k]
        u_i = u[k]
        
        searched = np.maximum.accumulate(np.insert(u_i[:-1], 0, 0)) <= r_i
        searched[0] = True
        
        u_i[~searched] = -np.inf
        
        j = np.argmax(u_i)
        bought = np.zeros(J, dtype=bool)
        bought[j] = np.max(u_i) > 0
        
        Y_sorted[k, 0] = searched
        Y_sorted[k, 1] = bought
    
    Y = np.empty_like(Y_sorted)
    Y[sort_idx] = Y_sorted
    
    return Y

