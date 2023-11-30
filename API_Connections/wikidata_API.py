from flask import Flask, request, jsonify
from SPARQLWrapper import SPARQLWrapper, JSON
from requests import get
import logging

wikidataEndpoint = Flask(__name__)
logging.basicConfig(level=logging.INFO)

#keywords = ["Aalborg", "Berlin"]

# Get wikidata Q-number for all entities.
def get_qnumber(wikiarticle, wikisite):
    resp = get('https://www.wikidata.org/w/api.php', {
                'action': 'wbgetentities',
                'titles': wikiarticle,
                'sites': wikisite,
                'props': '',
                'format': 'json'
                           }).json()
    logging.info(resp)
    logging.info(list(resp['entities'])[0])

    return list(resp['entities'])[0]

def formatTripleObject(results):
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
    results = sparql.query().convert()
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

    for entity in keywords:
        identifier_value = get_qnumber(wikiarticle=entity, wikisite="enwiki")
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
        result = call_wikidata_API(query)

        logging.info(result)
        triples.extend(result)

    merged_triples = {
        "triples": triples
    }
    return jsonify(merged_triples)

if __name__ == '__main__':
   wikidataEndpoint.run(host='0.0.0.0', port=5002)