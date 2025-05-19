from tqdm import tqdm
import os
from glob import glob
import yaml
import json
import re
import argparse
from io import StringIO
import os

MD_DIR = "./EXPORTS/MD"

mds = glob(MD_DIR + "/*/*.md")

def add_button(md_str, link, link_text):
    to_add = f"[link_text]({link}){{: .btn .btn-green }}"
    return to_add + "\n\n" + md_str

# def download_link_from_path(path):    

for f in mds:
    with open(f) as handle:
        pdf_path = f.replace("MD", "PDF")
        if os.path.isfile(pdf_path):
            md_content = add_button(handle.read(), , "Download PDF")

        docx_path = f.replace("MD", "DOCX")
        if os.path.isfile(docx_path):
            md_content = add_button(handle.read(), "", "Download DOCX")

