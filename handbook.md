# Little Handbook for Writing Research Guides
# in YAML & Markdown



## YAML vs Markdown

YAML (recursive acronym for "YAML Ain't Markup Language") is a data serialisation language, similar in its purpose to JSON, XML and other to structure data in machine-readable formats but intended to be more human-readable at the same time. It has _basic_ data types like strings and numbers and _container_ or _complex_ types like list and dictionaries. The latter can contain values of basic types or values of complex types to recursively build complex data structures, so it is valid in YAML to construct a dictionary that contains a list whose items are in turn dictionaries and so on. This [YAML Cheatsheet](https://quickref.me/yaml.html) lists out the various valid data constructs with examples (there are many other, more extensive, guides on YAML). 

Markdown, on the other hand, is a markup (sic!) language that contains constructs to enrich (i.e. "mark up") text with formatting information such as headings, italics, bulleted lists and links. It does so by defining characters that have special meanings and that a _parser_ (a program that reads a Markdown, yaml or other file and interprets it) uses to visually compose the document (e.g. by using different glyphs for headings and italicised text) and to extract and enrich it with information _about_ the document with information _from_ the document (e.g. by collecting all links or pre-filling references with defined values). Here is a [Markdown cheatsheet](LINK) which lists and describes the various special characters and valid syntactic constructions in Markdown. This document itself is in fact written in Markdown.

## YAML together with Markdown 

With YAML and Markdown as the data structuring and markup languages, respectively, we use them together as follows: All data in the Research Guides stays YAML data, since YAML is the primary structuring language. That is, all complex types such as lists and dictionaries naturally stay as they are specified by YAML, as do basic types such as numbers and booleans. Even strings all stay YAML strings but we distinguish between "simple" (or "plain") strings and Markdown strings. We indicate the latter by making the string variable a dictionary (which is a complex data type) and adding a content type (mimicking the HTTP protocol). So the plain YAML string
```
my-string: "hello world"
```
-- which is a variable with name `my-string` and value `"hello world"`-- can be turned into a Markdown string by writing the following YAML code
```
my-string:
  value: "hello **world**"
  content-type: "text/markdown"
```

(Notice the `**` around `world`, which is Markdown syntax for **boldfaced** text.)


## Links

A key aspect of the Research Guides is linking to other sources and data- & knowledge bases as well as within the Datahub and within themselves. The networks of knowledge that emerge through all of these links together has an important function in contextualising the Datahub. 

Links in the RGs come in the form of [URIs](https://en.wikipedia.org/entity/Uniform_Resource_Identifier), such as the more specific URLs or the more general IRIs. In any YAML file, any link is inside of a string (including when the string contains only the link).  




