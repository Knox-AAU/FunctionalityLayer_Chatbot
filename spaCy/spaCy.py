from flask import Flask, request, jsonify
import spacy
import logging

# Initialize danish spaCy mode, and Flask library
spacy_endpoint = Flask(__name__)
nlp = spacy.load('da_core_news_md')
logging.basicConfig(level=logging.INFO)


# Define a route for the API. This will be the endpoint for the function.
@spacy_endpoint.route('/extract_entities', methods=['POST'])
def extract_entities():
    try:
        logging.info("spaCy function was called")
        logging.info(request.json)
        # Get the input string from the JSON body of the request.
        input_string = request.json['input_string']
        # Use spaCy to process the input string
        processed_input = nlp(input_string)
        # Extract the entities from the processed text.
        entities = [ent.text for ent in processed_input.ents]
        # Return the entities as a JSON response.
        return jsonify(entities)
    except Exception as e:
        return jsonify({'error': str(e)})


# Run the Flask app.
if __name__ == '__main__':
    spacy_endpoint.run(host='0.0.0.0', port=5003)
