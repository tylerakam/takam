import spacy

# nlp = spacy.cli.download("en_core_web_sm")
nlp = spacy.load('en_core_web_sm')

futurama = open('futurama2.txt', 'r', encoding='utf8')
words = futurama.read()
wordstrings = str(words)
print(wordstrings)

# count=0
# for w in words:
#     count += 1
#     print(count, ": ", w)
# I also commented this out to save from scrolling, but I ran it and saw it in use
doc = nlp(wordstrings)
for token in doc:
    print(token.text)
    print(token.text, "--->", token.pos_)
# I think this is what we were looking for with the token from the spacy tutorial.
# I'm going to try some from the class example



