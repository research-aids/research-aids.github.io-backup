from tqdm import tqdm
import os
from glob import glob
import yaml
import json
import re

# copied from: https://stackoverflow.com/questions/34667108/ignore-dates-and-times-while-parsing-yaml
# used to stop the YAML parser to parse datetime strings -- which aren't a valid datatype in JSON
class NoDatesSafeLoader(yaml.SafeLoader):
    @classmethod
    def remove_implicit_resolver(cls, tag_to_remove):
        """
        Remove implicit resolvers for a particular tag

        Takes care not to modify resolvers in super classes.

        We want to load datetimes as strings, not dates, because we
        go on to serialise as json which doesn't have the advanced types
        of yaml, and leads to incompatibilities down the track.
        """
        if not 'yaml_implicit_resolvers' in cls.__dict__:
            cls.yaml_implicit_resolvers = cls.yaml_implicit_resolvers.copy()

        for first_letter, mappings in cls.yaml_implicit_resolvers.items():
            cls.yaml_implicit_resolvers[first_letter] = [(tag, regexp) 
                                                         for tag, regexp in mappings
                                                         if tag != tag_to_remove]

NoDatesSafeLoader.remove_implicit_resolver('tag:yaml.org,2002:timestamp')



BASE_DIR = "./published"
OUT_DIR = "./forKinsukAndSjors"



eng = glob(f"{BASE_DIR}/*/English/*.yml")
dutch = glob(f"{BASE_DIR}/*/Dutch/*.yml")
# top = glob(f"{BASE_DIR}/TopLevel/*.yml")

yaml_files = dutch + eng


def parse_filename(orig_path, has_path=False):

    path_part = '.+\/' if has_path else ''
    m = re.search(f'{path_part}(.*)_[0-9]+\.yml', orig_path)
    if m:
        return m.group(1)
    raise ValueError(f"{orig_path} couldn't be parsed!")

def parse_filepath(fp):
    *pref, level, lang, fname  = fp.split(os.path.sep)
    return level, lang, parse_filename(fname)


def addlinkFilename(rels, lang):
    sub = "Subtopics" if lang == "English" else "Deelonderwerpen"
    for d1 in rels:
        ((n, val),) = d1.items()
        level, lang, name = parse_filepath(val['link'])
        val = val | {"linkFilename": f"{level}/{lang}/{name}_{lang}"}
        if sub in val:
            val[sub] = list(addlinkFilename(val[sub], lang=lang)) 
        
        yield {n: val}

# def addlinkFilename_recurse(



def addEntityInfotoText(d, lang):
    assert lang in ("English", "Dutch")
    main = d["Main-text"]["content"]
    rlv = d["Relevant data"]

    header = "Name variations" if lang == "English" else "Naamsvarianten"
    name_vars = "\n".join(f" - {v}" for v in rlv['Name variations'])
    main += f"\n### {header}\n{name_vars}\n\n"

    header = "Period of activity" if lang == "English" else "Periode actief"
    period = f"{rlv['Period of activity']['Year of start']} -- {rlv['Period of activity']['Year of end']}"
    main += f"\n### {header}\n{period}\n\n"

    if isinstance(rlv['Identifiers'], list):
        header = "External identifiers" if lang == "English" else "Externe identificatie"
        external = "\n".join(f" - {v}" for v in rlv['Identifiers'])
        main += f"\n### {header}\n{external}\n\n"
    # d["Main-text"]["content"] = main
    
    return main


def add_sort_order_to_item_list(ls):
    for i, item in enumerate(ls, 1):
        item_title, item_fields = tuple(item.items())[0]
        item_fields.update({"sort_order": i})
        subtopics = item_fields.get("Deelonderwerpen", None) or item_fields.get("Subtopics", None)
        if subtopics:
            add_sort_order_to_item_list(subtopics)


def correct_IRI(url):
    # correct IRIs:
    #  - https://sws.geonames.org/6255149/
    #  - http://vocab.getty.edu/aat/300266789
    # -- http://www.wikidata.org/entity/Q219477
    md_link_re = re.compile(r"\[(.*)\]\(https?:\/\/(?:sws|www).geonames.org\/([0-9]+)\/?.*\)")
    # uri_re = re.compile(r"^https?:\/\/(?:sws|www).geonames.org\/([0-9]+)\/?.*")

    if md_link_re.match(url):
        link_text, geonames_id = md_link_re.match(url).group(1), md_link_re.match(url).group(2)
        return f"[{link_text}](https://sws.geonames.org/{geonames_id}/)"
    elif ("http" in url[:20]) or ("www" in url[:20]):
        # print(f" {url}  didn't parse! is it correct?")
        pass
    else:
        pass
    
    return url



complex_types = (list, dict)
def apply_func(yml, func, applies_to):
    if isinstance(yml, applies_to):
        return func(yml)
    if isinstance(yml, list):
        return [apply_func(x, func, applies_to) for x in yml]
    if isinstance(yml, dict):
        return {apply_func(k, func, applies_to): apply_func(v, func, applies_to) for k, v in yml.items()}
    return yml

# MAIN


for f in tqdm(yaml_files):
    print(f"processing {f}...")
    try:
        with open(f) as handle:
            yaml_content = yaml.load(handle, Loader=NoDatesSafeLoader)
    
        level, lang, name = parse_filepath(f)
        yaml_content["File name"] = name
        # link_list = "RelatedAides" if "RelatedAides" in yaml_content else "Breakdown"
        # yaml_content[link_list] = list(addlinkFilename(yaml_content[link_list], lang=lang))
        
        if "RelatedAides" in yaml_content:
            yaml_content["RelatedAides"] = list(addlinkFilename(yaml_content["RelatedAides"], lang=lang))
        if "Breakdown" in yaml_content:
            yaml_content["Breakdown"] = {subtitle: list(addlinkFilename(sublist, lang=lang))
                                         for subtitle, sublist in yaml_content["Breakdown"].items()}



        if "RelatedAides" in yaml_content:
            add_sort_order_to_item_list(yaml_content["RelatedAides"])
        if "Breakdown" in yaml_content:
            for title, ls in yaml_content["Breakdown"].items():
                add_sort_order_to_item_list(ls)


        yaml_content = apply_func(yaml_content, correct_IRI, str)
        
        
        new_name = f"{OUT_DIR}/{level}/{lang}/{name}_{lang}.json"

    
        os.makedirs(os.path.dirname(new_name), exist_ok=True)
        with open(new_name, "w") as handle:
            json.dump(yaml_content, handle, indent=4)

    
    # except yaml.scanner.ScannerError:
    #     print(f)
    #     exit(1)
    # except yaml.parser.ParserError:
    #     print(f)
    #     exit(1)
    except ValueError:
        print(f"{f}'s filename can't be parsed")
        exit(1)

exit(0)