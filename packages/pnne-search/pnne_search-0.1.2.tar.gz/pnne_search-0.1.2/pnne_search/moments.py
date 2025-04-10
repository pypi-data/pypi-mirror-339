import numpy as np
import scipy.sparse
from scipy.optimize import minimize


def moments(Y, Xp, Xa, Xc, consumer_idx, nne):

    n = Xc.shape[0]               # number of consumers
    J = Xp.shape[0] // n          # number of products per consumer
    p = Xp.shape[1]               # dimension p
    a = Xa.shape[1]               # dimension a
    c = Xc.shape[1]               # dimension c

    ip = np.hstack([np.ones(p, dtype=bool), np.zeros(nne['dim']['p'][1] - p, dtype=bool)])
    ia = np.hstack([np.ones(a, dtype=bool), np.zeros(nne['dim']['a'][1] - a, dtype=bool)])
    ic = np.hstack([np.ones(c, dtype=bool), np.zeros(nne['dim']['c'][1] - c, dtype=bool)])

    # Regularization parameters
    lamda = nne['reg_lamda']

    ys = Y[:, 0].astype(bool)  # searched
    yb = Y[:, 1].astype(bool)  # bought

    # Sparse consumer-to-row matrix A: (n x nJ)
    # A[i, r] = 1 if row r belongs to consumer i
    # consumer_idx is assumed 0-based; if 1-based, subtract 1 here.
    # data = np.ones(len(consumer_idx), dtype=float)
    # row_ind = consumer_idx - 1
    # col_ind = np.arange(len(consumer_idx))
    # A = scipy.sparse.csr_matrix((data, (row_ind, col_ind)), shape=(n, len(consumer_idx)))
    A = scipy.sparse.csr_matrix((np.ones(n * J), (consumer_idx-1, np.arange(n * J))), shape=(n, n * J))

    # Consumer-level sums
    ys_t = A @ ys # total # of searches per consumer
    yb_t = A @ yb # of times a consumer bought inside goods

    # Averages at consumer level
    Xp_t = A @ Xp / J
    Xa_t = A @ Xa / J

    # Subset for only rows where a search happened
    Xp_s = Xp[ys, :]
    Xa_s = Xa[ys, :]
    # Weighted consumer attribute matrix for the searched rows
    Xc_s = A[:, ys].T @ Xc

    # Some summary statistics
    # mu1: e.g. [mean(ys_t>1), mean(ys_t), mean(log(ys_t)), mean(yb_t), mean(yb(ys))]
    mu1 = np.array([
        np.mean(ys_t > 1),
        np.mean(ys_t),  
        np.mean(np.log(ys_t)),
        np.mean(yb_t),
        np.mean(yb[ys]) 
    ])

    # mu2: means of Xp_s, Xa_s, Xc_s, plus a nan
    mu2 = np.full(len(ip) + len(ia) + len(ic) + 1, 0.00) 
    # fill in [mean(Xp_s), mean(Xa_s), mean(Xc_s), nan]
    mu2[np.hstack([ip, ia, ic, True])] = np.hstack([np.mean(Xp_s, axis=0), np.mean(Xa_s, axis=0), np.mean(Xc_s, axis=0), np.nan])

    mv1 = [np.std(ys_t), np.std(np.log(ys_t))]
    mv2 = np.full(len(ip) + len(ia) + len(ic) + 1, 0.00)
    mv2[np.hstack([ip, ia, ic, True])] = np.hstack([np.std(Xp_s, axis=0), np.std(Xa_s, axis=0), np.std(Xc_s, axis=0), np.nan])

    mv3 = np.full(len(ip) + len(ia) + 1, 0.00)
    mv3[np.hstack([ip, ia, True])] = np.hstack([np.std(Xp_t, axis=0), np.std(Xa_t, axis=0), np.nan])

    # Remove near-constant columns from Xp_t, Xa_t for stability
    Xp_t = Xp_t[:, np.std(Xp_t, axis=0) >= 1e-4]
    Xa_t = Xa_t[:, np.std(Xa_t, axis=0) >= 1e-4]

    # X_o = [Xp, Xa, A'*Xc, A'*Xp_t, A'*Xa_t]
    X_o = np.hstack([Xp, Xa, A.T @ Xc, A.T @ Xp_t, A.T @ Xa_t]) 
    X_s = np.hstack([Xp_s, Xa_s, Xc_s])
    X_t = np.hstack([Xc, Xp_t, Xa_t])

    lamda = np.array(lamda, ndmin=1)  # ensure array
    mm1 = np.zeros((len(lamda), 1 + len(ip) + len(ic) + len(ia) + 1))
    mm2 = np.zeros_like(mm1)
    mm3 = np.zeros((len(lamda), 1 + len(ic) + 1))
    mm4 = np.zeros_like(mm3)
    mm5 = np.zeros_like(mm3)

    for k, lam in enumerate(lamda): 
        cf1, fl1 = reg_logit(lam, X_o, ys, None)               
        cf2, fl2 = reg_logit(lam, X_s, yb[ys], consumer_idx[ys])
        cf3, fl3 = reg_logit(lam, X_t, ys_t > 1, None)
        cf4, fl4 = reg_linear(lam, X_t, np.log(ys_t))
        cf5, fl5 = reg_logit(lam, X_t, yb_t, None)

        # if not all([fl1, fl2, fl3, fl4, fl5]):
        #     return None, None
        mm1[k, np.hstack([True, ip, ia, ic, True])] = np.hstack([cf1[:p + a + c + 1], np.nan])
        mm2[k, np.hstack([True, ip, ia, ic, True])] = np.hstack([cf2, np.nan])
        mm3[k, np.hstack([True, ic, True])] = np.hstack([cf3[:c + 1], np.nan])
        mm4[k, np.hstack([True, ic, True])] = np.hstack([cf4[:c + 1], np.nan])
        mm5[k, np.hstack([True, ic, True])] = np.hstack([cf5[:c + 1], np.nan])

    # Sensitivity: max absolute difference across the stacked [mm1..mm5].
    sens = np.nanmax(np.abs(np.diff(np.hstack([mm1, mm2, mm3, mm4, mm5]), axis=0)))

    # Finally, we assemble mmt as a single 1D array:
    mmt = np.hstack([
        mm1.T.flatten(), mm2.T.flatten(), mm3.T.flatten(), mm4.T.flatten(), mm5.T.flatten(),
        mu1, mu2, mv1, mv2, mv3,
        ip, ia, ic, J, np.sqrt(n)
    ])

    # Remove NaNs like rmmissing
    mmt = mmt[~np.isnan(mmt)].astype(np.float32).reshape(1,-1)

    return mmt, sens



