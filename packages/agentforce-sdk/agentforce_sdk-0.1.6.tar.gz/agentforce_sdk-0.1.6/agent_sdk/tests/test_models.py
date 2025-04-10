"""Tests for AgentForce SDK models."""

import unittest
from unittest.mock import MagicMock, patch
import json
import os
import sys

# Add the parent directory to sys.path if needed for testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from ..models.agent import Agent
from ..models.topic import Topic
from ..models.action import Action, Input
from ..models.variable import Variable
from ..models.system_message import SystemMessage
from ..models.output import Output

from .utils import SAMPLE_AGENT_DATA

class TestAgent(unittest.TestCase):
    """Tests for the Agent model."""
    
    def setUp(self):
        """Set up test cases."""
        self.agent = Agent(
            name="TestAgent",
            description="Test agent for unit tests",
            agent_type="Internal",
            company_name="Test Company"
        )
    
    def test_init(self):
        """Test Agent initialization."""
        self.assertEqual(self.agent.name, "TestAgent")
        self.assertEqual(self.agent.description, "Test agent for unit tests")
        self.assertEqual(self.agent.agent_type, "Internal")
        self.assertEqual(self.agent.company_name, "Test Company")
        self.assertEqual(len(self.agent.sample_utterances), 0)
        self.assertEqual(len(self.agent.variables), 0)
        self.assertEqual(len(self.agent.system_messages), 0)
        self.assertEqual(len(self.agent.topics), 0)
    
    def test_setters(self):
        """Test Agent property setters."""
        self.agent.name = "UpdatedTestAgent"
        self.assertEqual(self.agent.name, "UpdatedTestAgent")
        
        self.agent.description = "Updated description"
        self.agent.agent_type = "External"
        self.agent.company_name = "Updated Company"
        
        self.assertEqual(self.agent.description, "Updated description")
        self.assertEqual(self.agent.agent_type, "External")
        self.assertEqual(self.agent.company_name, "Updated Company")
    
    def test_sample_utterances(self):
        """Test setting sample utterances."""
        utterances = ["First utterance", "Second utterance"]
        self.agent.sample_utterances = utterances
        self.assertEqual(len(self.agent.sample_utterances), 2)
        self.assertEqual(self.agent.sample_utterances, utterances)
    
    def test_system_messages(self):
        """Test setting system messages."""
        messages = [
            SystemMessage(message="Welcome message", msg_type="WELCOME"),
            SystemMessage(message="Error message", msg_type="ERROR")
        ]
        self.agent.system_messages = messages
        self.assertEqual(len(self.agent.system_messages), 2)
        self.assertEqual(self.agent.system_messages, messages)
    
    def test_variables(self):
        """Test setting variables."""
        variables = [
            Variable(name="var1", data_type="string", default_value="val1"),
            Variable(name="var2", data_type="number", default_value=42)
        ]
        self.agent.variables = variables
        self.assertEqual(len(self.agent.variables), 2)
        self.assertEqual(self.agent.variables, variables)
    
    def test_topics(self):
        """Test setting topics."""
        topics = [
            Topic(name="Topic1", description="First topic", scope="public"),
            Topic(name="Topic2", description="Second topic", scope="public")
        ]
        self.agent.topics = topics
        self.assertEqual(len(self.agent.topics), 2)
        self.assertEqual(self.agent.topics, topics)
    
    def test_to_dict(self):
        """Test converting agent to dictionary."""
        # Set up test data
        self.agent.sample_utterances = ["test utterance"]
        self.agent.system_messages = [SystemMessage(message="test", msg_type="system")]
        self.agent.variables = [Variable(name="test", data_type="string")]
        self.agent.topics = [Topic(name="test", description="test", scope="public")]
        
        agent_dict = self.agent.to_dict()
        self.assertEqual(agent_dict["name"], self.agent.name)
        self.assertEqual(agent_dict["description"], self.agent.description)
        self.assertEqual(agent_dict["agent_type"], self.agent.agent_type)
        self.assertEqual(agent_dict["company_name"], self.agent.company_name)
        self.assertEqual(len(agent_dict["sample_utterances"]), 1)
        self.assertEqual(len(agent_dict["system_messages"]), 1)
        self.assertEqual(len(agent_dict["variables"]), 1)
        self.assertEqual(len(agent_dict["topics"]), 1)
    
    def test_to_json(self):
        """Test converting agent to JSON."""
        agent_json = self.agent.to_json()
        agent_dict = json.loads(agent_json)
        self.assertEqual(agent_dict["name"], self.agent.name)
        self.assertEqual(agent_dict["description"], self.agent.description)
    
    def test_save_to_file(self):
        """Test saving agent to a file."""
        with unittest.mock.patch("builtins.open", unittest.mock.mock_open()) as mock_file:
            self.agent.save_to_file("test_agent.json")
            mock_file.assert_called_once_with("test_agent.json", "w")
            handle = mock_file()
            handle.write.assert_called()
    
    @patch("agent_sdk.models.agent.Deployment")
    def test_create(self, mock_deployment):
        """Test creating an agent."""
        mock_deployment.return_value = "deployment_result"
        self.client.deploy_agent.return_value = {"status": "Succeeded"}
        
        result = self.agent.create()
        
        self.client.deploy_agent.assert_called_once_with(self.agent)
        self.assertEqual(result, "deployment_result")

