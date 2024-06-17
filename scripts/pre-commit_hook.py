from tqdm import tqdm
import os
from glob import glob
import yaml
import json

BASE_DIR = "."
OUT_DIR = f"{BASE_DIR}/forKinsukAndSjors"



eng = glob(f"{BASE_DIR}/*/English/*.yml")
dutch = glob(f"{BASE_DIR}/*/Dutch/*.yml")
top = glob(f"{BASE_DIR}/TopLevel/*.yml")

yaml_files = top + dutch + eng


def get_filename(orig_path):
    import re

    m = re.search(f'.+\/(.*)_[0-9]+\.yml', orig_path)
    if m:
        return m.group(1)
    raise ValueError(f"{orig_path} couldn't be parsed!")



for f in tqdm(yaml_files):
    print(f"processing {f}...")
    try:
        with open(f) as handle:
            yaml_content = yaml.safe_load(handle)
    
        yaml_content["File name"] = get_filename(f)
    
        
        new_name = f.split(os.path.sep, maxsplit=1)[1]
        new_name = new_name.replace(".yml", ".json")
        new_name = f"{OUT_DIR}/{new_name}"
    
        os.makedirs(os.path.dirname(new_name), exist_ok=True)
        with open(new_name, "w") as handle:
            json.dump(yaml_content, handle)

    
    except yaml.scanner.ScannerError:
        print(f)
        exit(1)
    except yaml.parser.ParserError:
        print(f)
        exit(1)
    except ValueError:
        print(f"{f}'s filename can't be parsed")
        exit(1)

exit(1)