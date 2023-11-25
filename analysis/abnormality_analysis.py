# %% Imports
import pandas as pd
import numpy as np
from analysis_config import PREDICTION_VAR
import sys
# %% Load data
sys.stdout('[Loading data] Start')
ds = pd.read_csv('data/DS_RAndD_minmax.csv', index_col='id')

evaluations = ds[PREDICTION_VAR]
feature_names = ds.columns[ds.columns != PREDICTION_VAR]
feature_data = ds[feature_names]
sys.stdout('[Loading data] Done')
# %% Load clusters
sys.stdout('[Loading clusterings] Start')
clusterings = np.load('data/clusterings/DBSCAN_clusterings_minmax_eps1_1_ms236.npy')
sys.stdout('[Loading clusterings] Done')