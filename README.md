# Research Guides as Data

This is a development repository for collaboratively designing and integrating the research guides from NIOD into the Datahub. 

## Content Overview
   
 - [dev.ipynb](dev.ipynb) development code snippets that load and check YAML files, next to some pointers and notes.
 - [level2](./niveau2/): 
 - [level3](./niveau3/): 



## Background

The research guides are organised in a hierarchy:  

 1. The top level consists of general texts about writing provenance reports, the landscape of heritage institutions, etc. Du to their general nature, there are only few such documents, they contain mainly unstructured text and are thus _not_ treated as data.
 2. The second tier is made up descriptions of broad topics, major actors and concepts in the colonial context, such as the Dutch colonial army. Guides on this level will be a main point of entry into the Datahub and provide context. There will be several dozens of such guides and they are thus treated as data, an example translation into YAML can be found in [this repository](./Leger_en_Marine.yaml).
 3. Finally, on the third level, there is additional information about specific entities, actors and concepts related to and active in the colonial context. These guides are data already from their origin, as there can be arbitrarily many, and they should be treated as such, i.e. live next to/in the data in the Datahub. An example of the Kunsthandel van Lier guide translated into YAML is [here](Kunsthandel_van_Lier.yaml).


## YAML


## Linking

-
