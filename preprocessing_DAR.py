# %% Jupyter extensions
%load_ext autoreload
%autoreload 2
# %% Imports
import pandas as pd
from pathlib import Path

from utils.preprocessing import get_file_metadata, json_list_to_csv

# %% Data paths
DAR_path = Path('D:/DAR_Aktuelt_Totaludtraek_JSON_HF_20231105180006/DAR_Aktuelt_Totaludtraek_JSON_HF_20231105180006.json')
HusnummerList_path = Path('data/DAR/DAR_HusnummerList.csv')
PostnummerList_path = Path('data/DAR/DAR_PostnummerList.csv')
NavngivenVejList_path = Path('data/DAR/DAR_NavngivenVejList.csv')
#############################################################
# Gathering data
#############################################################
# %% Generate Metadata
DAR_metadata_path = Path('data/DAR/DAR_metadata.json')
DAR_metadata = get_file_metadata(DAR_path, DAR_metadata_path)
DAR_metadata
########################## DAR data to csv ##########################
# %% HusnummerList
json_list_to_csv(
    DAR_path,
    DAR_metadata['HusnummerList'],
    HusnummerList_path,
    attributes=[
        'id_lokalId',
        'status',
        'adgangsadressebetegnelse',
        'husnummertekst',
        'navngivenVej',
        'postnummer'
    ])

# %% PostnummerList
json_list_to_csv(
    DAR_path,
    DAR_metadata['PostnummerList'],
    PostnummerList_path,
    attributes=[
        'id_lokalId',
        'status',
        'navn',
        'postnr'
    ])
# %% NavngivenVejList
json_list_to_csv(
    DAR_path,
    DAR_metadata['NavngivenVejList'],
    NavngivenVejList_path,
    attributes=[
        'id_lokalId',
        'status',
        'vejnavn'
    ])

########################## Join DAR files ##########################
# %% Loading DAR data
HusnummerList_data = pd.read_csv(HusnummerList_path, delimiter=';')\
                        .rename(columns={
                            'id_lokalId':'husnummer_id',
                            'adgangsadressebetegnelse': 'address',
                            'husnummertekst':'house_nr',
                            'navngivenVej':'street_id',
                            'postnummer':'postal_id'
                        })
NavngivenVejList_data = pd.read_csv(NavngivenVejList_path, delimiter=';')\
                        .rename(columns={
                            'id_lokalId':'street_id',
                            'vejnavn':'street_name'
                        })
PostnummerList_data = pd.read_csv(PostnummerList_path, delimiter=';')\
                        .rename(columns={
                            'id_lokalId':'postal_id',
                            'navn': 'city_name',
                            'postnr':'postal_nr'
                        })
# %% Filter addresses
has_street = ~pd.isna(HusnummerList_data['street_id'])
is_house = HusnummerList_data['house_nr'].apply(lambda x: str.isnumeric(str(x)))

DAR_data = HusnummerList_data.loc[has_street]
DAR_data
# %% Join DAR data
DAR_joined_data = DAR_data.merge(NavngivenVejList_data.loc[:,['street_id','street_name']], how='left', on='street_id')\
                    .merge(PostnummerList_data.loc[:, ['postal_id','city_name','postal_nr']], how='left', on='postal_id')\
                    .loc[:, ['husnummer_id','address','house_nr','street_name','city_name','postal_nr']]
DAR_joined_data
# %% Save DAR data
DAR_joined_data_path = Path('data/DAR/DAR_joined_full.csv')
DAR_joined_data.to_csv(DAR_joined_data_path, sep=';', index=False)
# %%
