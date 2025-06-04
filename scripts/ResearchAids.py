from datetime import datetime

class EditEvent:
    @classmethod
    def from_yaml(cls, yml):
        appl = yml.get("applies_to", None) 
        notes = yml.get("notes", None)
        return cls(yml["Date"],
                   yml["Author"],
                   yml["Role"],
                   appl, notes)
        
    def __init__(self, date, author, role, applies_to=None, notes=None):
        self.date = date # YAML parses dates automagically: datetime.strptime(date, "%Y-%m-%d")
        self.author = author
        self.role = role
        self.is_origin = ("original author" in self.role.lower())
        
        self.applies_to = applies_to
        self.notes = notes

    def __str__(self):
        return str(self.__dict__)
        
    def to_markdown(self, markdown=""):
        return markdown + f"""edited by {self.author} as {self.role} on {self.date.strftime("%Y-%m-%d")}
        {f'(applies to section: {self.notes})' if self.notes else ''}
        {f'(notes: {self.notes})' if self.notes else ''}""".strip()

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

class EditHistory(tuple):
    @classmethod
    def from_yaml(cls, yml):
        return cls(map(EditEvent.from_yaml, yml))
    
    def __new__(cls, events):
        sorted_events = sorted(events, key=lambda e: e.date)
        self = super().__new__(cls, sorted_events)
        self.origin_event = self.origin_event()
        # self.first_event = self.origin_event if self.origin_event else self[0]
        self.last_event = self[-1] if len(self) > 1 else None
        return self        
        
    def to_markdown(self, markdown=""):
        return markdown + "\n  - ".join(e.to_markdown() for e in self)

    def origin_event(self):
        orig_events = tuple(e for e in self if e.is_origin)
        return orig_events[0] if orig_events else None

class ResearchAid:
    @staticmethod
    def get_level(level_id):
        return [Level0, Level1, Level2, Level3][level_id]

    def __init__(self, yml, raise_parsing_error=False):
        self.level_id = int(yml["Level"])
        self.title = yml["Title"]

        self.edit_history = EditHistory.from_yaml(yml["Editing-history"])

        self.author = "Wiebe Reints (@wreints)"
        self.time = datetime.today().strftime("%Y-%m-%d")
        try:
            self.level = self.get_level(self.level_id)(yml)
            self._parsed = True
        except Exception as e:
            self._parsed = False
            self._error_msg = e
            if raise_parsing_error:
                raise e

    def __call__(self):
        if not self._parsed:
            return None

        #_author: {self.author}_  
        # _last edited: {self.time}_  
        return f"""_This is a level {self.level_id} Research Aid_
        _first {self.edit_history.origin_event.to_markdown()}_
        {'_last {self.edit_history.last_event.to_markdown()}_' if self.edit_history.last_event else ''}


# {self.title}

{self.level()}
        """

    
    def get_markdown_content(self, yml):
        if not (yml["content-type"] == 'text/markdown'):
            raise ValueError(f"only Markdown can be interpreted as markdown! got {yml}")
        return yml["content"]

    def parse_edit_history(self, yml):
        
    - Date: #mandatory
      Applies_to: #optional
      Author: #mandatory
      Role: #mandatory
      Editing_notes: #optional


    
    def parse_related_dict(self, yml):
        # key = next(yml.keys())
        # value_dict = next(yml.values())
        item_title, item_value_dict = tuple(yml.items())[0]
        rel_type = item_value_dict["rel_type"]
        if rel_type.lower()  == "see also":
            raise Exception("this Markdown doesn't get displayed right!")
            return f"_see also: [{item_title}]({item_value_dict["link"]})_  \n"
        elif rel_type == "broader":
            return f"_broader: [{item_title}]({item_value_dict["link"]})_  \n"
        elif rel_type == "narrower":
            return f"_narrower: [{item_title}]({item_value_dict["link"]})_  \n"
        else:
            print(rel_type.lower())
            raise ValueError(f"{item_value_dict}")

    
    def parse_anything(self, yml, result_md="", level=0):
        if isinstance(yml, (str, int, float, bool)):
            return result_md + yml
        elif isinstance(yml, list):
            ls_md = ", ".join(self.parse_anything(x) for x in yml)
            return result_md + "\n" + ls_md + "\n"
        elif isinstance(yml, dict):
            dict_md = ",\n  ".join(self.parse_anything(v, 
                                                    result_md=self.parse_anything(k, result_md="")+":\n  "
                                                   ) for k, v in yml.items())
            return result_md + dict_md
    


