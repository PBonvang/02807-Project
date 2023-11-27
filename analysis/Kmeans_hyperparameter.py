# %% Imports
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from analysis_config import PREDICTION_VAR
import matplotlib.pyplot as plt
# %% Load data
#ds_path = 'data/DS_reduced_and_dropped.csv'
ds_path = 'data/DS_RAndD_minmax.csv'
# ds_path = 'data/DS_RAndD_normalized.csv'
print('[Loading data] Start:', ds_path)
ds = pd.read_csv(ds_path, index_col='id')
print('[Loading data] Done')
# %% Separate data
feature_names = ds.columns[ds.columns != PREDICTION_VAR]
feature_data = ds[feature_names]

# %% Determine optimal K
sum_of_sq_dists = []
Ks = range(100,300,25)
for K in Ks:
    kmeans = KMeans(n_clusters=K, random_state=42, n_init=10)
    kmeans.fit(feature_data)
    sum_of_sq_dists.append(kmeans.inertia_)
plt.plot(Ks,sum_of_sq_dists, '.-')
plt.xlabel('K')
plt.ylabel('Sum of squared distances')
plt.title('Optimal K')
plt.savefig('../assets/Kmeans.png')