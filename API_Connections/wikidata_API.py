from SPARQLWrapper import SPARQLWrapper, JSON
from requests import get

keywords = ["Aalborg", "Berlin"]

# Get wikidata Q-number for all entities.
def get_qnumber(wikiarticle, wikisite):
    resp = get('https://www.wikidata.org/w/api.php', {
                'action': 'wbgetentities',
                'titles': wikiarticle,
                'sites': wikisite,
                'props': '',
                'format': 'json'
                           }).json()

    return list(resp['entities'])[0]

def call_wikidata_API(query):
    # Set up the SPARQL endpoint URL
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

    # Set the query string and return format
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    # Execute the query and get the results
    results = sparql.query().convert()
    # Construct the desired JSON structure
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

    # Create the final JSON object
    json_object = {
        # "query": query,  #Query udkommenteret, da vi ikke ønsker at bruge for mange tokens i Llama input.
        "triples": json_results
    }

    # return json object
    return json_object

def getAllKGs(keywords):
    KGs = []

    for entity in keywords:
        s_value = "wd:" + get_qnumber(wikiarticle=entity, wikisite="enwiki")
        print(s_value)
        # Set the query string
        query = f"""
                SELECT DISTINCT ?subject ?predicate ?object
                WHERE {{
                 VALUES (?s) {{({s_value})}}
                 ?s ?wdt ?o .
                 ?wd wikibase:directClaim ?wdt .
                 ?wd rdfs:label ?wdLabel .
                 ?s rdfs:label ?sLabel .
                 ?o rdfs:label ?oLabel .
                 FILTER (lang(?sLabel) = "en")
                 FILTER (lang(?oLabel) = "en")
                 FILTER (lang(?wdLabel) = "en")
                 BIND (COALESCE(?oLabel, ?o) AS ?object)
                 BIND (COALESCE(?wdLabel, ?wd) AS ?predicate)
                 BIND (?sLabel AS ?subject)
                 }} 
                ORDER BY xsd:integer(STRAFTER(STR(?wd), "http://www.wikidata.org/entity/P"))
                LIMIT 10
                """
        result = call_wikidata_API(query)
        print(result)
        KGs.append(result)


getAllKGs(keywords)


''' udkommenteret
query = """
SELECT DISTINCT ?subject ?predicate ?object
WHERE {
  VALUES (?s) {(wd:Q25410)}
  ?s ?wdt ?o .
  ?wd wikibase:directClaim ?wdt .
  ?wd rdfs:label ?wdLabel .
  ?s rdfs:label ?sLabel .
  ?o rdfs:label ?oLabel .
  FILTER (lang(?sLabel) = "en")
  FILTER (lang(?oLabel) = "en")
  FILTER (lang(?wdLabel) = "en")
  BIND (COALESCE(?oLabel, ?o) AS ?object)
  BIND (COALESCE(?wdLabel, ?wd) AS ?predicate)
  BIND (?sLabel AS ?subject)
 } 
ORDER BY xsd:integer(STRAFTER(STR(?wd), "http://www.wikidata.org/entity/P"))
LIMIT 10
"""
'''