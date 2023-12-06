# from spaCy.spaCy import extract_entities
from flask import Flask, request, jsonify
import requests
import json
import logging

krEndpoint = Flask(__name__)
logging.basicConfig(level=logging.INFO)


# Function to call the extract_entities API
def call_extract_entities(input_string):
    # Define the URL of the extract_entities API
    url = 'http://spacy-container:5003/extract_entities'
    # Define the headers for the request
    headers = {'Content-Type': 'application/json'}
    # Define the data for the request
    data = {'input_string': input_string}
    # Send a POST request to the extract_entities API
    logging.info("Calling spaCy function")
    # Log the request body
    logging.info(f'Request body: {json.dumps(data)}')
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # If the request was successful, return the response as a Python object
    if response.status_code == 200:
        return response.json()
    # If the request failed, log an error message and return None
    else:
        logging.info(f'Request failed with status code {response.status_code}')
        return None


def call_llama(user_prompt, pre_prompt, knowledge_graph, tokens):
    # Define the URL of the llama api
    url = 'http://llama-container:5004/llama'
    # Define the headers for the request
    headers = {'Content-Type': 'application/json'}

    system_message = f'{pre_prompt} {knowledge_graph}'
    # Define the data for the request
    input = {'user_message': user_prompt, 'system_message': system_message, 'max_tokens': tokens}
    # Send the POST request to the llama API
    logging.info('Calling Llama function')
    # Log the request body
    logging.info(f'Request body: {json.dumps(input)}')
    response = requests.post(url, headers=headers, data=json.dumps(input))
    logging.info(f'LLama response: {response}')

    # if the request was successful, return the response as a Python object
    if response.status_code == 200:
        return response.json()
    # If the request failed, log an error message and return none
    else:
        logging.info(f'Request failed with status code {response.status_code}')
        return None


def get_api_data(keywords):
    # Define the URL of the extract_entities API
    url = 'http://api-container:5002/GetTriples'
    # Define the headers for the request
    headers = {'Content-Type': 'application/json'}
    # Define the data for the request
    data = {'keywords': keywords}
    # Send a POST request to the extract_entities API
    logging.info("Calling database API function")
    # Log the request body
    logging.info(f'Request body: {json.dumps(data)}')
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # If the request was successful, return the response as a Python object
    if response.status_code == 200:
        return response.json()
    # If the request failed, log an error message and return None
    else:
        logging.info(f'Request failed with status code {response.status_code}')
        return None

# The following 5 functions are placeholder code, for potential structural improvements in the code
# Currently NOT implemented 

def promptUser():
    print("What would you like to ask the chatbot?")
    prompt = input("")
    print("Question: " + prompt)
    return prompt


def processKeywords(keywords):
    processedKeywords = []
    raise Exception("'processKeywords' Not yet implemented")
    return processedKeywords


def getGraphAPIData(Keywords):
    knowledgeGraphdata = []
    raise Exception("'getGraphAPIData' Not yet implemented")
    return knowledgeGraphdata


def processGraphData(knowledgeGraphdata):
    processedKnowledgeGraphData = []
    raise Exception("'processGraphData' Not yet implemented")
    return processedKnowledgeGraphData


def getChatbotResponse(processedData):
    response = ""

    print("Answer: " + response)
    raise Exception("'getChatbotResponse' Not yet implemented")
    return response


# Get input from the user
# userInput = promptUser()

# Define a route for the main Knowledge retriever API. This will be the endpoint for the function.
@krEndpoint.route('/knowledge_retriever', methods=['POST'])
def knowledge_retriever():
    # Get the input string from the JSON body of the request.
    userinput = request.json['input_string']
    # Call the extract_entities API in the spacy service to get keywords from the user input
    keywords = call_extract_entities(userinput)
    knowledgeGraphData = get_api_data(keywords)
    llama_response = None

    #logging.info(f'RunLlama: {request.json["run_llama"]}, hasattr: {hasattr(request.json, "run_llama")}')
    if 'run_llama' not in request.json or request.json['run_llama'] is True:
        llama_response = call_llama(userinput, 'Based on this prompt, give me an answer', knowledgeGraphData, 1000)

    # Error handling
    if llama_response is None:
        logging.info('Llama output empty')
        return jsonify({'Llama error': 'Llama function failed or was not executed', 'Knowledge Graph output': knowledgeGraphData})
    else:
        return llama_response


# Run the Flask app.
if __name__ == '__main__':
    krEndpoint.run(host='0.0.0.0', port=5001)

# Placeholder code for further processing and response generation
# processedKeywords = processKeywords(keywords)

# calls API to get Knowledge Graph data
# knowledgeGraphdata = getGraphAPIData(processedKeywords)

# processedData = processGraphData(knowledgeGraphdata)

# response = getChatbotResponse(processedData)
