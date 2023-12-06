import pytest
import json
from flask import jsonify
import wikidata_API
from wikidata_API import wikidata_endpoint


@pytest.fixture  # Create fixture of wikidata_endpoint. It will create an instance of the wikidata_API flask app and configure it for testing
def client():
    wikidata_endpoint.config['TESTING'] = True
    with wikidata_endpoint.test_client() as client:
        yield client


# Use this to add more tests
@pytest.mark.parametrize("keywords, hasTriples", [
    ("Aalborg", True),
    ("dfghjkl", False),
    ("Barack Obama", True),
    ("asdfghjk", False)
])
def test_get_triples_recieving_triples(client, keywords, hasTriples):
    # Simulate a POST request to the endpoint
    response = client.post('/GetTriples', json={'keywords': keywords})
    response_json = response.get_json()
    # Check that the response status code is 200 (OK)
    assert response.status_code == 200
    # Check that the json response contains a key 'triple'
    assert response_json.get('triples') is not None
    # Check that the response contains any or no triples based on input
    assert hasTriples == (len(response_json['triples']) != 0)


# Use this to add more tests
@pytest.mark.parametrize("wikipage, expected_qnumber", [
    ("Aalborg", "Q25410"),
    ("dfghjkl", "-1"),
    ("Barack Obama", "Q76"),
    ("asdfghjk", "-1")
])
def test_get_wikidata_id_recieves_correct_ID(wikipage, expected_qnumber):
    assert wikidata_API.get_wikidata_id(wikipage) == expected_qnumber


# Use this to add more tests
@pytest.mark.parametrize("query, exceptionMessage", [
    ("""  SELECT ?item ?itemLabel 
         WHERE 
         {
         ?item wdt:P31 wd:Q146.
         SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
         }""", "result did not contain either subject, object or predicate"),
    ("""  SELECT ?subject ?object ?predicate
         WHERE 
         {
         ?item wdt:P31 wd:Q146.
         SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
         }""", "result needs to contain atleast one element"),
    ("qwertyuip", "Bad Query")
])
def test_get_triples_from_wikidata_produces_exceptions(query, exceptionMessage):
    with pytest.raises(Exception) as exectionInfo:
        assert wikidata_API.get_triples_from_wikidata(query)
    assert str(exectionInfo.value) == exceptionMessage


# Use this to add more tests
@pytest.mark.parametrize("jsonObject, exceptionMessage", [
    ("qwerty", "Invalid JSON format. Expected 'results' with 'bindings'"),
    ({
         "results": {
             "bindings": [
                 {
                     "subject": {"value": "example_subject"},
                     "predicate": {"value": "example_predicate"},
                     "object": {"value": "example_object"}
                 },
                 # Missing "subject" key in the second binding
                 {
                     "predicate": {"value": "another_predicate"},
                     "object": {"value": "another_object"}
                 }
             ]
         }
     }, "Invalid JSON format. Expected 'subject', 'predicate', and 'object' in each binding")
])
def test_format_triples_object_produces_exceptions(jsonObject, exceptionMessage):
    with pytest.raises(Exception) as exectionInfo:
        assert wikidata_API.format_triple_object(jsonObject)
    assert str(exectionInfo.value) == exceptionMessage
