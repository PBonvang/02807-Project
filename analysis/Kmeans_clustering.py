# %% Imports
import pandas as pd
from sklearn.cluster import KMeans
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
K = 250

# %% Fit clusters
print('[Determining clusters] Start')
kmeans = KMeans(n_clusters=K)
labels = kmeans.fit_predict(feature_data)
print('[Determining clusters] Done')
# %% Save clusters
np.save(f"data/clusterings/Kmeans_clusterings_K{str(K)}.npy", labels)