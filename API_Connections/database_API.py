# Purpose of this file is to setup an API, which returns a set of partial triples from the KNOX database
from flask import Flask, request, jsonify
import logging
import requests
#keywords = ["Aalborg", "Berlin"]
url = "http://130.225.57.13/knox-api/triples?g=http://knox_database"

KnoxDatabaseEndpoint = Flask(__name__)
logging.basicConfig(level=logging.INFO)


def add_url_query(keyword, type):
    if (not(type == "subject" or type == "object")):
        raise Exception("type has to be subject or object.")

    if type == "subject":
        print(url + "&s=" + keyword)
        return url + "&s=" + keyword

    elif type == "object":
        print(url + "&o=" + keyword)
        return url + "&o=" + keyword

# Returns the entities extracted in a partial triple consisting of Subject and Object the user input.
@KnoxDatabaseEndpoint.route('/GetTriples', methods=['POST'])
def GetTriples():
    logging.info("GetTriples was called")
    keywords = request.json['keywords']
    logging.info(request.json)
    logging.info(keywords)
    triples = []
    for entity in keywords:
        header={"Access-Authorization":"internal_key"}

        # Add each entity add as subject and object
        subURL = add_url_query(entity, "subject")
        objURL = add_url_query(entity, "object")

        subjectResponse = requests.get(subURL,headers=header)  # only works if you are connected to KNOXserver: ssh <studiemail>@knox-kb01.srv.aau.dk -L 8000:localhost:8081.
        objectResponse = requests.get(objURL,headers=header)  # only works if you are connected to KNOXserver: ssh <studiemail>@knox-kb01.srv.aau.dk -L 8000:localhost:8081.

        if subjectResponse.status_code >= 500 or objectResponse.status_code >= 500:
            raise Exception("Serverside Error")

        elif subjectResponse.status_code == 400 or objectResponse.status_code == 400:
            raise Exception("Bad request") #Often the database group that have changed something on the endpoint.

        logging.info(subjectResponse.status_code)
        logging.info(objectResponse.status_code)
        triples.extend(subjectResponse.json()["triples"])
        triples.extend(objectResponse.json()["triples"])
        logging.info(triples)

    merged_triples = {"triples": triples}
    return jsonify(merged_triples)

if __name__ == '__main__':
   KnoxDatabaseEndpoint.run(host='0.0.0.0', port=5002)
