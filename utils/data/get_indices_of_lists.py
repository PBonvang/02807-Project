import os
import sys
import json

sys.path.append(os.getcwd())

from config import BBR_DATA_PATH, DATA_FOLDER

from tqdm import tqdm

LIST_IDENTIFIER = 'List":'



def get_attribute_from_json_line(line: str)->str:
    return line.split(':')[0][1:-1]

def get_indices_of_lists()->dict:
    i = 0
    list_indices = dict()
    with tqdm(total=BBR_DATA_PATH.stat().st_size) as pbar:
        with BBR_DATA_PATH.open(encoding='utf-8') as file:
            while line := file.readline():
                if LIST_IDENTIFIER in line:
                    attribute = get_attribute_from_json_line(line)
                    list_indices[attribute] = i
                    
                i += 1
                if not i % 1000:
                    pbar.update(file.tell() - pbar.n)

    return list_indices

def save_indices_of_list(indices_of_list: dict, outfile_name: str):
    outfile_path = DATA_FOLDER / outfile_name
    with outfile_path.open('w', encoding='utf-8') as outfile:
        json.dump(indices_of_list, outfile)

if __name__ == '__main__':
    indices_of_lists = get_indices_of_lists()
    save_indices_of_list(indices_of_lists, 'BBR_FULL_indices_of_lists.json')
