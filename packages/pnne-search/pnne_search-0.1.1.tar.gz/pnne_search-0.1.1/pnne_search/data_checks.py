import numpy as np
from scipy.sparse import csr_matrix

def data_checks(Y, Xp, Xa, Xc, consumer_idx):
    
    # Y = np.asarray(Y)
    # Xp = np.asarray(Xp)
    # Xa = np.asarray(Xa) if Xa is not None else np.zeros((0,0))
    # Xc = np.asarray(Xc) if Xc is not None else np.zeros((0,0))
    # consumer_idx = np.asarray(consumer_idx)

    n = consumer_idx[-1].item()
    # J = number of options (per consumer)
    J = int(consumer_idx.size / n)

    # Check that each consumer appears exactly J times
    unique_counts = np.bincount(consumer_idx)  # consumer_idx is 1-based
    # Ignore count of zero for index=0, since bincount returns length= max(consumer_idx)+1
    unique_counts = unique_counts[1:]
    if np.ptp(unique_counts) != 0:  # ptp = max - min
        raise ValueError("Each consumer must appear the same number of times (J).")

    # Check that consumer_idx is exactly [1,1,...,2,2,...,n,n,...] (repelem(1..n, J))
    check_idx = np.repeat(np.arange(1, n+1), J)
    if not np.array_equal(consumer_idx, check_idx):
        raise ValueError("consumer_idx must be sorted and repeat each ID exactly J times.")

    # If Xa or Xc are empty in MATLAB, they become (n*J,0) or (n,0). Ensure shapes match here:
    if Xa.size == 0:  # Suppose user passed an empty array
        Xa = np.zeros((n * J, 0))
    if Xc.size == 0:
        Xc = np.zeros((n, 0))

    # Check shape of Y
    if Y.shape[1] != 2:
        raise ValueError("Y must have 2 columns: [search_indicator, buy_indicator].")
    if Y.shape[0] != n * J:
        raise ValueError("Y must have n*J rows.")
    # Ensure Y is binary
    if not np.array_equal(Y, Y.astype(bool)):
        raise ValueError("Y must be binary (0 or 1).")

    # Check shape of Xp, Xa, Xc
    if Xp.shape[0] != n * J:
        raise ValueError("Xp must have n*J rows.")
    if Xa.shape[0] != n * J:
        raise ValueError("Xa must have n*J rows.")
    if Xc.shape[0] != n:
        raise ValueError("Xc must have n rows.")

    # Check that all arrays have finite entries
    def allfinite(arr):
        return np.isfinite(arr).all()

    if not (allfinite(Xp) and allfinite(Xa) and allfinite(Xc)):
        raise ValueError("Xp/Xa/Xc contain non-finite or missing values.")
        
    # Check that each feature has some variation.
    def has_zero_range(arr):
        if arr.size == 0:
            return False
        col_ranges = arr.max(axis=0) - arr.min(axis=0)
        return np.any(col_ranges == 0)

    if has_zero_range(Xp) or has_zero_range(Xa) or has_zero_range(Xc):
        raise ValueError("Xp, Xa, or Xc has a column with no variation (range=0).")
    
    # Check if X is de-meaned and standardized
    if np.any(np.abs(np.mean(Xp, axis=0)) > 1e-5) or np.any(np.abs(np.mean(Xa, axis=0)) > 1e-5) or np.any(np.abs(np.mean(Xc, axis=0)) > 1e-5):
        raise ValueError("X is not de-meaned.")
    if np.any(np.abs(np.std(Xp, axis=0) - 1) > 1e-5) or np.any(np.abs(np.std(Xa, axis=0) - 1) > 1e-5) or np.any(np.abs(np.std(Xc, axis=0) - 1) > 1e-5):
        raise ValueError("X is not standardized.")
    
    # Y columns
    ys = Y[:,0]  # search indicator
    yb = Y[:,1]  # buy indicator

    # consumer_idx is 1-based, so shift by -1 for np.bincount
    ys_t = np.bincount(consumer_idx - 1, weights=ys)
    yb_t = np.bincount(consumer_idx - 1, weights=yb)

    # Check that each consumer doesn't buy more than one option
    if np.any(yb_t > 1):
        raise ValueError("A consumer bought more than one option.")

    # Check that each consumer made at least one search
    if np.any(ys_t < 1):
        raise ValueError("A consumer did not make the free search.")

    # Check that if an option was bought, it was also searched
    if np.any((yb == 1) & (ys == 0)):
        raise ValueError("A consumer bought an option that was never searched.")

    # Compute buy_rate, srh_rate, etc.
    buy_rate = np.mean(yb_t)        # fraction of consumers who buy
    srh_rate = np.mean(ys_t > 1)    # fraction of consumers searching more than once
    num_srh  = np.mean(ys_t)        # mean number of searches
    buy_n    = buy_rate * n         # expected # of buyers among n consumers
    srh_n    = srh_rate * n         # expected # of multi-search consumers

    pass_ = (
        (buy_n > 25) and 
        (buy_rate > 0.005) and 
        (buy_rate < 0.99) and
        (srh_n > 25) and
        (srh_rate > 0.005) and
        (num_srh < (J - 1))
    )

    return pass_, buy_rate, srh_rate, num_srh, buy_n, srh_n
