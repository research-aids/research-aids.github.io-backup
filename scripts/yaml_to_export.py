from tqdm import tqdm
import os
from glob import glob
import yaml
import json
import re
import argparse
from io import StringIO


# unused: from docx import Document
from Markdown2docx import Markdown2docx
# from md2docx_python.src.md2docx_python import markdown_to_word

from markdown_pdf import MarkdownPdf, Section
from yaml_to_markdown.md_converter import MDConverter
MD_CONV = MDConverter()

from ResearchAids import ResearchAid
from md_to_website import download_button, front_matter


IN_DIR = "./published"
OUT_DIR = "./EXPORTS"

eng = glob(f"{IN_DIR}/*/English/*.yml")
dutch = glob(f"{IN_DIR}/*/Dutch/*.yml")
# top = glob(f"{BASE_DIR}/TopLevel/*.yml")

yaml_files = sorted(dutch + eng)


def parse_filename(orig_path, has_path=False):
    path_part = '.+\/' if has_path else ''
    m = re.search(f'{path_part}(.*)_[0-9]+\.yml', orig_path)
    if m:
        return m.group(1)
    raise ValueError(f"{orig_path} couldn't be parsed!")

def parse_filepath(fp):
    *pref, level, lang, fname  = fp.split(os.path.sep)
    return level, lang, parse_filename(fname)


def export_markdown(f, out_dir, level, lang, name, return_content=True):
    md_name = f"{out_dir}/MD/{level}/{lang}/{name}.md"
    os.makedirs(os.path.dirname(md_name), exist_ok=True)
    
    with open(f) as handle:
        yaml_content = yaml.safe_load(handle)
        ra = ResearchAid(yaml_content)
        if ra._parsed:
            md_content = ra()
            with open(md_name, "w") as md_handle:
                md_handle.write(md_content)

            
            website_name = md_name.replace("/MD/", "/WEBSITE/")
            os.makedirs(os.path.dirname(website_name), exist_ok=True)
            website_content = front_matter(ra.title, level, lang) + "\n\n" +\
                                "this new string from 28.07.2025\n\n" +\
                                download_button(level, lang, name, "PDF") + "     " +\
                                download_button(level, lang, name, "DOCX") +\
                                "\n\n" + md_content

            with open(website_name, "w") as web_handle:
                web_handle.write(website_content)

            with open(f"{out_dir}/WEBSITE/{level}/{level}.md", "w") as md:
                level_md = f"""---
layout: default
title: {level}
nav_enabled: true
has_toc: true
parent: Published
---
This is level {level[-1]} of the RAs.
"""
                md.write(level_md)

            return md_content
        
        
    #     yaml_content["author"] = "wreints"

    #     with open(md_name, "w") as md_handle:
    #         MD_CONV.convert(yaml_content, md_handle)     

    # with open(md_name) as handle:
    #     markdown_content = handle.read()
    #     return markdown_content

def remove_imgs(md):
    img_regex = re.compile(r"!\[.+\]\(.+\)")

    md_copy = md[:]
    for instance in img_regex.findall(md_copy):
        md_copy = md_copy.replace(instance, instance[1:])
    return md_copy


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--file_format", help="Output file format, PDF, DOCX and Markdown are supported.")
    args = argparser.parse_args()
    if not args.file_format or (not args.file_format.lower().strip() in ("pdf", "docx", "md")):
        raise ValueError("Please specify either PDF, DOCX or Markdown ('md')!")

    fmt = args.file_format

    didnt_parse = []
    failed_to_save = []
    for f in tqdm(yaml_files):
        # print(f"processing {f}...")

        level, lang, name = parse_filepath(f)

        new_name = f"{OUT_DIR}/{fmt.upper()}/{level}/{lang}/{name}.{fmt}"
        os.makedirs(os.path.dirname(new_name), exist_ok=True)

        markdown_content = export_markdown(f, OUT_DIR, level, lang, name)
        if not markdown_content:
            didnt_parse.append(f)
            continue
            
        if fmt.lower() == "pdf":
            # print("!!!SAVING PDF")
            pdf = MarkdownPdf()#toc_level=2)
            pdf.add_section(Section(markdown_content, toc=False))
            pdf.meta["title"] = name
            pdf.meta["author"] = "wreints"
            # print(f"saving {new_name}")
            pdf.save(new_name)
        elif fmt.lower() == "docx":
            try:
                docx_md_content = remove_imgs(markdown_content)
                # raise Exception("bold and italics don't render!")
                docx = Markdown2docx(name, markdown=[docx_md_content])
                docx.eat_soup()
                docx.outfile = new_name
                docx.save()
            except TypeError:
                print(f"EXPORTING {f} TO DOCX FAILED!")
                failed_to_save.append(f)
                continue
        else:
            pass

    if didnt_parse:
        with open(f"{OUT_DIR}/didnt_parse.txt", "w") as handle:
            handle.write("\n".join(didnt_parse))


    if failed_to_save:
        with open(f"{OUT_DIR}/failed_to_save.txt", "w") as handle:
            handle.write("\n".join(failed_to_save))