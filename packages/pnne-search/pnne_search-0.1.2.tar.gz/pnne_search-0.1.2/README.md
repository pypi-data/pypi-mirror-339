This package `pnne_search` implements the pre-trained neural network estimator for sequential search model, as described by "Pre-Training Estimators for Structural Models: Application to Consumer Search"

See below for a simple demonstration of how to use `pnne_search`:

import time 
import pnne_search

data = pnne_search.load_example_data()

pnne_search.pnne_estimate(data['Y'], data['Xp'], data['Xa'], data['Xc'], 
                          data['consumer_idx'], checks = True)

start_time = time.time()
pnne_search.pnne_estimate(data['Y'], data['Xp'], data['Xa'], data['Xc'], 
                          data['consumer_idx'], checks = True, se=True)
time.time() - start_time

start_time = time.time()
pnne_search.pnne_estimate(data['Y'], data['Xp'], data['Xa'], data['Xc'], 
                          data['consumer_idx'], checks = True, se=True, use_parallel=False)
time.time() - start_time
