import pytest

# Create a fixture of the LlamaEndpoint. It will create an instance of the Llama flask app and configure it for testing
from llama_cpu_server import app


# Create unit tests for the LlamaEndpoint
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.mark.parametrize("system_message, user_message, max_tokens", [
    ("You are a helpful assistant", "Generate a list of 5 funny dog names", 100)
])
def test_llama(client, system_message, user_message, max_tokens):
    # Simulate a POST request to the endpoint
    response = client.post('/llama', json={'system_message': system_message, 'user_message': user_message,
                                           'max_tokens': max_tokens})
    response_json = response.get_json()
    # Check that the response status code is 200 (OK)
    assert response_json is not None
    assert response.status_code == 200

def test_llama_fail(client):
    # Simulate a POST request to the endpoint
    longvar = "test " * 1000
    response = client.post('/llama', json={'system_message': longvar, 'user_message': longvar,
                                           'max_tokens': 100})
    response_json = response.get_json()
    # Check that the response status code is 200 (OK)
    assert response_json is not None
    assert response.status_code == 500