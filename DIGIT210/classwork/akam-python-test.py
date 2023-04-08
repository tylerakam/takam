# STAGE 5: LET'S CLEAN THIS UP: DEALING WITH MESSY NLP TAGGING
# We will try adding an EntityRuler to guide spaCy.
# pip install saxonche
# The library above lets you read and pull data with XPath
import os
import spacy
from spacy.pipeline import EntityRuler
import re as regex
from saxonche import PySaxonProcessor
# ebb: The line above imports the PySaxonProcessor from SaxonCHE (free "home edition")
# for work with XPath


# nlp = spacy.cli.download("en_core_web_lg")
nlp = spacy.load('en_core_web_lg')

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
    # print(entities)

# ebb: After reading the sorted dictionary output, we know spaCy is making some mistakes.
# So, here let's try adding an EntityRuler to customize spaCy's classification. We need
# to configure this BEFORE we send the tokens off to nlp() for processing.
##########################################################################################
# Create the EntityRuler and set it so the ner comes after, so OUR rules take precedence
# Sources:
#   W. J. B. Mattingly: https://ner.pythonhumanities.com/02_01_spaCy_Entity_Ruler.html
#   spaCy documentation on NER Entity Ruler: https://spacy.io/usage/rule-based-matching#entityruler

config = {"spans_key": None, "annotate_ents": True, "overwrite": True, "validate": True}
ruler = nlp.add_pipe("span_ruler", before="ner", config=config)
def readTextFiles(souls):
    # with open(souls, 'r', encoding='utf8') as f:
    with PySaxonProcessor(license=False) as proc:
        xml = open(souls, encoding='utf-8').read()
        # ebb: Here we changed to the Saxon processor to read files with XPath.
        # From here on, we change how we formulate the string that Python will send to NLP.
        xp = proc.new_xpath_processor()
        node = proc.parse_xml(xml_text=xml)
        xp.set_context(xdm_item=node)
        xpath = xp.evaluate('//desc ! normalize-space() => string-join()')
        # ebb: Let's get the string() value of all the <p> elements that are descendants of <book>.
        # The XPath function normalize-space() gets the string value and removes extra spaces.
        # That way we avoid the prologue, preface material.
        # I'm sending the whole thing to string-join() to bundle it together as one string
        # instead of a new string for every <p> element.
        # string = xpath.__str__()
        # TSA: I'm gonna try my itemTypes
        string = str(xpath)
        print(string)
        # ebb: Doing some regex replacements to clean up punctuation issues that are getting in the way of the NER tagger
        # cleanedUp = regex.sub("_", " ", string)
        # cleanedUp = regex.sub(r"'([A-Z])]", r" \1", cleanedUp)
        # cleanedUp = regex.sub(r"([.!?;'`])([A-Z'`]])", r"\1 \2", cleanedUp)
        # # send to spaCy to collect nlp data on the big string
        tokens = nlp(string)
        # tokens = nlp.pipe(cleanedUp, disable=["tagger", "parser", "attribute_ruler", "lemmatizer"])
# TSA: I don't think I need this unless I have issues with punctuation.
        dictEntities = entitycollector(tokens)
        # ebb: The line above sends our nlp tokens to the named entity collector function.
        # THIS current function will receive and print a simple form of their output in the next line.
        print(f"{dictEntities=}")

        return (dictEntities)
# 4. ebb: The function below returns a simple list of named entities.
# But on the way, we're printing out as much we can from spaCy's classification of named entities:
def entitycollector(tokens):
    print("entityCollector is running")
    entities = {}
    for ent in sorted(tokens.ents):
        if ent.label_ == "LOC" or ent.label_=="FAC" or ent.label_=="ORG" or ent.label_=="GPE" or ent.label_=="NORP" or ent.label_=="PERSON":
            if not regex.match(r"\w*[.,!?;:']\w*", ent.text):
        # ebb: The line helps experiment with different spaCy named entity classifiers, in combination if you like:
        # When using it, remember to indent the next lines for the for loop.
            # stringify = (ent.text + ': ' + ent.label_ + ': ' + spacy.explain(ent.label_) + '\n')
            # stringify is a string-formatted version of this designed to provide an easily readable file output.
            # print(f"{stringify=}")
                entities[ent.text] = ent.label_
    print(f"{entities=}")
    return entities
    # ebb: Keep the return line in position at same indentation level as the definition of the entities variable.
# 2. and 5. ebb: The for loop below is working with your CollPath, and going through each file inside,
# and sending it up to readTextFiles, where the nlp processing will happen.
def assembleAllNames(souls):
    soulsFileDict = readTextFiles(souls)
    print(f"{soulsFileDict=}")

    AllNamesKeys = list(soulsFileDict.keys())
    AllNamesKeys.sort()
    SortedDict = {i: soulsFileDict[i] for i in AllNamesKeys}
    print(f"{SortedDict=}")
    writeSortedEntries(SortedDict)
    # ebb: The function call in the above line will print the file to a useful output for review.
    # In a previous version of this file, we were printing the entire dictionary out to a file, and it was printing all the entries
    # out in one extremely long line. So I defined a simple function that will
    # output each entry as a string, line-by-line in the output file so the entries are easy
    # to read and review. We keep the dictionary as key-value pairs to send on to the xmlTagger function.


    soulsFileData = xmlTagger(souls, SortedDict)
            # ebb: In the lines above, we send to the xmlTagger to add the nlp info as XML elements and attributes to the source files.
    return soulsFileData
    # Python functions don't really need to have return lines, but we can set the return to the function's most important output.

def writeSortedEntries(dictionary):
    print("writeSortedEntries is firing!")
    with open('distTrained-ORG-LOC-GPE-NORP.txt', 'w') as f:
        for key, value in dictionary.items():
            f.write(key + ' : ' + value + '\n')
def xmlTagger(sourcePath, SortedDict):
    with open(sourcePath, 'r', encoding='utf8') as f:
        readFile = f.read()
        stringFile = str(readFile)
        print("XML TAGGER IS FIRING! ")

        # ebb: Get the current filename. We need to know it to write its new output version
        # filename = os.path.basename(f.name)
        # print(f"{filename=}")
        targetFile = 'dsTestOutput.xml'
        print(f"{targetFile=}")


        # ebb: Work with stringFile variable to look for matches from the distinctNames set.
        for key, val in SortedDict.items():
            replacement = '<name type="' + val + '">' + key + '</name>'
            # print(f"{replacement=}")
            stringFile = stringFile.replace(key, replacement)
            print(f"{stringFile=}")

        # ebb: Output goes in the taggedOutput directory: ../taggedOutput
        with open(targetFile, 'w') as f:
            f.write(stringFile)


assembleAllNames(souls)

    # ebb: The functions are all initiated here now.
    # This just delivers the collection path up to the first function in the sequence.