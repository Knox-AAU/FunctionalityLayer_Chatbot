# Goal of this file, is to call the wikidata API, which returns a set of partial triples, which define the subject, object and predicate of the entities in a user prompt

from flask import Flask, request, jsonify
from SPARQLWrapper import SPARQLWrapper, JSON
import jsonschema
from jsonschema import validate
from requests import get
import logging

wikidataEndpoint = Flask(__name__)
logging.basicConfig(level=logging.INFO)

#keywords = ["Aalborg", "Berlin"]

WIKISITE = "enwiki"

# Get wikidata Q-number for all entities.
def get_qnumber(wikipage):
    resp = get('https://www.wikidata.org/w/api.php', {
                'action': 'wbgetentities',
                'titles': wikipage,
                'sites': WIKISITE,
                'props': '',
                'format': 'json'
                           }).json()
    logging.info(resp)
    logging.info(list(resp['entities'])[0])

    return list(resp['entities'])[0]

def formatTripleObject(results):

        # Check if the expected structure is present in the JSON
    if "results" not in results or "bindings" not in results["results"]:
        raise ValueError("Invalid JSON format. Expected 'results' with 'bindings'")

    for result in results["results"]["bindings"]:
        # Assuming subject, predicate, and object are always present in each result
        if "subject" not in result or "predicate" not in result or "object" not in result:
            raise ValueError("Invalid JSON format. Expected 'subject', 'predicate', and 'object' in each binding")
        
    json_results = []

    for result in results["results"]["bindings"]:
        triple = {
            "s": {
                    "Type": type(result["subject"]["value"]).__name__,
                    "Value": result["subject"]["value"]
                 },
            "p": {
                    "Type": type(result["subject"]["value"]).__name__,
                    "Value": result["predicate"]["value"]
                 },
            "o": {
                    "Type": type(result["subject"]["value"]).__name__,
                    "Value": result["object"]["value"]
                }
        }
        json_results.append(triple)
    return json_results

def call_wikidata_API(query):
    # Set up the SPARQL endpoint URL
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

    # Set the query string and return format
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    # Execute the query and get the results
    try:
        results = sparql.query().convert()
    except Exception as error:
        raise Exception("Bad Query")

    logging.info(results)
    logging.info(results["head"]["vars"])

    #check if the results contain subject, object and predicate keywords
    if ("subject" not in results["head"]["vars"] or 
       "predicate" not in results["head"]["vars"] or 
       "object" not in results["head"]["vars"]):
        logging.info("result did not contain either subject, object or predicate")
        raise Exception("result did not contain either subject, object or predicate")

    if ("bindings" not in results["results"] or
        not results["results"]["bindings"][0].get("subject") or
        not results["results"]["bindings"][0].get("predicate") or
        not results["results"]["bindings"][0].get("object")):
        logging.info("result needs to contain atleast one element")
        raise Exception("result needs to contain atleast one element")

    # Construct the desired JSON structure
    formattedTriples = formatTripleObject(results)

    # return json object
    return formattedTriples

@wikidataEndpoint.route('/GetTriples', methods=['POST'])
def GetTriples():
    logging.info("GetTriples was called")
    keywords = request.json['keywords']
    logging.info(request.json)
    logging.info(keywords)
    triples = []

    #Checks if the keyword given is of type string, instead of array, and add the string to the array
    if (isinstance(keywords, str)):
        keywords = [keywords]

    for entity in keywords:
        identifier_value = get_qnumber(entity)
        if identifier_value == "-1":
            #add fejlmeddelse til flask..
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
        result = call_wikidata_API(query)

        logging.info(result)
        triples.extend(result)

    merged_triples = {
        "triples": triples
    }
    return jsonify(merged_triples)

if __name__ == '__main__':
   wikidataEndpoint.run(host='0.0.0.0', port=5002)