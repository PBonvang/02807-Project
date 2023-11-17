# %% Jupyter extensions
%load_ext autoreload
%autoreload 2
# %% Imports
import json
import pandas as pd
from pathlib import Path

from utils.preprocessing import get_file_metadata, json_list_to_csv
from config import BBR_DATA_PATH, DATA_FOLDER

#%%
FullBuildingList_path = DATA_FOLDER / 'BuildingListBBR_FULL.json'
BuildingList_path = DATA_FOLDER / 'BBR_BuildingList.csv'

#%%
BBR_metadata_path = DATA_FOLDER / 'BBR_metadata.json'
BBR_metadata = get_file_metadata(BBR_DATA_PATH, BBR_metadata_path)
BBR_metadata

# %% HusnummerList
json_list_to_csv(
    BBR_DATA_PATH,
    BBR_metadata['BygningList'],
    BuildingList_path,
    attributes=[
        'id_lokalId',
        'status',
        'byg007Bygningsnummer',
        'byg021BygningensAnvendelse',
        'byg026Opførelsesår',
        'byg027OmTilbygningsår',
        'byg030Vandforsyning',
        'byg031Afløbsforhold',
        'byg032YdervæggensMateriale',
        'byg033Tagdækningsmateriale',
        'byg034SupplerendeYdervæggensMateriale',
        'byg035SupplerendeTagdækningsMateriale',
        'byg036AsbestholdigtMateriale',
        'byg038SamletBygningsareal',
        'byg039BygningensSamledeBoligAreal',
        'byg040BygningensSamledeErhvervsAreal',
        'byg041BebyggetAreal',
        'byg042ArealIndbyggetGarage',
        'byg043ArealIndbyggetCarport',
        'byg044ArealIndbyggetUdhus',
        'byg045ArealIndbyggetUdestueEllerLign',
        'byg046SamletArealAfLukkedeOverdækningerPåBygningen',
        'byg047ArealAfAffaldsrumITerrænniveau',
        'byg048AndetAreal',
        'byg049ArealAfOverdækketAreal',
        'byg051Adgangsareal',
        'byg054AntalEtager',
        'byg055AfvigendeEtager',
        'byg056Varmeinstallation',
        'byg057Opvarmningsmiddel',
        'byg058SupplerendeVarme',
        'byg069Sikringsrumpladser',
        'byg070Fredning',
        'byg111StormrådetsOversvømmelsesSelvrisiko',
        'byg112DatoForRegistreringFraStormrådet',
        'byg130ArealAfUdvendigEfterisolering',
        'byg136PlaceringPåSøterritorie',
        'jordstykke',
        'husnummer',
        'ejerlejlighed',
        'grund'
    ])

#%%
BygningList_data = pd.read_csv(BuildingList_path, delimiter=';')
# %%
columns_to_remove = []
for col in BygningList_data.columns:
    if not (~BygningList_data[col].isna()).any():
        print(col)
        columns_to_remove.append(col)

new_BygningList_data = BygningList_data.loc[:, set(BygningList_data.columns) - set(columns_to_remove)]

#%%
new_BygningList_data.to_csv(
    DATA_FOLDER / 'BBR_BuildingList2.csv', sep=';')

#%% Remove Apartments
BygningList_data_no_apartments = new_BygningList_data[new_BygningList_data['ejerlejlighed'].isna()]

#%% Remove non-residence buildings
residence_building_ids = [120, 121, 122, 130, 131, 132, 140, 190]
BygningList_data_residence_places = BygningList_data_no_apartments[BygningList_data_no_apartments['byg021BygningensAnvendelse'].isin(residence_building_ids)]
# %% Save the filtered version
BygningList_data_residence_places.to_csv(
    DATA_FOLDER / 'BBR_BuildingList_filtered.csv', sep=';')
