# Research Aids

## Table of Contents

- [Research Aids as Data](#research-aids-as-data)
- [Content Overview](#content-overview)
- [Documentation for adding and updating research aids](#documentation-for-adding-and-updating-research-aids)

## Research Aids as Data

_This repository and the intellectual work (aka data) it contains are published under a CC-BY-SA license ([more information in the deed](./LICENSE)).  
In brief, this means that you are allowed to freely use and adapt its contents in your own work as long as you attribute the original authors appropriately and share it as part of the Creative Commons as well._  

This is a development repository for collaboratively designing and integrating the research guides from NIOD into the Datahub. The core of the approach is to treat the research _guides_ as data, which means structuring them and the texts they contain as much as possible for parsing, automatic ingestion into and linking with the Datahub and its front-end applications.

## Content Overview

**[CLICK HERE FOR A DIRECTORY TREE OF THE RESEARCH GUIDES](./directory_tree.md)**
(not updated automatically - to generate the directory tree run)
```
(echo "\`\`\`"; echo "$(tree --charset=ascii published/niveau*)"; echo "\`\`\`") > directory_tree.md
```

#### [Level 0](./published/niveau0)

[insert description level 0 / overview]

#### [Level 1](./published/niveau1)

The research guides as produced by NIOD are organised in a hierarchy of 3 levels. The top level of the hierarchy, level 1, consists of general texts about writing provenance reports, the landscape of heritage institutions and other introductory materials. Due to their general nature, there are only few such documents, they contain mainly unstructured text and are thus _not_ treated as data. This means that they are not included in the work done in this repository.


#### [Level 2](./published/niveau2)

The second tier of the hierarchy is made up of descriptions of broad topics, major actors and concepts in the colonial context, such as the Dutch colonial army. Guides on this level will be a main point of entry into the Datahub and provide context. There will be several dozens of such guides and they are thus treated as data, an example translation into YAML can be found in [Leger_en_Marine.yaml](./niveau2/Leger_en_Marine.yaml).

#### [Level 3](./published/niveau3)

Finally, on the third level, there is additional information about specific entities, actors and concepts related to and active in the colonial context. These guides are data already from their origin, as there can be arbitrarily many, and they should be treated as such, i.e. live next to/in the data in the Datahub. An example of the Kunsthandel van Lier guide translated into YAML is [Kunsthandel_van_Lier.yam;l](./niveau3Kunsthandel_van_Lier.yaml).

#### Misc Contents of this Repo

 - [scripts](./scripts/) contains development code & the scripts that process YAML written by NIOD into JSON that can be processed as LinkedData
 - test
 - test2 19:40
 - tesst3 20:23

## Documentation for adding and updating research aids

**Korte uitleg over de frontend van de website** :desktop_computer:
  - Wat kan ik vinden op de website
	 - Hoe is de content geordend/wat zijn de huidige categorieën
	 - Hoe verhoudt deze zich tot de Github? >> Wanneer vindt er een update van de landing page plaats?

**Uitleg over de backend (Github)** :floppy_disk:
  - Hoe is deze gestructureerd
  - Hoe voeg ik een zoekhulp toe
    - Wat moet er in een yaml bestand staan
    - Waar vind ik een template
    - Hoe voeg ik informatie toe
    - Hoe link ik naar websites
    - Hoe link ik naar andere zoekhulpen
    - Hoe noteer ik bronnen
    - (Hoe voeg ik een zoekhulp toe via het formulier)
  - Hoe onderhoud ik bestaande zoekhulpen
  - Wat te doen bij een foutmelding
