# %% Imports
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import pickle
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
print('[No scaling] Fitting')
poly_features = PolynomialFeatures(degree=2, include_bias=False)\
    .fit_transform(feature_data)
poly_model = LinearRegression(n_jobs=-1).fit(poly_features, total_address_values)
print('[No scaling] Fitting done')

# Coefficient of determination
coef_det = poly_model.score(poly_features, total_address_values)
print(f'[No scaling] Coefficient of determination: {coef_det}')

if coef_det > 0.315:
    with open('data/models/PR_model.sav', 'wb') as f:
        pickle.dump(poly_model, f)
#############################################################
# %% Standard scaling
#############################################################
scaler = StandardScaler()
normalized_feature_data = scaler.fit_transform(feature_data)

print('[Standard scaling] Fitting')
poly_features = PolynomialFeatures(degree=2, include_bias=False)\
    .fit_transform(normalized_feature_data)
poly_model = LinearRegression(n_jobs=-1).fit(poly_features, total_address_values)
print('[Standard scaling] Fitting done')

# Coefficient of determination
coef_det = poly_model.score(poly_features, total_address_values)
print(f'[Standard scaling] Coefficient of determination: {coef_det}')

if coef_det > 0.315:
    with open('data/models/PR_standard_model.sav', 'wb') as f:
        pickle.dump(poly_model, f)
#############################################################
# %% MinMax scaling
#############################################################
scaler = MinMaxScaler()
normalized_feature_data = scaler.fit_transform(feature_data)

print('[MinMax scaling] Fitting')
poly_features = PolynomialFeatures(degree=2, include_bias=False)\
    .fit_transform(normalized_feature_data)
poly_model = LinearRegression(n_jobs=-1).fit(poly_features, total_address_values)
print('[MinMax scaling] Fitting done')

# Coefficient of determination
coef_det = poly_model.score(poly_features, total_address_values)
print(f'[MinMax scaling] Coefficient of determination: {coef_det}')

if coef_det > 0.315:
    with open('data/models/PR_minmax_model.sav', 'wb') as f:
        pickle.dump(poly_model, f)