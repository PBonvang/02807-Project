import os
import sys

sys.path.append(os.getcwd())

from config import BBR_DATA_PATH, DATA_FOLDER

from tqdm import tqdm

BUILDING_LIST_LINE_NUMBER = 55_911_629

def extract_specific_sequence_from_json_file(outfile_name: str, start_index: int = 0, start_character: str = '[', end_character: str = ']') -> None:
    i = 0
    outfile_path = DATA_FOLDER / outfile_name
    with tqdm(total=BBR_DATA_PATH.stat().st_size) as pbar:
        with BBR_DATA_PATH.open(encoding='utf-8') as file:
            with outfile_path.open('w', encoding='utf-8') as outfile:
                while line := file.readline():
                    i += 1
                    if not i % 1000:
                        pbar.update(file.tell() - pbar.n)
                    if i < start_index:
                        continue
                    outfile.write(line)

                    last_character_of_line = line.strip()[-1]
                    if last_character_of_line == end_character:
                        break


extract_specific_sequence_from_json_file('BuildingListBBR_FULL.json', BUILDING_LIST_LINE_NUMBER)