class TestTopic(unittest.TestCase):
    """Tests for the Topic model."""
    
    def setUp(self):
        """Set up test cases."""
        self.topic = Topic(
            name="Test Topic",
            description="A topic for testing",
            scope="Test scope"
        )
    
    def test_init(self):
        """Test Topic initialization."""
        self.assertEqual(self.topic.name, "Test Topic")
        self.assertEqual(self.topic.description, "A topic for testing")
        self.assertEqual(self.topic.scope, "Test scope")
        self.assertEqual(len(self.topic.instructions), 0)
        self.assertEqual(len(self.topic.actions), 0)
    
    def test_setters(self):
        """Test Topic property setters."""
        self.topic.name = "Updated Topic"
        self.topic.description = "Updated description"
        self.topic.scope = "Updated scope"
        
        self.assertEqual(self.topic.name, "Updated Topic")
        self.assertEqual(self.topic.description, "Updated description")
        self.assertEqual(self.topic.scope, "Updated scope")
    
    def test_instructions(self):
        """Test setting instructions."""
        instructions = ["Instruction 1", "Instruction 2"]
        self.topic.instructions = instructions
        self.assertEqual(len(self.topic.instructions), 2)
        self.assertEqual(self.topic.instructions, instructions)
    
    def test_actions(self):
        """Test setting actions."""
        actions = [
            Action(
                name="Action1",
                inputs=[Input(name="input1", description="test", data_type="string")],
                example_output=Output(status="success", details={})
            )
        ]
        self.topic.actions = actions
        self.assertEqual(len(self.topic.actions), 1)
        self.assertEqual(self.topic.actions, actions)
    
    def test_to_dict(self):
        """Test converting topic to dictionary."""
        # Set up test data
        self.topic.instructions = ["test instruction"]
        self.topic.actions = [
            Action(
                name="test_action",
                inputs=[Input(name="test_input", description="test", data_type="string")],
                example_output=Output(status="success", details={})
            )
        ]
        
        topic_dict = self.topic.to_dict()
        self.assertEqual(topic_dict["name"], self.topic.name)
        self.assertEqual(topic_dict["description"], self.topic.description)
        self.assertEqual(topic_dict["scope"], self.topic.scope)
        self.assertEqual(len(topic_dict["instructions"]), 1)
        self.assertEqual(len(topic_dict["actions"]), 1)

