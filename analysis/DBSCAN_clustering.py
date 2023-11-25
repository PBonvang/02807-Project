# %% Imports
import pandas as pd
from sklearn.cluster import DBSCAN
import numpy as np
# %% Load data
print('[Loading data] Start')
ds = pd.read_csv('data/DS_reduced_and_dropped.csv', index_col='id')
print('[Loading data] Done')
# %% Separate data
# Prediction variable
prediction_property = 'totalAddressValue'
total_address_values = ds[prediction_property]

# Feature data
feature_names = ds.columns[ds.columns != prediction_property]
feature_data = ds[feature_names]
# %% Hyperparameters
# https://medium.com/@tarammullin/dbscan-parameter-estimation-ff8330e3a3bd
eps = 329
min_samples = 2*len(feature_names)

# %% Fit clusters
print('[Determining clusters] Start')
dbscan = DBSCAN(eps=eps, min_samples=min_samples, n_jobs=-1)
dbscan.fit(feature_data)
print('[Determining clusters] Done')
# %% Save clusters
db_clusterings = dbscan.labels_
np.save(f'data/DBSCAN_clusterings_eps{eps}_ms{min_samples}_DS_reduced_and_dropped.npy', db_clusterings)