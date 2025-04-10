"""Test cases for core functionality."""

import os
import sys
import json
import pytest
import unittest
import tempfile
import shutil
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch, MagicMock, mock_open

from ..config import Config
from ..core.agentforce import Agentforce
from ..core.auth import BasicAuth, DirectAuth
from ..exceptions import AgentforceAuthError, AgentforceApiError, ValidationError
from ..models.agent import Agent
from ..core.base import AgentforceBase
from ..utils.agent_utils import AgentUtils

# Add the parent directory to sys.path if needed for testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from .utils import SAMPLE_AGENT_DATA, create_temp_json_file
from .mocks import MockSalesforceLogin, MockSalesforce, MockRequests


class TestAgentForceBase(unittest.TestCase):
    """Tests for the AgentForceBase class."""
    
    @patch('agent_sdk.core.base.SalesforceLogin', side_effect=MockSalesforceLogin.mock_login)
    @patch('agent_sdk.core.base.Salesforce')
    def test_init_and_login(self, mock_sf, mock_login):
        """Test initialization and login."""
        # Test initialization without login
        auth = BasicAuth(
            username=None,
            password=None
        )
        base = AgentforceBase(auth=auth)
        self.assertIsNone(base.session_id)
        self.assertIsNone(base.instance_url)
        
        # Test initialization with login
        auth = BasicAuth(
            username="test@example.com",
            password="password"
        )
        base = AgentforceBase(auth=auth)
        mock_login.assert_called_once_with(username="test@example.com", password="password", domain="login")
        self.assertEqual(base.session_id, "fake-session-id")
        self.assertEqual(base.instance_url, "https://test.salesforce.com")
    
    @patch('agent_sdk.core.base.SalesforceLogin', side_effect=MockSalesforceLogin.mock_login)
    @patch('agent_sdk.core.base.Salesforce')
    def test_login_method(self, mock_sf, mock_login):
        """Test explicit login method."""
        auth = BasicAuth(
            username=None,
            password=None
        )
        base = AgentforceBase(auth=auth)
        self.assertIsNone(base.session_id)
        
        auth2 = BasicAuth(
            username="test@example.com",
            password="password"
        )
        base = AgentforceBase(auth=auth2)
        result = base.login()
        
        self.assertTrue(result)
        mock_login.assert_called_once_with(username="test@example.com", password="password", domain="login")
        self.assertEqual(base.session_id, "fake-session-id")
        self.assertEqual(base.instance_url, "https://test.salesforce.com")
    
    @patch('agent_sdk.core.base.SalesforceLogin', side_effect=MockSalesforceLogin.mock_login)
    @patch('agent_sdk.core.base.Salesforce')
    def test_sf_property(self, mock_sf, mock_login):
        """Test the sf property."""
        base = AgentforceBase()
        
        # Should return None when not authenticated
        self.assertIsNone(base.sf)
        
        # Should login and return Salesforce instance when authenticated
        auth = BasicAuth(
            username="test@example.com",
            password="password"
        )
        base = AgentforceBase(auth=auth)
        sf = base.sf
        
        mock_login.assert_called_once()
        mock_sf.assert_called_once()
        self.assertIsNotNone(sf)
    
    @patch('agent_sdk.core.base.SalesforceLogin', side_effect=MockSalesforceLogin.mock_login)
    @patch('agent_sdk.core.base.requests.request', side_effect=MockRequests.mock_request)
    def test_execute_rest_request(self, mock_request, mock_login):
        """Test execute_rest_request method."""
        auth = BasicAuth(
            username="test@example.com",
            password="password"
        )
        base = AgentforceBase(auth=auth)
        
        # Test GET request
        result = base.execute_rest_request("GET", "some/endpoint")
        mock_request.assert_called_with(
            "GET", 
            "https://test.salesforce.com/services/data/v61.0/some/endpoint",
            headers={
                'Authorization': 'Bearer fake-session-id',
                'Content-Type': 'application/json'
            }
        )
        
        # Test POST request with data
        data = {"key": "value"}
        result = base.execute_rest_request("POST", "some/endpoint", json=data)
        mock_request.assert_called_with(
            "POST", 
            "https://test.salesforce.com/services/data/v61.0/some/endpoint",
            headers={
                'Authorization': 'Bearer fake-session-id',
                'Content-Type': 'application/json'
            },
            json=data
        )
    
    @patch('agent_sdk.core.base.SalesforceLogin', side_effect=MockSalesforceLogin.mock_login)
    @patch('agent_sdk.core.base.requests.request', side_effect=MockRequests.mock_request)
    def test_http_helper_methods(self, mock_request, mock_login):
        """Test HTTP helper methods (get, post, patch, delete)."""
        auth = BasicAuth(
            username="test@example.com",
            password="password"
        )
        base = AgentforceBase(auth=auth)
        
        # Test GET
        base.get("some/endpoint", params={"q": "query"})
        mock_request.assert_called_with(
            "GET", 
            "https://test.salesforce.com/services/data/v61.0/some/endpoint",
            headers={
                'Authorization': 'Bearer fake-session-id',
                'Content-Type': 'application/json'
            },
            params={"q": "query"}
        )
        
        # Test POST
        data = {"key": "value"}
        base.post("some/endpoint", data=data)
        mock_request.assert_called_with(
            "POST", 
            "https://test.salesforce.com/services/data/v61.0/some/endpoint",
            headers={
                'Authorization': 'Bearer fake-session-id',
                'Content-Type': 'application/json'
            },
            json=data
        )
        
        # Test PATCH
        base.patch("some/endpoint", data=data)
        mock_request.assert_called_with(
            "PATCH", 
            "https://test.salesforce.com/services/data/v61.0/some/endpoint",
            headers={
                'Authorization': 'Bearer fake-session-id',
                'Content-Type': 'application/json'
            },
            json=data
        )
        
        # Test DELETE
        base.delete("some/endpoint")
        mock_request.assert_called_with(
            "DELETE", 
            "https://test.salesforce.com/services/data/v61.0/some/endpoint",
            headers={
                'Authorization': 'Bearer fake-session-id',
                'Content-Type': 'application/json'
            }
        )
    
    def test_check_auth(self):
        """Test authentication check."""
        base = AgentforceBase()
        
        # Should raise ValueError when not authenticated
        with self.assertRaises(ValueError):
            base._check_auth()
        
        # Should not raise error when authenticated
        base.auth.session_id = "fake-session-id"
        base.auth.instance_url = "https://test.salesforce.com"
        base._check_auth()  # Should not raise exception


