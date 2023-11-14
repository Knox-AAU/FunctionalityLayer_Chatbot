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
    url = 'http://spacy-container:5000/extract_entities'
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


# Nedestående funktioner kan bare slettes og erstattes med de rigtige :)

def promptUser():
    print("What would you like to ask the chatbot?")
    prompt = input("")
    print("Question: " + prompt)
    return prompt


def processKeywords(keywords):
    processedKeywords = []
    raise Exception("'processKeywords' Not yet implemented")
    return processedKeywords


def getGraphAPIData(processedKeywords):
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


"""flag = True
while flag:"""


# Get input from the user
# userInput = promptUser()

# Define a route for the API. This will be the endpoint for the function.
@krEndpoint.route('/knowledge_retriever', methods=['POST'])
def knowledge_retriever():
    # Get the input string from the JSON body of the request.
    userinput = request.json['input_string']
    # Call the extract_entities API in the spacy service to get keywords from the user input
    try:
        keywords = call_extract_entities(userinput)
        if keywords is None:
            return jsonify({'error': 'Failed to extract keywords, Input string = ' + userinput})
        else:
            return jsonify(keywords)
    except Exception as e:
        return jsonify({'error': str(e)})


# Run the Flask app.
if __name__ == '__main__':
    krEndpoint.run(host='0.0.0.0', port=5001)

"""repeat = "flag"
while repeat != "y" and repeat != "n":
    repeat = input("Har du lyst til at spørge om noget nyt? (y/n)")
if repeat == "n":
    flag = False"""

# Placeholder code for further processing and response generation
# processedKeywords = processKeywords(keywords)

# calls API to get Knowledge Graph data
# knowledgeGraphdata = getGraphAPIData(processedKeywords)

# processedData = processGraphData(knowledgeGraphdata)

# response = getChatbotResponse(processedData)