def reg_linear(penalty, X, y):
    
    n = len(y)
    
    # Add intercept term
    X = np.column_stack((np.ones(n), X))
    
    # Define penalty weights
    w = penalty * np.concatenate(([0], np.ones(X.shape[1] - 1)))
    
    # Compute regularized covariance matrix
    B = (X.T @ X) / n + 2 * np.diag(w)
    
    # Check condition number
    flag = np.linalg.eigvals(B).min() > 1e-9
    
    # Compute coefficients
    coef = np.linalg.solve(B, (X.T @ y) / n)
    
    # Compute sensitivity
    # sens = -2* np.linalg.solve(B, np.concatenate(([0], coef[1:])))

    return coef, flag


def reg_logit(penalty, X, y, consumer_idx=None):

    m = int(1e4)
    
    y = y.astype(bool)
    X = np.column_stack((np.ones(len(y)), X))
    coef = np.zeros(X.shape[1])
    
    rng = np.random.RandomState(1)

    if consumer_idx is None:  # Simple logit
        n = len(y)
        
        if n > m:
            n1 = np.sum(y)
            n0 = n - n1
            m1 = min(n1, max(m - n0, m // 2))
            m0 = m - m1
            
            r = rng.random_sample(len(y))

            true_idx, false_idx = np.where(y)[0], np.where(~y)[0]
            idx1 = true_idx[np.argsort(r[true_idx])[:m1]]
            idx0 = false_idx[np.argsort(r[false_idx])[:m0]]

            i = np.concatenate((idx1, idx0))
            X_y_sum = -np.sum(X[i][y[i]], axis=0)
            res = minimize(fun=lambda c: loss_binary(X[i], y[i], X_y_sum,penalty, c)[0],
                        x0=coef,
                        jac=lambda c: loss_binary(X[i], y[i], X_y_sum,penalty, c)[1],
                        hess=lambda c: loss_binary(X[i], y[i], X_y_sum, penalty, c)[2],
                        method='trust-ncg')
            coef = res.x
            coef[0] -= np.log(n0 / n1 * m1 / m0)

        X_y_sum = -np.sum(X[y], axis=0)
        res = minimize(fun=lambda c: loss_binary(X, y, X_y_sum,penalty, c)[0],
                        x0=coef,
                        jac=lambda c: loss_binary(X, y, X_y_sum,penalty, c)[1],
                        hess=lambda c: loss_binary(X, y, X_y_sum,penalty, c)[2],
                        method='trust-ncg')
        coef = res.x
        # res.hess = loss_binary(X, y, X_y_sum, penalty, coef)[2]
        flag = res.success and np.min(np.linalg.eigvals(res.hess)) > 1e-9
    
    else:  # Multinomial logit
        n = np.max(consumer_idx)
        if n > m:
            t = np.bincount(consumer_idx, weights=y)[1:]
            m1 = max(1, int(np.mean(t) * m))
            m0 = m - m1

            # k1 = np.random.choice(np.where(t > 0)[0], m1, replace=False)
            # k0 = np.random.choice(np.where(t == 0)[0], m0, replace=False)
            r = rng.random_sample(len(t))
            pos_candidates = np.where(t > 0)[0]
            sortOrderPos = np.argsort(r[pos_candidates])
            k1 = pos_candidates[sortOrderPos[:m1]]
            neg_candidates = np.where(t == 0)[0]
            sortOrderNeg = np.argsort(r[neg_candidates])
            k0 = neg_candidates[sortOrderNeg[:m0]]

            i = np.isin(consumer_idx, np.concatenate((k1, k0)))         

            X_y_sum = -np.sum(X[i][y[i]], axis=0)
            res = minimize(fun=lambda c: loss_multi(X[i], y[i], consumer_idx[i], X_y_sum, penalty, c)[0], 
                x0=coef, 
                jac=lambda c: loss_multi(X[i], y[i], consumer_idx[i], X_y_sum, penalty, c)[1], 
                hess=lambda c: loss_multi(X[i], y[i], consumer_idx[i], X_y_sum, penalty, c)[2],
                method='trust-ncg')

            coef = res.x

        X_y_sum = -np.sum(X[y], axis=0)        
        res = minimize(fun=lambda c: loss_multi(X, y, consumer_idx, X_y_sum, penalty, c)[0], 
                        x0=coef, 
                        jac=lambda c: loss_multi(X, y, consumer_idx, X_y_sum, penalty, c)[1], 
                        hess=lambda c: loss_multi(X, y, consumer_idx, X_y_sum, penalty, c)[2],
                        method='trust-ncg')
        coef = res.x
        # res.hess = loss_multi(X, y, consumer_idx, penalty, coef)[2]
        flag = res.success and np.min(np.linalg.eigvals(res.hess)) > 1e-9
    
    # sens = -2 * np.concatenate(([0], coef[1:])) / res.hess
    return coef, flag



def loss_binary(X, y, X_y_sum, penalty, coef):
    n = len(y)
    w = penalty * np.concatenate(([0], np.ones(X.shape[1] - 1)))
    
    v = X @ coef
    e = np.exp(-v)
    s = e + 1
    val = (1/n) * (-np.sum(v[y]) + np.sum(v) + np.sum(np.log(s))) + np.sum(w * coef**2)
    
    Q = X / s[:, None]
    grad = (1/n) * (X_y_sum + np.sum(Q, axis=0)) + 2 * w * coef
    hess = (1/n) * ((X - Q).T @ Q) + 2 * np.diag(w)
    hess = (hess + hess.T) / 2
    
    return val, grad, hess

def loss_multi(X, y, idx, X_y_sum, penalty, coef):

    unique_labels, idx = np.unique(idx, return_inverse=True)
    idx = idx + 1

    n = np.max(idx)
    w = penalty * np.concatenate(([0], np.ones(X.shape[1] - 1)))
    
    v = X @ coef
    e = np.exp(v)
    s = np.bincount(idx, weights=e) + 1
    val = (1/n) * (-np.sum(v[y]) + np.sum(np.log(s))) + np.sum(w * coef**2)
    
    Q = X * (e / s[idx])[:, None]
    grad = (1/n) * (X_y_sum + np.sum(Q, axis=0)) + 2 * w * coef
    
    Hmat = scipy.sparse.csr_matrix((np.ones(len(idx)), (idx-1, np.arange(len(idx)))),
                                shape=(idx.max(), len(idx)))
    H = Hmat.dot(Q)
    hess = (1/n) * (X.T @ Q - H.T @ H) + 2*np.diag(w)

    hess = (hess + hess.T) / 2
    
    return val, grad, hess

