import requests,re, sys
import pandas as pd
import numpy as np
from tqdm import tqdm
from requests_ratelimiter import LimiterSession
session = LimiterSession(per_second=10)

def property_assessment(addressID: str, verbose=False):
    url = "https://api-fs.vurderingsportalen.dk/preliminaryproperties/_search"

    query = {
      "query": {
        "bool": {
          "must": [
            {
              "match_phrase": {
                "adgangsAdresseID": f"{addressID}"
              }
            }
          ],
          "filter": [
            {
              "bool": {
                "should": []
              }
            },
            {
              "match": {
                "documentType": 4
              }
            }
          ]
        }
      }
    }

    headers = {
        "Content-Type": "application/json",
    }
    
    response = session.post(url, json=query, headers=headers)

    if verbose:
        if response.status_code == 200:
            print("Success:")
            print(response.json())
        else:
            print("Failed to fetch data:")
            print("Status code:", response.status_code)
            print("Response:", response.text)
        
    return response.json()

def scrape(idx_start:int, idx_end:int, DAR_PATH:str='DAR_joined.csv', debug=False):
    """
    Can be run with "python <path to scrape.py> <idx_start> <idx_end> <DAR_PATH> <debug>"
    
    Args:
        idx_start (int): Start index of scraping. Must be greater than or equal to 0
        idx_end (int): End index of scraping. Must be less or equal to 2259957
        DAR_PATH (str): Path to "DAR_joined.csv"
        debug (bool, optional): Enables verbose and checks if 3 debug samples or scraped (index 0 to 2). Defaults to False.
    """
    columns = {'id':int,'adgangsAdresseID':str,
               'vurderingsaar':int,'propertyValue':float,
               'groundValue':float,'propertyTax':float,
               'groundTax':float,'totalAddressTax':float}

    debug_samples = ['0a3f507c-036b-32b8-e044-0003ba298018','2edda757-9218-1605-e044-0003ba298018','0a3f5083-e355-32b8-e044-0003ba298018'] #Middle one is invalid

    output_file = f'VUR_{idx_start}_to_{idx_end}.csv'
    
    pd.DataFrame(columns=columns.keys()).to_csv(output_file, index=False, sep=';')

    if debug:
        addressIDs = debug_samples
    else:
        addressIDs = pd.read_csv(DAR_PATH, delimiter=';').husnummer_id.iloc[idx_start:idx_end]

    for id in tqdm(addressIDs, desc='Scraping in progress', total=len(addressIDs)):
        response = property_assessment(id, verbose=debug)
        try:
            source = response['hits']['hits'][0]['_source']
            taxCalculations = source.pop('taxCalculation')
            source.update({k:re.sub("[^0-9]", "", v) for k, v in taxCalculations.items()})
            pd.DataFrame({key:source[key] for key in columns.keys()},index=[0]).to_csv(output_file, mode='a',index=False, header=False, sep=';')
        except IndexError:
            pass
        
        except KeyError as error:
            
            if error.args[0] == 'taxCalculation': # Basically fill tax columns with NaNs
              for k in columns.keys():
                pattern = re.compile(r'tax', re.IGNORECASE)
                if pattern.search(k):
                  source[k] = np.nan
            pd.DataFrame({key:source[key] for key in columns.keys()},index=[0]).to_csv(output_file, mode='a',index=False, header=False, sep=';')
                  
        
    VUR_edit = pd.read_csv(output_file, delimiter=';')
    for col, dtype in columns.items():
        VUR_edit[col] = VUR_edit[col].astype(dtype)
    VUR_edit.to_csv(output_file,index=False, header=True, sep=';')

# Examples
#scrape(1123328,1123332,r'<path_to>\DAR_joined.csv') #Solbakkevej 68 included - test
#scrape(5587,5600)

scrape(*map(int,sys.argv[1:3]),*sys.argv[3:5]) # Run it CL (easier like this for HPC)