# %% Imports
import pandas as pd
import numpy as np
from analysis_config import PREDICTION_VAR
import sys
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
from scipy.stats import norm
from tqdm import tqdm
tqdm.pandas()

import warnings
warnings.filterwarnings("ignore")
# %% Load data
print('[Loading data] Start')
ds = pd.read_csv('../data/DS_abnormality.csv', index_col='id')
print('[Loading data] Done')
# %% Configuration
feature_names = ds.columns[ds.columns != PREDICTION_VAR]
seed = 42
T = 1/100
reference_dist = norm()
############################################################
# Creating test dataset
############################################################
# %% Get normal obs and change their evaluation
normal_obs = ds.loc[ds['isAbnormal'] == 0].sample(frac=1/10, random_state=seed).copy()
normal_obs['multiplier'] = np.random.choice([-2,2], len(normal_obs), replace=True)
normal_obs[PREDICTION_VAR] = normal_obs[PREDICTION_VAR]*normal_obs['multiplier']
normal_obs['label'] = 1
normal_obs

# %% Get abnormal ones and change evaluation to the average of the K nearest normal ones to check if it will make it normal
def get_average_of_normal_KNN(abnormal_row, NN_model: NearestNeighbors, evaluations: pd.Series):
    distances, indicies = NN_model.kneighbors(abnormal_row[feature_names].to_numpy().reshape(1, -1))
    nearest_neighbor_evaluations = evaluations[indicies[0][1:]]
    
    return nearest_neighbor_evaluations.mean()

abnormal_obs = ds.loc[(ds['isAbnormal'] == 1) & (ds['cluster'] != -1)].sample(frac=1/10, random_state=seed).copy()
K = 5
for cluster_id in tqdm(abnormal_obs['cluster'].unique()):
    norm_cluster = ds.loc[(ds['cluster'] == cluster_id) & (ds['isAbnormal'] == 0)]
    abnorm_mask = abnormal_obs['cluster'] == cluster_id
    abnorm_cluster = abnormal_obs.loc[abnorm_mask]

    cluster_NN = NearestNeighbors(n_neighbors=K).fit(norm_cluster[feature_names])
    abnormal_obs.loc[abnorm_mask, PREDICTION_VAR] = abnorm_cluster.apply(lambda row: get_average_of_normal_KNN(row, cluster_NN, norm_cluster[PREDICTION_VAR]), axis=1)

abnormal_obs['label'] = 0
abnormal_obs
# %% Test set
ds_test = pd.concat([normal_obs, abnormal_obs])
ds_test

############################################################
# Creating test dataset
############################################################
# %% Predict
for cluster_id in tqdm(ds_test['cluster'].unique()):
    cluster = ds.loc[ds['cluster'] == cluster_id]
    cluster_evals = cluster[PREDICTION_VAR]

    test_cluster_mask = ds_test['cluster'] == cluster_id
    test_cluster = ds_test.loc[test_cluster_mask]
    zs = (test_cluster[PREDICTION_VAR] - cluster_evals.mean())/cluster_evals.std()
    ps = 1 - reference_dist.cdf(np.abs(zs))

    ds_test.loc[test_cluster_mask,'prediction'] = (ps<T).astype(int)

ds_test

# %% Evaluation
print(confusion_matrix(ds_test['label'], ds_test['prediction'], normalize='true'))

t = ds_test.loc[ds_test['label'] == 1]
(t['label'] == t['prediction']).sum()/len(t)
# %%
