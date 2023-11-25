# %% Imports
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler, MinMaxScaler
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

#############################################################
# %% No scaling
#############################################################
# %% Determine distances
NN_model = NearestNeighbors(n_neighbors=2, n_jobs=-1).fit(feature_data)
distances, indices = NN_model.kneighbors(feature_data)

# %% Save distances
np.save('data/DBSCAN_HP_distances.npy',distances)

#############################################################
# %% Standard scaling
#############################################################
scaler = StandardScaler()
normalized_feature_data = scaler.fit_transform(feature_data)

# %% Determine distances
NN_model = NearestNeighbors(n_neighbors=2, n_jobs=-1).fit(normalized_feature_data)
distances, indices = NN_model.kneighbors(normalized_feature_data)

# %% Save distances
np.save('data/DBSCAN_HP_distances_standard.npy',distances)

#############################################################
# %% MinMax scaling
#############################################################
scaler = MinMaxScaler()
normalized_feature_data = scaler.fit_transform(feature_data)

# %% Determine distances
NN_model = NearestNeighbors(n_neighbors=2, n_jobs=-1).fit(normalized_feature_data)
distances, indices = NN_model.kneighbors(normalized_feature_data)

# %% Save distances
np.save('data/DBSCAN_HP_distances_minmax.npy',distances)