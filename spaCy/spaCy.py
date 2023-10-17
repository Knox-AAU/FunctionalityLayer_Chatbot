import spacy
nlp = spacy.load('da_core_news_md')

def extract_entities(input_string):
    doc = nlp(input_string)
    entities = [ent.text for ent in doc.ents]
    return entities

def runSpaCy(str):
    key_entities = extract_entities(str)
    return key_entities
