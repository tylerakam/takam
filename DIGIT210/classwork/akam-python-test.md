# Tyler Akam Python Test

**The Beginning:**
I started with using regex to get my document converted into readable xml that I could process later. I then worked at getting my document to resemble [Dr. B's python code](https://github.com/newtfire/textAnalysis-Hub/blob/main/Class-Examples/Python/nlp-NER/py/lotr-files-stage5.py) on the Text analysis repo, then made changes to make it fit the Dark Souls project better. One of the big differences between  all of the  other projects and  the Dark Souls project is that at the moment, we have one main file of our data to look at. I think this was a challenge to implement into the python code, but I believe I have it working.
- The import and single document codes:
```
import os
import spacy
from spacy.pipeline import EntityRuler
import re as regex
from saxonche import PySaxonProcessor
```

```
souls = open('dsexcel-text-test.xml', 'r', encoding='utf8')
readTextFiles(souls)
```
**The Code:**
The code has a few major sections. The beginning of it all consists of the NLP processor spaCy, and the entity collector. This is something we've worked with before and it makes sense to use it here before we output it through the other sections. The goal is to find all of the types of  information and have it automatically tag the information as something such as a PERSON, GPE (geo political entity), etc. After we do that, we run it through Saxonche to make it possible to use Xpath to go over the information and use the xmlTagger. After this, we use the xmltagger to make the information visible as xml tags. Then we finally process it all to an output file that we can view. The goal is to generate new tags over our xml file to include the information from the spaCy tagging. The code for some of this follows:
- The spaCy and entity collector code:
Note that some comments are visible, and for the code to work, they don't **need** to be visible. This simply tracks our source file and then prepares them in a dictionary for spaCy to process so that we can later send it to the PySaxon processor and the xml Autotagger.

This is what accesses my file and begins the spaCy process. Mine looks different because I had to adapt this and make it select on just one file instead of a collection like the rest of the project groups. This makes it both harder and easier, as I only have to make sure I am focusing on the current working directory, but it means that I had a few issues converting the code that Dr. B left for me. 
```nlp = spacy.load('en_core_web_lg')
souls = 'dsexcel-text-test.xml'
def readTextFiles(filepath):
    readFile = filepath.read()
    # print(readFile)
    stringFile = str(readFile)
    # lengthFile = len(readFile)
    # print(lengthFile)
    tokens = nlp(stringFile)
    # print(tokens)
    listEntities = entitycollector(tokens)
    print(listEntities)
def entitycollector(tokens):
    entities = []
    for entity in tokens.ents:
        # if entity.label_ == "CARDINAL":
        print(entity.text, entity.label_, spacy.explain(entity.label_))
        # Attribute error 'dict' object has no attribute 'append'

        entities.append(entity.text)
    return entities
```
This is the NER entity Ruler. This is to fix some issues spaCy may be having.
```
config = {"spans_key": None, "annotate_ents": True, "overwrite": True, "validate": True}
ruler = nlp.add_pipe("span_ruler", before="ner", config=config)
```
- The Saxonche code:
Here, the PySaxon process begins. We're using the PySaxon processor, which allows us to match on our dict and use xPath to get the exact pieces we want. This is one of the last steps in our process where we create tags for the system. The section after this helps finalize and prepare this for the actual tagging. Inside here, we select our file that we want to process, defined as `souls` and then send it through PySaxon and use xPath to match on the `<desc>` element in the xml code.
```
def readTextFiles(souls):
    # with open(souls, 'r', encoding='utf8') as f:
    with PySaxonProcessor(license=False) as proc:
        xml = open(souls, encoding='utf-8').read()
        xp = proc.new_xpath_processor()
        node = proc.parse_xml(xml_text=xml)
        xp.set_context(xdm_item=node)
        xpath = xp.evaluate('//desc ! normalize-space() => string-join()')
        string = str(xpath)
        print(string)
        tokens = nlp(string)
        dictEntities = entitycollector(tokens)
        print(f"{dictEntities=}")

        return (dictEntities)
```
This makes the spaCy identifiers that we use when tagging them. By classifying things like "LOC" or "PERSON" in the for loop, we can tell the function to include these in the markup process. Because it is a for loop, this operates over every instance of a tag to give them the proper attribute according to how spaCy defines a word or string.
```
def entitycollector(tokens):
    print("entityCollector is running")
    entities = {}
    for ent in sorted(tokens.ents):
        if ent.label_ == "LOC" or ent.label_=="FAC" or ent.label_=="ORG" or ent.label_=="GPE" or ent.label_=="NORP" or ent.label_=="PERSON":
            if not regex.match(r"\w*[.,!?;:']\w*", ent.text):
                entities[ent.text] = ent.label_
    print(f"{entities=}")
    return entities
```
- The output file code:
The following is simply just the code that outputs my code into an xml file that I can review. It points to a specific file that it writes to using information from up above in the document. We then prepare to autotag by calling it in the output...
```
def assembleAllNames(souls):
    soulsFileDict = readTextFiles(souls)
    print(f"{soulsFileDict=}")

    AllNamesKeys = list(soulsFileDict.keys())
    AllNamesKeys.sort()
    SortedDict = {i: soulsFileDict[i] for i in AllNamesKeys}
    print(f"{SortedDict=}")
    writeSortedEntries(SortedDict)
    soulsFileData = xmlTagger(souls, SortedDict)
    return soulsFileData
def writeSortedEntries(dictionary):
    print("writeSortedEntries is firing!")
    with open('distTrained-ORG-LOC-GPE-NORP.txt', 'w') as f:
        for key, value in dictionary.items():
            f.write(key + ' : ' + value + '\n')
```
- The xmlTagger code:
In here we use the autoTagger. We look at the information from spaCy and make it read it and then apply the new changes from the autoTagger (with help from PySaxon for the xPath parts) and make sure that it gets sent to the output file. (Don't mind the print lines that mention things firing. those are simply there for testing purposes. I kept them in for documentation purposes.) The final section looks at the string file and look for matches.
```
def xmlTagger(sourcePath, SortedDict):
    with open(sourcePath, 'r', encoding='utf8') as f:
        readFile = f.read()
        stringFile = str(readFile)
        print("XML TAGGER IS FIRING! ")
        # filename = os.path.basename(f.name)
        # print(f"{filename=}")
        targetFile = 'dsTestOutput.xml'
        print(f"{targetFile=}")
        
                for key, val in SortedDict.items():
            replacement = '<name type="' + val + '">' + key + '</name>'
            # print(f"{replacement=}")
            stringFile = stringFile.replace(key, replacement)
            print(f"{stringFile=}")

        with open(targetFile, 'w') as f:
            f.write(stringFile)


assembleAllNames(souls)
```

That should be everything that makes my code function. By sending it step through step to different functions, it becomes more readable and understandable. A quick recap would include the following:

- use the xml file as a start and then bring in import lines for everything that's needed.
- point to the xml and process it with spaCy to get a generated dictionary
- send it to PySaxon to use xPath so we can use autoTagger
- make a destination for output, auto tag it and make sure that it gets sent to the output file


[![](https://mermaid.ink/img/pako:eNpVkkFP5DAMhf-KldMiDeI-h5VgBjitFgkkDlMOpnXbaNMkShxmqun893WSsgs9NY773vdcn1XrOlJb1Rt3bEcMDC_7xoI8twcfyGMgeMdIcJoM9NrQG1xf_1z05J30assO_Myjswvc_Vir0eNu3sDT_IwnZzcQaLg_AdoOHI8UoOoia2fjVTW7y6qwO78GzQR9sm25hd4FIGxHiFQql9q-KxDF54Ysa56hdcZIjwsL7A9JgKO_bWfIfGsMhE4XEQwzuB7EaYrAIzJgYjcJUIvGzIDMQb8nAWkNxqh7qVccUZME09tXijXmAvfFdj3m1nw8PSGP-RAp4-XPZWoSayqS0Ac31YGVAeVr4f3QLsUycsYhfg2RByK1QdvhG4X0vkiZJP5D4fg0qg4r1U11Er2cWHT-Z43F_5uNKLjEPnH98dXuofyp5Xe5WODxcAzogT4oyBoIFSRflCKtcSwdV5koQOu2FAT7Kf9vt9RGTSSj0Z2s5DkbNioPnBq1ldcOw59GNfYifTnA82xbteWQaKOS75Bpr3EIOKltjyZKlTotK_Gr7nhZ9ctfHL4K6g?type=png)](https://mermaid.live/edit#pako:eNpVkkFP5DAMhf-KldMiDeI-h5VgBjitFgkkDlMOpnXbaNMkShxmqun893WSsgs9NY773vdcn1XrOlJb1Rt3bEcMDC_7xoI8twcfyGMgeMdIcJoM9NrQG1xf_1z05J30assO_Myjswvc_Vir0eNu3sDT_IwnZzcQaLg_AdoOHI8UoOoia2fjVTW7y6qwO78GzQR9sm25hd4FIGxHiFQql9q-KxDF54Ysa56hdcZIjwsL7A9JgKO_bWfIfGsMhE4XEQwzuB7EaYrAIzJgYjcJUIvGzIDMQb8nAWkNxqh7qVccUZME09tXijXmAvfFdj3m1nw8PSGP-RAp4-XPZWoSayqS0Ac31YGVAeVr4f3QLsUycsYhfg2RByK1QdvhG4X0vkiZJP5D4fg0qg4r1U11Er2cWHT-Z43F_5uNKLjEPnH98dXuofyp5Xe5WODxcAzogT4oyBoIFSRflCKtcSwdV5koQOu2FAT7Kf9vt9RGTSSj0Z2s5DkbNioPnBq1ldcOw59GNfYifTnA82xbteWQaKOS75Bpr3EIOKltjyZKlTotK_Gr7nhZ9ctfHL4K6g)