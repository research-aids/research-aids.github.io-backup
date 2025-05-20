from tqdm import tqdm
import yaml
from glob import glob
import os

import networkx as nx
# import matplotlib.pyplot as plt


BASE_DIR = "./published"
eng = glob(f"{BASE_DIR}/*/English/*.yml")
dutch = glob(f"{BASE_DIR}/*/Dutch/*.yml")
# top = glob(f"{BASE_DIR}/TopLevel/*.yml")

yaml_files = dutch + eng

for f in tqdm(yaml_files):
    print(f"processing {f}...")
    with open(f) as handle:
        yaml_content = yaml.safe_load(handle)



print(f"SUCCESS: all {len(yaml_files)} parsed properly, i.e. are valid YAML")

def remove_path(f):
    return (f.rsplit(".")[-2]).rsplit("/")[-1]


links = {}
for f in tqdm(yaml_files):
    with open(f) as handle:
        d = yaml.safe_load(handle)
        if "RelatedAides" in d:
            rels = {v['link']: v["rel_type"] for sub in d["RelatedAides"] for k, v in sub.items()}
            links[remove_path(f)] = sorted(map(remove_path, rels.keys()))

G = nx.from_dict_of_lists(links)

if nx.is_connected(G):
    print(f"SUCCESS: there are no orphaned guides, i.e. every guide is referred to be at least another one!")
else:
    raise ValueError("There are orphans in the graph!")







