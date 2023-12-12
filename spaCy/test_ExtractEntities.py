import pytest

from spaCy import spacy_endpoint

@pytest.fixture # Create fixture of spaCyEndpoint. It will create an instance of the spaCy flask app and configure it for testing
def client():
   spacy_endpoint.config['TESTING'] = True
   with spacy_endpoint.test_client() as client:
       yield client

# Use this to add more tests
@pytest.mark.parametrize("input_string, expected_entities", [
   ("Hvem er Obama", ["Obama"]),
   ("hvor er Obama født", ["Obama"]),
   ("Aalborg er i Danmark", ["Aalborg", "Danmark"]),
   ("Hvordan åbner man en flaske vin?", []),
   ("Jeg bor i New York", ["New York"]),
   ("Hvem er Elon Musk", ["Elon Musk"])
])


def test_extract_entities(client, input_string, expected_entities):
   # Simulate a POST request to the endpoint
   response = client.post('/extract_entities', json={'input_string': input_string})
   response_json = response.get_json()
   # Check that the response status code is 200 (OK)
   assert response.status_code == 200
   # Check that the response data is as expected
   assert response_json == expected_entities

