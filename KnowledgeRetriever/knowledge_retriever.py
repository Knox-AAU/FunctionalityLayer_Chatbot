# from spaCy.spaCy import get_extracted_entities
from flask import Flask, request, jsonify
import requests
import json
import logging

knowledge_retriever_endpoint = Flask(__name__)
logging.basicConfig(level=logging.INFO)


# Function to call the get_extracted_entities API
def get_extracted_entities(input_string):
    # Define the URL of the get_extracted_entities API
    endpoint_url = 'http://spacy-container:5003/extract_entities'
    # Define the headers for the request
    headers = {'Content-Type': 'application/json'}
    # Define the data for the request
    data = {'input_string': input_string}
    # Send a POST request to the get_extracted_entities API
    logging.info("Calling spaCy function")

    response = requests.post(endpoint_url, headers=headers, data=json.dumps(data))

    # If the request was successful, return the response as a Python object
    if response.status_code == 200:
        return response.json()
    # If the request failed, log an error message and return None
    else:
        logging.info(f'Request failed with status code {response.status_code}')
        return None


def get_response_in_natural_language(user_prompt, system_prompt, triples, tokens):
    # Define the URL of the llama api
    endpoint_url = 'http://llama-container:5004/llama'

    # Define the headers for the request
    headers = {'Content-Type': 'application/json'}

    system_message = f'{system_prompt} {triples}'

    # Define the data for the request
    input = {'user_message': user_prompt, 'system_message': system_message, 'max_tokens': tokens}
    
    # Send the POST request to the llama API
    logging.info('Calling Llama function')

    response = requests.post(endpoint_url, headers = headers, data = json.dumps(input))

    # if the request was successful, return the response as a Python object
    if response.status_code == 200:
        return response.json()
    # If the request failed, log an error message and return none
    else:
        logging.info(f'Request failed with status code {response.status_code}')
        return jsonify({'Llama error': 'Llama function failed', 'Knowledge Graph output': triples})


def get_triples(keywords):
    # Define the URL of the get_extracted_entities API
    endpoint_url = 'http://api-container:5002/get_triples'
    # Define the headers for the request
    headers = {'Content-Type': 'application/json'}
    # Define the data for the request
    data = {'keywords': keywords}
    # Send a POST request to the get_extracted_entities API
    logging.info("Calling database API function")
    # Log the request body
    logging.info(f'Request body: {json.dumps(data)}')
    response = requests.post(endpoint_url, headers=headers, data=json.dumps(data))

    # If the request was successful, return the response as a Python object
    if response.status_code == 200:
        return response.json()
    # If the request failed, log an error message and return None
    else:
        logging.info(f'Request failed with status code {response.status_code}')
        return None


# Define a route for the main Knowledge retriever API. This will be the endpoint for the function.
@knowledge_retriever_endpoint.route('/knowledge_retriever', methods=['POST'])
def knowledge_retriever():
    # Get the input string from the JSON body of the request.
    user_prompt = request.json['input_string']

    # Call the get_extracted_entities API in the spacy service to get keywords from the user input
    keywords = get_extracted_entities(user_prompt)
    triples = get_triples(keywords)

    natural_language_response = None
    #logging.info(f'RunLlama: {request.json["run_llama"]}, hasattr: {hasattr(request.json, "run_llama")}')
    if 'run_llama' not in request.json or request.json['run_llama'] is True:
        natural_language_response = get_response_in_natural_language(user_prompt, 'Based on this prompt, give me an answer', triples, 1000)
    else:
        return jsonify({'Llama error': 'Llama function was not executed', 'Knowledge Graph output': triples})

    return natural_language_response


# Run the Flask app.
if __name__ == '__main__':
    knowledge_retriever_endpoint.run(host='0.0.0.0', port=5001)