class TestAction(unittest.TestCase):
    """Tests for the Action model."""
    
    def setUp(self):
        """Set up test cases."""
        self.action = Action(
            name="testAction",
            inputs=[
                Input(name="testInput", description="Test input", data_type="string")
            ],
            example_output=Output(status="success", details={})
        )
    
    def test_init(self):
        """Test Action initialization."""
        self.assertEqual(self.action.name, "testAction")
        self.assertEqual(len(self.action.inputs), 1)
        self.assertEqual(self.action.example_output.status, "success")
    
    def test_setters(self):
        """Test Action property setters."""
        self.action.name = "updatedAction"
        self.assertEqual(self.action.name, "updatedAction")
    
    def test_inputs(self):
        """Test setting inputs."""
        inputs = [
            Input(name="input1", description="First input", data_type="string"),
            Input(name="input2", description="Second input", data_type="number")
        ]
        self.action.inputs = inputs
        self.assertEqual(len(self.action.inputs), 2)
        self.assertEqual(self.action.inputs, inputs)
    
    def test_example_output(self):
        """Test setting example output."""
        output = Output(status="success", details={"key": "value"})
        self.action.example_output = output
        self.assertEqual(self.action.example_output.status, "success")
        self.assertEqual(self.action.example_output.details, {"key": "value"})
    
    def test_to_dict(self):
        """Test converting action to dictionary."""
        action_dict = self.action.to_dict()
        self.assertEqual(action_dict["name"], self.action.name)
        self.assertEqual(len(action_dict["inputs"]), 1)
        self.assertEqual(action_dict["example_output"]["status"], "success")

class TestInput(unittest.TestCase):
    """Tests for the Input model."""
    
    def setUp(self):
        """Set up test cases."""
        self.input = Input(
            name="testInput",
            description="Test input description",
            data_type="string",
            required=True
        )
    
    def test_init(self):
        """Test Input initialization."""
        self.assertEqual(self.input.name, "testInput")
        self.assertEqual(self.input.description, "Test input description")
        self.assertEqual(self.input.data_type, "string")
        self.assertTrue(self.input.required)
    
    def test_setters(self):
        """Test Input property setters."""
        self.input.name = "updatedInput"
        self.input.description = "Updated description"
        self.input.data_type = "number"
        self.input.required = False
        
        self.assertEqual(self.input.name, "updatedInput")
        self.assertEqual(self.input.description, "Updated description")
        self.assertEqual(self.input.data_type, "number")
        self.assertFalse(self.input.required)
    
    def test_to_dict(self):
        """Test converting input to dictionary."""
        input_dict = self.input.to_dict()
        self.assertEqual(input_dict["name"], self.input.name)
        self.assertEqual(input_dict["description"], self.input.description)
        self.assertEqual(input_dict["data_type"], self.input.data_type)
        self.assertTrue(input_dict["required"])
    
    def test_from_dict(self):
        """Test creating input from dictionary."""
        input_dict = {
            "name": "dictInput",
            "description": "Dictionary input description",
            "data_type": "boolean",
            "required": False
        }
        input_obj = Input.from_dict(input_dict)
        
        self.assertIsInstance(input_obj, Input)
        self.assertEqual(input_obj.name, "dictInput")
        self.assertEqual(input_obj.description, "Dictionary input description")
        self.assertEqual(input_obj.data_type, "boolean")
        self.assertFalse(input_obj.required)

class TestOutput(unittest.TestCase):
    """Tests for the Output model."""
    
    def setUp(self):
        """Set up test cases."""
        self.output = Output(
            status="success",
            details={"key": "value"}
        )
    
    def test_init(self):
        """Test Output initialization."""
        self.assertEqual(self.output.status, "success")
        self.assertEqual(self.output.details, {"key": "value"})
    
    def test_setters(self):
        """Test Output property setters."""
        self.output.status = "error"
        self.output.details = {"error": "message"}
        
        self.assertEqual(self.output.status, "error")
        self.assertEqual(self.output.details, {"error": "message"})
    
    def test_to_dict(self):
        """Test converting output to dictionary."""
        output_dict = self.output.to_dict()
        self.assertEqual(output_dict["status"], "success")
        self.assertEqual(output_dict["details"], {"key": "value"})
    
    def test_from_dict(self):
        """Test creating output from dictionary."""
        output_dict = {
            "status": "error",
            "details": {"error": "message"}
        }
        output_obj = Output.from_dict(output_dict)
        
        self.assertIsInstance(output_obj, Output)
        self.assertEqual(output_obj.status, "error")
        self.assertEqual(output_obj.details, {"error": "message"})


if __name__ == "__main__":
    unittest.main() 