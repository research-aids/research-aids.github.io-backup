from tqdm import tqdm
import os
from glob import glob
import yaml
import json
import re

BASE_DIR = "."
OUT_DIR = f"{BASE_DIR}/forKinsukAndSjors"



eng = glob(f"{BASE_DIR}/*/English/*.yml")
dutch = glob(f"{BASE_DIR}/*/Dutch/*.yml")
top = glob(f"{BASE_DIR}/TopLevel/*.yml")

yaml_files = top + dutch + eng

with open(f"{OUT_DIR}/action_results.txt", "w") as handle:
  handle.write(str(yaml_files))
