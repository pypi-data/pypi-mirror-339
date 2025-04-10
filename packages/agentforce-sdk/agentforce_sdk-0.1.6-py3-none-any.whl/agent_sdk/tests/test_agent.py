from unittest import TestCase, mock
from unittest.mock import patch, MagicMock
from ..core.agentforce import Agentforce
from ..exceptions import AgentforceAuthError, AgentforceApiError

class TestAgent(TestCase):
    def setUp(self):
        """Set up test cases."""
        self.agent_force = Agentforce(username="test@example.com", password="password")

    def test_list_agents(self):
        """Test listing agents."""
        mock_response = {
            "records": [
                {"Id": "1", "Name": "Test Agent 1"},
                {"Id": "2", "Name": "Test Agent 2"}
            ]
        }
        
        with patch.object(self.agent_force, 'get', return_value=mock_response):
            agents = self.agent_force.list_agents()
            self.assertEqual(len(agents["records"]), 2)

    def test_send_message_to_agent(self):
        """Test sending a message to an agent."""
        # Test first message (no session ID)
        mock_response = [{
            'actionName': 'TestAgent5',
            'isSuccess': True,
            'outputValues': {
                'sessionId': 'fdd48ec7-8d97-4d3f-975b-d9f33bddd377',
                'agentResponse': '{"type":"Text","value":"Test response"}'
            }
        }]
        
        with patch.object(self.agent_force, 'post', return_value=mock_response):
            response = self.agent_force.send_message(
                agent_api_name="TestAgent5",
                user_message="Order number is 1234"
            )
            
            self.assertEqual(response['session_id'], 'fdd48ec7-8d97-4d3f-975b-d9f33bddd377')
            self.assertEqual(response['agent_response'], '{"type":"Text","value":"Test response"}')
            self.assertTrue(response['is_success'])
            
        # Test follow-up message (with session ID)
        mock_response_2 = [{
            'actionName': 'TestAgent5',
            'isSuccess': True,
            'outputValues': {
                'sessionId': 'new-session-id',
                'agentResponse': '{"type":"Text","value":"Follow-up response"}'
            }
        }]
        
        with patch.object(self.agent_force, 'post', return_value=mock_response_2):
            response = self.agent_force.send_message(
                agent_api_name="TestAgent5",
                user_message="What's the status?",
                session_id='fdd48ec7-8d97-4d3f-975b-d9f33bddd377'
            )
            
            self.assertEqual(response['session_id'], 'new-session-id')
            self.assertEqual(response['agent_response'], '{"type":"Text","value":"Follow-up response"}')
            self.assertTrue(response['is_success'])

    def test_deploy_agent(self):
        """Test deploying an agent."""
        mock_response = {
            'deployResult': {
                'status': 'Succeeded',
                'success': True
            }
        }
        
        with patch('agent_sdk.core.deploy_tools.deploy_zipfile.deploy_metadata_to_salesforce', return_value=mock_response):
            result = self.agent_force.deploy_agent(
                agent_name="TestAgent",
                zip_path="test.zip",
                bot_api_name="SampleBot"  # Using the new default bot name
            )
            self.assertTrue(result['deployResult']['success'])

    def test_deploy_agent_failure(self):
        """Test deploying an agent with failure."""
        mock_response = {
            'deployResult': {
                'status': 'Failed',
                'success': False,
                'details': {
                    'errors': [{'message': 'Test error'}]
                }
            }
        }
        
        with patch('agent_sdk.core.deploy_tools.deploy_zipfile.deploy_metadata_to_salesforce', return_value=mock_response):
            with self.assertRaises(AgentforceApiError):
                self.agent_force.deploy_agent(
                    agent_name="TestAgent",
                    zip_path="test.zip",
                    bot_api_name="SampleBot"
                ) 