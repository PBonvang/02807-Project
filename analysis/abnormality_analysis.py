# %% Imports
import pandas as pd
import numpy as np
from analysis_config import PREDICTION_VAR
import sys
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from scipy.stats import norm
from tqdm import tqdm
tqdm.pandas()

import warnings
warnings.filterwarnings("ignore")
# %% Load data
sys.stdout.write('[Loading data] Start\n')
ds = pd.read_csv('../data/DS_RAndD_minmax.csv', index_col='id')

evaluations = ds[PREDICTION_VAR]
feature_names = ds.columns[ds.columns != PREDICTION_VAR]
feature_data = ds[feature_names]
sys.stdout.write('[Loading data] Done\n')
# %% Load clusters
sys.stdout.write('[Loading clusterings] Start\n')
clusterings = np.load('../data/clusterings/DBSCAN_clusterings_minmax_eps1_1_ms236.npy')
sys.stdout.write('[Loading clusterings] Done\n')
# %% Hyperparameters
K = 100
T = 1/100
reference_dist = norm()
# %% Abnormality analysis
def check_outlier_abnormality(row, NN_model, evaluations):
    distances, indicies = NN_model.kneighbors(row[feature_names].to_numpy().reshape(1, -1))
    nearest_neighbor_evaluations = evaluations[indicies[0][1:]]
    z =  (row[PREDICTION_VAR] - nearest_neighbor_evaluations.mean())/nearest_neighbor_evaluations.std()
    p = 1 - reference_dist.cdf(abs(z))

    return 0 if p > T else 1

abnormality_ds = pd.DataFrame()
cluster_ids = np.unique(clusterings)
for cluster_id in tqdm(cluster_ids):
    cluster_mask = clusterings==cluster_id
    cluster = ds[cluster_mask]
    cluster['cluster'] = cluster_id

    if cluster_id == -1: # Outliers
        cluster['isAbnormal'] = 1
        # cluster_NN = NearestNeighbors(n_neighbors=K+1).fit(feature_data) # K+1 because it will find itself
        # cluster['isAbnormal'] = cluster.progress_apply(lambda row: check_outlier_abnormality(row, cluster_NN, evaluations), axis=1)
    else:
        zs = StandardScaler().fit_transform(cluster[PREDICTION_VAR].to_numpy().reshape(-1, 1))
        ps = 1 - reference_dist.cdf(np.abs(zs))

        cluster['isAbnormal'] = (ps<T).astype(int)

    abnormality_ds = pd.concat([abnormality_ds, cluster])

abnormality_ds.to_csv('../data/DS_abnormality.csv')