# %% Imports
import pandas as pd
from sklearn.cluster import DBSCAN
import numpy as np
from analysis_config import PREDICTION_VAR
# %% Load data
print('[Loading data] Start')
ds = pd.read_csv('data/DS_RAndD_minmax.csv', index_col='id')
print('[Loading data] Done')
# %% Separate data
feature_names = ds.columns[ds.columns != PREDICTION_VAR]
feature_data = ds[feature_names]
# %% Hyperparameters
# https://medium.com/@tarammullin/dbscan-parameter-estimation-ff8330e3a3bd
eps = 1.1
min_samples = 2*len(feature_names)

# %% Fit clusters
print('[Determining clusters] Start')
dbscan = DBSCAN(eps=eps, min_samples=min_samples, n_jobs=-1)
dbscan.fit(feature_data)
print('[Determining clusters] Done')
# %% Save clusters
db_clusterings = dbscan.labels_
np.save(f'data/clusterings/DBSCAN_clusterings_minmax_eps{eps}_ms{min_samples}.npy', db_clusterings)