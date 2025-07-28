from tqdm import tqdm
import os
from glob import glob
import yaml
import json
import re
import argparse
from io import StringIO
import os
from datetime import datetime

github_raw_base_URL = "https://raw.githubusercontent.com/colonial-heritage/research-guides-dev/refs/heads/main/"

# example_path = "EXPORTS/PDF/niveau2/English/MilitaryAndNavy.pdf"


def download_button(level, language, name, extension):
    link_text = dict(pdf="Download PDF", docx="Download DOCX")
    link_text = link_text[extension.lower()]

    # language = "English" if language.lower().startswith("en") else "Dutch"
    link_path = f"EXPORTS/{extension.upper()}/{level}/{language}/{name}.{extension.lower()}"
    link = github_raw_base_URL + link_path

    return f"[{link_text}]({link}){{: .btn .btn-blue }}"
  

def front_matter(ra_name, level, lang):
    return f"""---
layout: default
title: {ra_name}
parent: {level}
nav_enabled: true
has_toc: true
date: {datetime.today().strftime("%Y-%m-%d")}
--- 
"""


    



# MD_DIR = "./EXPORTS/MD"

# mds = glob(MD_DIR + "/*/*.md")

# def add_button(md_str, link, link_text):
#     button_md = f"[{link_text}]({link}){{: .btn .btn-green }}"
#     return to_add + "\n\n" + md_str

# # def download_link_from_path(path):    

# BASE_URL = "https://research-aids.github.io/"

# for f in mds:
#     with open(f) as handle:
#         md_content = handle.read()
#         pdf_path = f.replace("MD", "PDF")
        
#         if os.path.isfile(pdf_path):
#             md_content = add_button(md_content, link, "Download PDF")

#         docx_path = f.replace("MD", "DOCX")
#         if os.path.isfile(docx_path):
#             md_content = add_button(md_content, link, "Download DOCX")

