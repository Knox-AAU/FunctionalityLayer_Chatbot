from SPARQLWrapper import SPARQLWrapper, JSON

# Set up the SPARQL endpoint URL
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

# Set the query string
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
    "query": query,
    "triples": json_results
}

# Print the final JSON object
#print(json_object['triples'])
print(json_object)
