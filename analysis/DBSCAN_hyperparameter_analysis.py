# %% Imports
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from analysis_config import PREDICTION_VAR
# %% Load data
ds_path = 'data/DS_reduced_and_dropped.csv'
# ds_path = 'data/DS_RAndD_minmax.csv'
# ds_path = 'data/DS_RAndD_normalized.csv'
print('[Loading data] Start:', ds_path)
ds = pd.read_csv(ds_path, index_col='id')
print('[Loading data] Done')
# %% Separate data
feature_names = ds.columns[ds.columns != PREDICTION_VAR]
feature_data = ds[feature_names]

# %% Determine distances
NN_model = NearestNeighbors(n_neighbors=2, n_jobs=-1).fit(feature_data)
distances, indices = NN_model.kneighbors(feature_data)

# %% Save distances
np.save('data/distances/DBSCAN_HP_distances.npy',distances)
# np.save('data/distances/DBSCAN_HP_distances_minmax.npy',distances)
# np.save('data/distances/DBSCAN_HP_distances_normalized.npy',distances)