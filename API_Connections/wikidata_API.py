# Goal of this file, is to call the wikidata API, which returns a set of partial triples, which define the subject, object and predicate of the entities in a user prompt

from flask import Flask, request, jsonify
from SPARQLWrapper import SPARQLWrapper, JSON
from requests import get
import logging

wikidata_endpoint = Flask(__name__)
logging.basicConfig(level=logging.INFO)

WIKISITE = "enwiki"


# Get wikidata Q-number for all entities.
def get_wikidata_id(wikipage):
    wikidata_ids = get('https://www.wikidata.org/w/api.php', {
        'action': 'wbgetentities',
        'titles': wikipage,
        'sites': WIKISITE,
        'props': '',
        'format': 'json'
    }).json()
    logging.info(wikidata_ids)
    logging.info(list(wikidata_ids['entities'])[0])

    return list(wikidata_ids['entities'])[0]


def format_triple_object(triples):
    # Check if the expected structure is present in the JSON
    if "triples" not in triples or "bindings" not in triples["triples"]:
        raise ValueError("Invalid JSON format. Expected 'triples' with 'bindings'")

    for triple in triples["triples"]["bindings"]:
        # Assuming subject, predicate, and object are always present in each triple
        if "subject" not in triple or "predicate" not in triple or "object" not in triple:
            raise ValueError("Invalid JSON format. Expected 'subject', 'predicate', and 'object' in each binding")

    json_triples = []

    for triple in triples["triples"]["bindings"]:
        formatted_triple = {
            "s": {
                "Type": type(triple["subject"]["value"]).__name__,
                "Value": triple["subject"]["value"]
            },
            "p": {
                "Type": type(triple["subject"]["value"]).__name__,
                "Value": triple["predicate"]["value"]
            },
            "o": {
                "Type": type(triple["subject"]["value"]).__name__,
                "Value": triple["object"]["value"]
            }
        }
        json_triples.append(formatted_triple)

    return json_triples


def get_triples_from_wikidata(query):
    # Set up the SPARQL endpoint URL
    wikidata_sparql_endpoint = SPARQLWrapper("https://query.wikidata.org/wikidata_sparql_endpoint")

    # Set the query string and return format
    wikidata_sparql_endpoint.setQuery(query)
    wikidata_sparql_endpoint.setReturnFormat(JSON)

    # Execute the query and get the triples
    try:
        triples = wikidata_sparql_endpoint.query().convert()
    except Exception as error:
        raise Exception("Bad Query")

    logging.info(triples)
    logging.info(triples["head"]["vars"])

    # check if the triples contain subject, object and predicate keywords
    if ("subject" not in triples["head"]["vars"] or
            "predicate" not in triples["head"]["vars"] or
            "object" not in triples["head"]["vars"]):
        logging.info("triple did not contain either subject, object or predicate")
        raise Exception("triple did not contain either subject, object or predicate")

    # check if the triples contain atleast one subject, object and predicate
    if ("bindings" not in triples["triples"] or
            not triples["triples"]["bindings"][0].get("subject") or
            not triples["triples"]["bindings"][0].get("predicate") or
            not triples["triples"]["bindings"][0].get("object")):
        logging.info("triple needs to contain atleast one element")
        raise Exception("triple needs to contain atleast one element")

    # Construct the desired JSON structure
    formatted_triples = format_triple_object(triples)

    # return json object
    return formatted_triples


@wikidata_endpoint.route('/get_triples', methods=['POST'])
def get_triples():
    logging.info("get_triples was called")
    keywords = request.json['keywords']
    logging.info(request.json)
    logging.info(keywords)
    triples = []

    # Checks if the keyword given is of type string, instead of array, and add the string to the array
    if (isinstance(keywords, str)):
        keywords = [keywords]

    for entity in keywords:
        identifier_value = get_wikidata_id(entity) #get wikidata ID (needed for querying that speicifc keyword)
        if identifier_value == "-1":
            # add fejlmeddelse til flask..
            continue

        s_value = "wd:" + identifier_value
        # Set the query string
        query = f"""
                SELECT DISTINCT ?subject ?predicate ?object
                WHERE {{
                 VALUES (?s) {{({s_value})}}
                 ?s ?wdt ?o .
                 ?p wikibase:directClaim ?wdt .
                 ?p rdfs:label ?pLabel .
                 ?s rdfs:label ?sLabel .
                 ?o rdfs:label ?oLabel .
                 FILTER (lang(?sLabel) = "en")
                 FILTER (lang(?oLabel) = "en")
                 FILTER (lang(?pLabel) = "en")
                 BIND (?oLabel AS ?object)
                 BIND (?pLabel AS ?predicate)
                 BIND (?sLabel AS ?subject)
                 }} 
                ORDER BY xsd:integer(STRAFTER(STR(?wd), "http://www.wikidata.org/entity/P"))
                LIMIT 5
                """
        logging.info(query)
        triple = get_triples_from_wikidata(query)

        logging.info(triple)
        triples.extend(triple)

    merged_triples = {
        "triples": triples
    }
    return jsonify(merged_triples)


if __name__ == '__main__':
    wikidata_endpoint.run(host='0.0.0.0', port=5002)
