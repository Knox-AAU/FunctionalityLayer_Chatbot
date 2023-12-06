# Purpose of this file is to setup an API, which returns a set of partial triples from the KNOX database
from flask import Flask, request, jsonify
import logging
import requests

knox_endpoint_url = "http://130.225.57.13/knox-api/triples?g=http://knox_database"

knox_database_endpoint = Flask(__name__)
logging.basicConfig(level=logging.INFO)


def get_endpoint_url(keyword, query_type):
    # Raise and exception if query_type is neither "subject" or "object"
    if (not(query_type == "subject" or query_type == "object")):
        raise Exception("query_type has to be subject or object.")

    if query_type == "subject":
        return knox_endpoint_url + "&s=" + keyword
    elif query_type == "object":
        return knox_endpoint_url + "&o=" + keyword

# Returns the entities extracted in a partial triple consisting of Subject and Object the user input.
@knox_database_endpoint.route('/GetTriples', methods=['POST'])
def GetTriples():
    
    logging.info("GetTriples was called")

    keywords = request.json['keywords']

    logging.info(request.json)
    logging.info(keywords)

    triples = []

    for keyword in keywords:
        header={"Access-Authorization":"internal_key"}

        # Add each keyword as subject and object
        subject_endpoint_url = get_endpoint_url(keyword, "subject")
        object_endpoint_url = get_endpoint_url(keyword, "object")

        subject_response = requests.get(subject_endpoint_url, headers=header)  # only works if you are connected to KNOXserver: ssh <studiemail>@knox-kb01.srv.aau.dk -L 8000:localhost:8081.
        object_response = requests.get(object_endpoint_url, headers=header)  # only works if you are connected to KNOXserver: ssh <studiemail>@knox-kb01.srv.aau.dk -L 8000:localhost:8081.

        if subject_response.status_code >= 500 or object_response.status_code >= 500:
            raise Exception("Serverside Error")

        elif subject_response.status_code == 400 or object_response.status_code == 400:
            raise Exception("Bad request") #Often the database group that have changed something on the endpoint.

        logging.info(subject_response.status_code)
        logging.info(object_response.status_code)

        triples.extend(subject_response.json()["triples"])
        triples.extend(object_response.json()["triples"])

        logging.info(triples)

    merged_triples = {"triples": triples}
    return jsonify(merged_triples)

if __name__ == '__main__':
   knox_database_endpoint.run(host='0.0.0.0', port=5002)
