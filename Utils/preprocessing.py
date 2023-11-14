
from collections import defaultdict
from pathlib import Path
from pandas import DataFrame, concat
from tqdm import tqdm
import json
import csv

from config import LIST_IDENTIFIER

def get_attribute_from_json_line(line: str)->str:
    return line.split(':')[0][1:-1]

def clean_file(data_path: Path, output_path: Path) -> None:
    with tqdm(total=data_path.stat().st_size) as pbar:
        with data_path.open(encoding='utf-8') as data_file:
            with output_path.open('w', encoding='utf-8') as output_file:
                while line := data_file.readline():
                    if line.strip() == '': continue

                    output_file.write(line)

def get_file_metadata(data_path: Path, save_path: Path = None)->dict:
    file_metadata = dict()

    with tqdm(total=data_path.stat().st_size) as pbar:
        with data_path.open(encoding='utf-8') as file:
            sample = {}
            determine_attributes = False

            i = 0
            list_name = ''
            while line := file.readline():
                if LIST_IDENTIFIER in line:
                    if list_name in file_metadata: 
                        file_metadata[list_name]['end_line'] = i-2
                        file_metadata[list_name]['attributes'] = list(sample.keys())
                        file_metadata[list_name]['sample'] = sample

                    list_name = get_attribute_from_json_line(line)
                    file_metadata[list_name] = {'start_line':i}

                    sample = {}
                    determine_attributes = True
                
                elif determine_attributes and '}' in line:
                    determine_attributes = False
                
                elif determine_attributes and ':' in line:
                    attribute, value = get_json_key_value_pair(line)
                    sample[attribute] = value
                    
                i += 1
                if not i % 1000:
                    pbar.update(file.tell() - pbar.n)

            if list_name in file_metadata: 
                file_metadata[list_name]['end_line'] = i-2
                file_metadata[list_name]['attributes'] = list(sample.keys())
                file_metadata[list_name]['sample'] = sample
                
    if save_path is not None:
        with save_path.open('w', encoding='utf-8') as outfile:
            json.dump(file_metadata, outfile)

    return file_metadata

def get_json_key_value_pair(json_line: str) -> tuple[str]:
    attribute, value = list(
        map(str.strip, json_line\
            .replace('"','')\
            .replace(',\n','')\
            .replace('\n','')\
            .split(':',1))
    )
    return attribute, value

def json_list_to_csv(json_file: Path,
                     list_metadata: dict,
                     output_file: Path,
                     attributes: list[str] = None) -> None:
    
    if attributes is None:
        attributes = list_metadata['attributes']

    with tqdm(total=list_metadata['end_line']) as pbar:
        with json_file.open(encoding='utf-8') as file:
            with output_file.open('w', encoding='utf-8',newline='') as output_file:
                csvwriter = csv.DictWriter(output_file, fieldnames=attributes, delimiter=";")
                csvwriter.writeheader()

                data_point = {}
                for i in range(list_metadata['end_line']):
                    line = file.readline()

                    if not i % 1000:
                        pbar.update(1000)

                    if i <= list_metadata['start_line']: # Skip to list
                        continue
                    
                    if ':' in line:
                        attribute, value = get_json_key_value_pair(line)
                        if attribute in attributes:
                            data_point[attribute] = value

                    if '}' in line and len(data_point.keys()) > 0:
                        csvwriter.writerow(data_point)
                        data_point = {}




                

