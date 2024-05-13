
# Little Handbook for Writing YAML & Markdown Research Guides


## YAML vs Markdown

YAML (recursive acronym for "YAML Ain't Markup Language) is a data serialisation language, similar in its purpose to JSON, XML and other to structure data in machine-readable formats but intended to be more human-readable at the same time. Its basic data types like strings and numbers and container types like list and dictionaries 

Markdown, on the other hand, is a markup (sic!) language that contains constructs to enrich (i.e. "mark up") text with formatting information such as headings, italics, bulleted lists and links. It does so by defining characters that have special meanings and that a _parser_ (a program that reads a Markdown, yaml or other file and interprets it) uses to visually compose the document (e.g. by using different glyphs for headings and italicised text) and to extract and enrich it with information _about_ the document with information _from_ the document (e.g. by collecting all links or pre-filling references with defined values). Here is a [Markdown cheatsheet](LINK) which lists and describes the various special characters and valid syntactic constructions in Markdown. This document itself is in fact written in Markdown.

## YAML together with Markdown 

With YAML and Markdown as the data structuring and markup languages of our choice, we use them together as follows: All data in the Research Guides stays YAML data, since YAML is the primary structuring language. That is, all complex types such as lists and dictionaries naturally stay as they are specified by YAML, as do basic types such as numbers and booleans. Even strings all stay YAML strings but we distinguish between "simple" (or "plain") strings and markdown strings. We indicate this by making the string variable a dictionary (which is a complex data type) and adding a content type (mimicking the HTTP protocol). So the plain YAML string
```
my-string: "hello world"
```
-- which is a variable with name `my-string` and value `"hello world"`-- can be turned into a Markdown string by writing the following YAML code
```
my-string:
  value: "hello **world**"
  content-type: "text/markdown"
```