class Level0(ResearchAid):
    def __init__(self, yml):
        self.sub = yml["Subtitle"]
        self.main_text = self.get_markdown_content(yml["Content"])
        self.breakdown = yml["Breakdown"]


    def parse_topic(self, yml):
        # print( "---", yml, "---")
        if isinstance(yml, list): return ""
        # item_title, item_fields = tuple(yml.items())[0]
        # if item_fields["rel_type"] == "see also":
        #     md = f"""_see also {item_title} ({item_fields["link"]})_
        #     """
        # else:
        #     raise ValueError(f"{item_fields}")
        md = self.parse_related_dict(yml)

        subtopics = item_fields.get("Subtopics", None)
        if subtopics:
            md +=self.parse_topic(subtopics)
        return md
    
        
    def parse_breakdown(self, yml):
        for title, ls in yml.items():
            md = f"""### {title}
            """
            for d in ls:
                md += self.parse_topic(d)
            yield md
                
    
    def __call__(self):
        breakdown = "\n".join(self.parse_breakdown(self.breakdown))
        return f"""
        ## {self.sub}

        {self.main_text}

        {breakdown}
        """
    
class Level1(ResearchAid):
    def __init__(self, yml):
        self.abstract = yml["Abstract"]
        self.main_text = self.get_markdown_content(yml["Main-text"])
        self.related_aids = self.parse_related_aids(yml["RelatedAides"])

    def parse_related_aids(self, yml):
        md = ""
        for d in yml:
            md += self.parse_related_dict(d)
        return md

    def __call__(self):
        return f"""
## Abstract

{self.abstract}

{self.main_text}

## Related Aids

{self.related_aids}
"""
    
class Level2(Level1):
    def __init__(self, yml):
        self.abstract = yml["Abstract"]
        self.main_text = self.get_markdown_content(yml["Main-text"])
        self.related_aids = self.parse_related_aids(yml["RelatedAides"])
        self.relevant_data = self.parse_anything(yml["Relevant data"])
        self.sources = self.parse_sources(yml["Sources"])

    def parse_source_links(self, yml):
        for d in yml:
            for k, v in d.items():
                if k == "ISBN":
                    yield f"[ISBN {v}](https://isbnsearch.org/isbn/{v})"
                elif k == "ISSN":
                    yield f"[ISBN {v}](https://portal.issn.org/resource/ISSN/{v})"
                elif k == "OCLC":
                    yield f"[WorldCat {v}](https://search.worldcat.org/title/{v})"
                elif k == 'Google Books ID':
                    yield f"[Google Books ID {v}](https://books.google.nl/books?id={v})"
                elif k == "DOI":
                    yield f"DOI: {v}"
                elif k == "URL":
                    yield f"[{v}]({v})"
                else:
                    raise ValueError(f"link dict {d} unknown")
            
    
    def parse_sources(self, yml):
        md = ""
        for source_lvl, source_ls in yml.items():
            md += f"## {source_lvl}\n\n"
            for source in source_ls:
                'Type of source', 'Name', 'Link', 'Description and remarks'
                source_md = f"**{source['Type of source']}**: {source['Name']}"
                # links_md = ", ".join([f"{v} (_{k}_)" for d in source['Link'] for k, v in d.items()])
                links_md = ", ".join(self.parse_source_links(source['Link']))
                # links_md = "(" + links_md + ")"
                md += f"{source_md}  \n{links_md}  \n"
                if"Description and remarks" in source:
                    md+= f"_{source["Description and remarks"]}_  \n\n"
        return md
                
    def __call__(self):
        md = super().__call__()
        return md+f"""{self.sources}

---
## Relevant Data 
{self.relevant_data}"""
            

class Level3(Level2):
    """
    Level 3 and Level 2 have the same keys.
    """
    def __init__(self, yml):
        super().__init__(yml)
        # self.abstract = yml["Abstract"]
        # self.main_text = self.get_markdown_content(yml["Main-text"])
        # self.related_aids = self.parse_related_aids(yml["RelatedAides"])