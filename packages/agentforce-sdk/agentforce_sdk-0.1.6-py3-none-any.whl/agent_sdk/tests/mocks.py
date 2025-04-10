"""Mock objects for testing AgentForce SDK."""

import json
from unittest.mock import MagicMock
import sys

class MockSalesforceLogin:
    """Mock for SalesforceLogin function."""
    
    @classmethod
    def mock_login(cls, username, password, domain):
        """Mock the SalesforceLogin function."""
        return "fake-session-id", "test.salesforce.com"
    
    @staticmethod
    def login(*args, **kwargs):
        """Mock login method."""
        return ("MOCK_SESSION_ID", "https://mock.salesforce.com", "mock@example.com")

class MockSalesforce:
    """Mock for Salesforce class."""
    
    def __init__(self, *args, **kwargs):
        """Initialize the mock Salesforce object."""
        self.GenAIAgent__c = MagicMock()
        self.GenAIAgent__c.get.return_value = {
            "Id": "01p5f000000ABCDE",
            "DeveloperName": "TestAgent",
            "MasterLabel": "Test Agent",
            "Description": "Test agent for unit tests"
        }
        
        self.query = MagicMock()
        self.query.return_value = {
            "records": [
                {
                    "Id": "01p5f000000ABCDE",
                    "DeveloperName": "TestAgent",
                    "MasterLabel": "Test Agent",
                    "Description": "Test agent for unit tests"
                }
            ]
        }

class MockRequests:
    """Mock for requests module."""
    
    @staticmethod
    def create_response(status_code=200, json_data=None, text=None):
        """Create a mock response object."""
        response = MagicMock()
        response.status_code = status_code
        
        if json_data:
            response.json.return_value = json_data
        
        if text:
            response.text = text
        elif json_data:
            response.text = json.dumps(json_data)
        else:
            response.text = ""
            
        if status_code >= 400:
            response.raise_for_status.side_effect = Exception(f"HTTP Error: {status_code}")
        
        return response
    
    @staticmethod
    def mock_post(*args, **kwargs):
        """Mock the requests.post method."""
        if "metadata/deployRequest" in args[0]:
            return MockRequests.create_response(json_data={
                "id": "0Af5f000000ABCDE",
                "status": "InProgress"
            })
        return MockRequests.create_response()
    
    @staticmethod
    def mock_get(*args, **kwargs):
        """Mock the requests.get method."""
        if "metadata/deployRequest" in args[0]:
            return MockRequests.create_response(json_data={
                "id": "0Af5f000000ABCDE",
                "status": "Succeeded",
                "details": {
                    "successes": [
                        {
                            "componentType": "GenAIAgent",
                            "id": "01p5f000000ABCDE"
                        }
                    ],
                    "errors": []
                }
            })
        return MockRequests.create_response()
    
    @staticmethod
    def mock_request(method, *args, **kwargs):
        """Mock the requests.request method."""
        if method.upper() == "POST":
            return MockRequests.mock_post(*args, **kwargs)
        elif method.upper() == "GET":
            return MockRequests.mock_get(*args, **kwargs)
        return MockRequests.create_response()

# Mock simple_salesforce module
class MockSimpleSalesforce:
    """Mock for simple_salesforce.Salesforce."""
    
    def __init__(self, *args, **kwargs):
        """Initialize the mock."""
        self.session_id = "MOCK_SESSION_ID"
        self.instance_url = "https://mock.salesforce.com"
        
    def query(self, *args, **kwargs):
        """Mock query method."""
        return {"records": []}
    
    def __getattr__(self, name):
        """Return a mock for any attribute access."""
        return MagicMock()

# Add module mocks to sys.modules
sys.modules["simple_salesforce"] = MagicMock()
sys.modules["simple_salesforce"].Salesforce = MockSimpleSalesforce
sys.modules["simple_salesforce"].SalesforceLogin = MockSalesforceLogin 