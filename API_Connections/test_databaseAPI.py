import pytest
from database_API import KnoxDatabaseEndpoint

@pytest.fixture # Create fixture of KnoxDatabaseEndpoint. It will create an instance of the database_API flask app and configure it for testing
def client():
   KnoxDatabaseEndpoint.config['TESTING'] = True
   with KnoxDatabaseEndpoint.test_client() as client:
       yield client

#def test_databaseAPI(client, input_string, expected_entities):
    # needs to be created when the server works again