class TestAgentForce(unittest.TestCase):
    """Tests for the AgentForce class."""
    
    @patch('agent_sdk.core.agent.AgentforceBase.__init__')
    def test_init(self, mock_base_init):
        """Test initialization."""
        mock_base_init.return_value = None
        
        auth = BasicAuth(
            username="test@example.com",
            password="password",
            domain="test"
        )
        agent_force = Agentforce(auth=auth)
        
        mock_base_init.assert_called_once_with(username="test@example.com", password="password", domain="test")
    
    def test_create_agent(self):
        """Test creating an agent from modular files."""
        # Get the path to the modular agent example
        modular_dir = os.path.join(os.path.dirname(__file__), '../../examples/assets/modular_agent_dir')
        # Create the agent from modular files
        agent = AgentUtils.create_agent_from_modular_files(modular_dir, "order_management_agent")
        
        # Verify agent properties
        self.assertIsInstance(agent, Agent)
        self.assertEqual(agent.name, "Order Management Agent")
        self.assertEqual(agent.description, "An agent that helps customers manage their orders and reservations")
        self.assertEqual(agent.agent_type, "Bot")
        self.assertEqual(agent.company_name, "Salesforce")
        
        # Verify sample utterances
        self.assertEqual(len(agent.sample_utterances), 5)
        self.assertIn("I want to place an order", agent.sample_utterances)
        self.assertIn("Check my order status", agent.sample_utterances)
        
        # Verify system messages
        self.assertEqual(len(agent.system_messages), 2)
        self.assertEqual(agent.system_messages[0].message, "You are a helpful order management assistant.")
        self.assertEqual(agent.system_messages[0].msg_type, "system")
        
        # Verify variables
        self.assertEqual(len(agent.variables), 1)
        self.assertEqual(agent.variables[0].name, "customer_id")
        self.assertEqual(agent.variables[0].data_type, "String")
        
        # Verify topics
        self.assertEqual(len(agent.topics), 2)
        
        # Verify order management topic
        order_topic = agent.topics[0]
        self.assertEqual(order_topic.name, "Order Management")
        self.assertEqual(order_topic.description, "Handle order-related queries and actions")
        self.assertEqual(order_topic.scope, "public")
        self.assertEqual(len(order_topic.instructions), 3)
        self.assertEqual(len(order_topic.actions), 2)
        
        # Verify order management actions
        place_order = order_topic.actions[0]
        self.assertEqual(place_order.name, "Place Order")
        self.assertEqual(len(place_order.inputs), 2)
        self.assertEqual(place_order.inputs[0].name, "product_id")
        self.assertEqual(place_order.inputs[1].name, "quantity")
        
        check_status = order_topic.actions[1]
        self.assertEqual(check_status.name, "Check Order Status")
        self.assertEqual(len(check_status.inputs), 1)
        self.assertEqual(check_status.inputs[0].name, "order_id")
        
        # Verify reservation management topic
        reservation_topic = agent.topics[1]
        self.assertEqual(reservation_topic.name, "Reservation Management")
        self.assertEqual(reservation_topic.description, "Handle reservation-related queries and actions")
        self.assertEqual(reservation_topic.scope, "public")
        self.assertEqual(len(reservation_topic.instructions), 3)
        self.assertEqual(len(reservation_topic.actions), 1)
        
        # Verify reservation management action
        make_reservation = reservation_topic.actions[0]
        self.assertEqual(make_reservation.name, "Make Reservation")
        self.assertEqual(len(make_reservation.inputs), 3)
        self.assertEqual(make_reservation.inputs[0].name, "date")
        self.assertEqual(make_reservation.inputs[1].name, "time")
        self.assertEqual(make_reservation.inputs[2].name, "party_size")
        
        # Test creating the agent in Salesforce
        with patch('agent_sdk.core.agent.AgentforceBase._check_auth') as mock_check_auth, \
             patch('agent_sdk.core.agent.zipfile.ZipFile') as mock_zipfile, \
             patch('agent_sdk.core.agent.Agentforce._deploy_to_salesforce') as mock_deploy:
            
            mock_deploy.return_value = {"status": "Succeeded"}
            
            # Create the agent
            result = agent.create()
            
            mock_check_auth.assert_called_once()
            mock_zipfile.assert_called()
            mock_deploy.assert_called_once()
            self.assertEqual(result["status"], "Succeeded")
    
    def test_create_agent_from_dict(self):
        """Test creating an agent from a dictionary."""
        # Create agent from dictionary
        agent = Agent.from_dict(SAMPLE_AGENT_DATA)
        
        self.assertIsInstance(agent, Agent)
        self.assertEqual(agent.name, "TestAgent")
        self.assertEqual(agent.description, "Test agent for unit tests")
        self.assertEqual(len(agent.topics), 1)
        
        # Test creating the agent in Salesforce
        with patch('agent_sdk.core.agent.AgentforceBase._check_auth') as mock_check_auth, \
             patch('agent_sdk.core.agent.zipfile.ZipFile') as mock_zipfile, \
             patch('agent_sdk.core.agent.Agentforce._deploy_to_salesforce') as mock_deploy:
            
            mock_deploy.return_value = {"status": "Succeeded"}
            
            # Create the agent
            result = agent.create()
            
            mock_check_auth.assert_called_once()
            mock_zipfile.assert_called()
            mock_deploy.assert_called_once()
            self.assertEqual(result["status"], "Succeeded")
    
    def test_create_agent_from_file(self):
        """Test creating an agent from a JSON file."""
        # Create a temporary JSON file
        json_file = create_temp_json_file(SAMPLE_AGENT_DATA)
        
        try:
            # Create agent from file
            agent = Agent.from_file(json_file)
            
            self.assertIsInstance(agent, Agent)
            self.assertEqual(agent.name, "TestAgent")
            self.assertEqual(agent.description, "Test agent for unit tests")
            self.assertEqual(len(agent.topics), 1)
            
            # Test creating the agent in Salesforce
            with patch('agent_sdk.core.agent.AgentforceBase._check_auth') as mock_check_auth, \
                 patch('agent_sdk.core.agent.zipfile.ZipFile') as mock_zipfile, \
                 patch('agent_sdk.core.agent.Agentforce._deploy_to_salesforce') as mock_deploy:
                
                mock_deploy.return_value = {"status": "Succeeded"}
                
                # Create the agent
                result = agent.create()
                
                mock_check_auth.assert_called_once()
                mock_zipfile.assert_called()
                mock_deploy.assert_called_once()
                self.assertEqual(result["status"], "Succeeded")
        finally:
            # Clean up the temporary file
            if os.path.exists(json_file):
                os.remove(json_file)
    
    def test_create_agent_from_directory(self):
        """Test creating an agent from a directory structure."""
        # Create a temporary directory structure
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create agent.json
            agent_data = {
                "agent_api_name": "TestAgent",
                "AI_Agent_Description": "Test agent from directory",
                "agent_type": "Internal",
                "company_name": "Test Company",
                "domain": "login"
            }
            
            with open(os.path.join(temp_dir, "agent.json"), "w") as f:
                json.dump(agent_data, f)
            
            # Create topics directory
            topics_dir = os.path.join(temp_dir, "topics")
            os.makedirs(topics_dir)
            
            # Create a topic file
            topic_data = {
                "Topic": "Test Topic",
                "ClassificationDescription": "A topic for testing",
                "Scope": "Test scope",
                "Instructions": ["Test instruction"]
            }
            
            with open(os.path.join(topics_dir, "test_topic.json"), "w") as f:
                json.dump(topic_data, f)
            
            # Create actions directory for the topic
            actions_dir = os.path.join(topics_dir, "test_topic", "actions")
            os.makedirs(actions_dir)
            
            # Create an action file
            action_data = {
                "action_name": "testAction",
                "inputs": [
                    {
                        "inputName": "testInput",
                        "input_description": "Test input",
                        "input_dataType": "string"
                    }
                ],
                "example_output": {
                    "status": "success"
                }
            }
            
            with open(os.path.join(actions_dir, "test_action.json"), "w") as f:
                json.dump(action_data, f)
            
            # Create agent from directory
            agent = Agent.from_directory(temp_dir)
            
            self.assertIsInstance(agent, Agent)
            self.assertEqual(agent.name, "TestAgent")
            self.assertEqual(agent.description, "Test agent from directory")
            self.assertEqual(len(agent.topics), 1)
            
            # Check that the topic and action were loaded correctly
            topic = agent.topics[0]
            self.assertEqual(topic["Topic"], "Test Topic")
            self.assertEqual(len(topic["Actions"]), 1)
            self.assertEqual(topic["Actions"][0]["action_name"], "testAction")
            
            # Test creating the agent in Salesforce
            with patch('agent_sdk.core.agent.AgentforceBase._check_auth') as mock_check_auth, \
                 patch('agent_sdk.core.agent.zipfile.ZipFile') as mock_zipfile, \
                 patch('agent_sdk.core.agent.Agentforce._deploy_to_salesforce') as mock_deploy:
                
                mock_deploy.return_value = {"status": "Succeeded"}
                
                # Create the agent
                result = agent.create()
                
                mock_check_auth.assert_called_once()
                mock_zipfile.assert_called()
                mock_deploy.assert_called_once()
                self.assertEqual(result["status"], "Succeeded")
    
    @patch('agent_sdk.core.agent.AgentforceBase._check_auth')
    @patch('agent_sdk.core.agent.zipfile.ZipFile')
    @patch('agent_sdk.core.agent.deploy_metadata_to_salesforce')
    def test_deploy_agent(self, mock_deploy, mock_zipfile, mock_check_auth):
        """Test deploying an agent."""
        agent_force = Agentforce()
        mock_deploy.return_value = {"status": "Succeeded"}
        
        # Create a mock agent
        mock_agent = MagicMock()
        mock_agent.to_dict.return_value = SAMPLE_AGENT_DATA
        mock_agent.name = "TestAgent"
        
        # Test deploy_agent method
        result = agent_force.deploy_agent(mock_agent)
        
        mock_check_auth.assert_called_once()
        mock_zipfile.assert_called()
        mock_deploy.assert_called_once()
        self.assertEqual(result["status"], "Succeeded")
    
    @patch('agent_sdk.core.agent.AgentforceBase._check_auth')
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=b'zip_content')
    @patch('agent_sdk.core.agent.requests.post')
    @patch('agent_sdk.core.agent.Agentforce._check_deployment_status')
    def test_deploy_to_salesforce(self, mock_check_status, mock_post, mock_open, mock_check_auth):
        """Test deploying a metadata zip file to Salesforce."""
        agent_force = Agentforce()
        agent_force.session_id = "fake-session-id"
        agent_force.instance_url = "https://test.salesforce.com"
        
        mock_check_status.return_value = {"status": "Succeeded"}
        mock_post.return_value = MagicMock(status_code=200, json=lambda: {"id": "0Af5f000000ABCDE"})
        
        result = agent_force._deploy_to_salesforce("path/to/zip.zip", "TestAgent")
        
        mock_check_auth.assert_called_once()
        mock_open.assert_called_once_with("path/to/zip.zip", "rb")
        mock_post.assert_called_once()
        mock_check_status.assert_called_once()
        self.assertEqual(result["status"], "Succeeded")
    
    @patch('agent_sdk.core.agent.AgentforceBase._check_auth')
    @patch('agent_sdk.core.agent.requests.get')
    @patch('agent_sdk.core.agent.time.sleep')
    def test_check_deployment_status(self, mock_sleep, mock_get, mock_check_auth):
        """Test checking deployment status."""
        agent_force = Agentforce()
        agent_force.session_id = "fake-session-id"
        agent_force.instance_url = "https://test.salesforce.com"
        
        mock_get.return_value = MagicMock(status_code=200, json=lambda: {
            "id": "0Af5f000000ABCDE",
            "status": "Succeeded",
            "details": {
                "successes": [{"componentType": "GenAIAgent", "id": "01p5f000000ABCDE"}],
                "errors": []
            }
        })
        
        result = agent_force._check_deployment_status("0Af5f000000ABCDE")
        
        mock_check_auth.assert_called_once()
        mock_get.assert_called_once()
        self.assertEqual(result["status"], "Succeeded")
    
    @patch('agent_sdk.core.agent.AgentforceBase._check_auth')
    @patch('agent_sdk.core.agent.AgentforceBase.sf', new_callable=unittest.mock.PropertyMock)
    def test_list_agents(self, mock_sf_property, mock_check_auth):
        """Test listing agents."""
        mock_sf = MockSalesforce()
        mock_sf_property.return_value = mock_sf
        
        agent_force = Agentforce()
        agents = agent_force.list_agents()
        
        mock_check_auth.assert_called_once()
        mock_sf.query.assert_called_once()
        self.assertEqual(len(agents), 1)
    
    @patch('agent_sdk.core.agent.AgentforceBase._check_auth')
    @patch('agent_sdk.core.agent.AgentforceBase.sf', new_callable=unittest.mock.PropertyMock)
    def test_get_agent(self, mock_sf_property, mock_check_auth):
        """Test getting a specific agent."""
        mock_sf = MockSalesforce()
        mock_sf_property.return_value = mock_sf
        
        agent_force = Agentforce()
        agent = agent_force.get_agent("01p5f000000ABCDE")
        
        mock_check_auth.assert_called_once()
        mock_sf.GenAIAgent__c.get.assert_called_once_with("01p5f000000ABCDE")
        self.assertEqual(agent["Id"], "01p5f000000ABCDE")


if __name__ == "__main__":
    unittest.main() 