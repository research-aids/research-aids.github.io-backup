# Research Guides as Data

This is a development repository for collaboratively designing and integrating the research guides from NIOD into the Datahub. The core of the approach is to treat the research _guides_ as data, which means structuring them and the texts they contain as much as possible for parsing, automatic ingestion into and linking with the Datahub and its front-end applications.

## Content Overview

## [CLICK HERE FOR A DIRECTORY TREE OF THE RESEARCH GUIDES](./directory_tree.md)
(not updated automatically -- to generate the directory tree run
```
(echo "\`\`\`"; echo "$(tree --charset=ascii niveau*)"; echo "\`\`\`") > directory_tree.md
```
)


The research guides as produced by NIOD are organised in a hierarchy of 3 levels. The top level of the hierarchy, level 1, consists of general texts about writing provenance reports, the landscape of heritage institutions and other introductory materials. Due to their general nature, there are only few such documents, they contain mainly unstructured text and are thus _not_ treated as data. This means that they are not included in the work done in this repository.


#### [Level 2](./niveau2/)

The second tier of the hierarchy is made up of descriptions of broad topics, major actors and concepts in the colonial context, such as the Dutch colonial army. Guides on this level will be a main point of entry into the Datahub and provide context. There will be several dozens of such guides and they are thus treated as data, an example translation into YAML can be found in [Leger_en_Marine.yaml](./niveau2/Leger_en_Marine.yaml).

#### [Level 3](./niveau3/)

Finally, on the third level, there is additional information about specific entities, actors and concepts related to and active in the colonial context. These guides are data already from their origin, as there can be arbitrarily many, and they should be treated as such, i.e. live next to/in the data in the Datahub. An example of the Kunsthandel van Lier guide translated into YAML is [Kunsthandel_van_Lier.yam;l](./niveau3Kunsthandel_van_Lier.yaml).



#### Misc Contents of this Repo

 - [scripts](./scripts/) contains development code & the scripts that process YAML written by NIOD into JSON that can be processed as LinkedData
   -  

## Documentation

_YAML_ (short for _YAML Ain't Markup Language_) is a human-readable data format that defines basic data types and containers and allows to construct more complex data constructions with those. _Markdown_ is a markup \[sic!\] language


## Open Questions & TODOs

 - example SPARQL queries would be nice
   -> showcase to users how to search the Datahub (e.g. for the entity described in the given guide) 
   -> makes nice use of the equivalence between URIs as identifiers of individual items and queries as identifiers of sets of items



## YAML


## Linking

-
