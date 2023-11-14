# %% Jupyter extensions
%load_ext autoreload
%autoreload 2
# %% Imports
import pandas as pd
from pathlib import Path
from data.DAR import DAR_PATH

from utils.preprocessing import get_file_metadata, json_list_to_csv

#############################################################
# DAR
#############################################################
# %% Metadata
DAR_path = Path('D:/DAR_Aktuelt_Totaludtraek_JSON_HF_20231105180006/DAR_Aktuelt_Totaludtraek_JSON_HF_20231105180006.json')

DAR_metadata = get_file_metadata(DAR_path, Path('data/DAR_metadata.json'))
DAR_metadata
# %% AdresseList to csv
json_list_to_csv(
    DAR_PATH,
    DAR_metadata['AdresseList'],
    Path('data/DAR_adresse_list.csv'))

# %%
