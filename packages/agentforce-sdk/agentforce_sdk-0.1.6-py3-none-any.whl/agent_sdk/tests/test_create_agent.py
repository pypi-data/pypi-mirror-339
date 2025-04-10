"""Integration tests demonstrating agent creation functionality."""

import os
import sys
from agent_sdk.core.agentforce import Agentforce
from agent_sdk.models.agent import Agent
from agent_sdk.models.topic import Topic
from agent_sdk.models.action import Action, Input, Output
from agent_sdk.models.variable import Variable
from agent_sdk.models.system_message import SystemMessage

def create_basic_agent():
    """Demonstrate creating an agent with basic configuration."""
    # Initialize AgentForce client
    agent_force = Agentforce()
    
    # Create the agent
    agent = Agent(
        name="TestAgent",
        description="Test agent for integration tests",
        agent_type="External",
        company_name="Test Company"
    )
    
    # Create the agent in Salesforce
    result = agent.create()
    print(f"Basic agent creation result: {result}")

def create_agent_with_topics():
    """Demonstrate creating an agent with topics."""
    # Initialize AgentForce client
    agent_force = Agentforce()
    
    # Create the agent
    agent = Agent(
        name="TopicTestAgent",
        description="Agent with topics for integration tests",
        agent_type="External",
        company_name="Test Company"
    )
    
    # Create a topic
    topic = Topic(
        name="Test Topic",
        description="Test topic description",
        scope="public"
    )
    
    # Set topic instructions
    topic.instructions = ["Test instruction 1", "Test instruction 2"]
    
    # Create an action for the topic
    action = Action(
        name="Test Action",
        inputs=[
            Input(name="test_input", description="Test input", data_type="String", required=True)
        ],
        example_output=Output(status="success", details={"message": "Test output"})
    )
    
    # Set the action for the topic
    topic.actions = [action]
    
    # Add the topic to the agent
    agent.topics = [topic]
    
    # Create the agent in Salesforce
    result = agent.create()
    print(f"Agent with topics creation result: {result}")

def create_agent_with_variables():
    """Demonstrate creating an agent with variables."""
    # Initialize AgentForce client
    agent_force = Agentforce()
    
    # Create the agent
    agent = Agent(
        name="VariableTestAgent",
        description="Agent with variables for integration tests",
        agent_type="External",
        company_name="Test Company"
    )
    
    # Add variables to the agent
    agent.variables = [
        Variable(name="var1", data_type="String"),
        Variable(name="var2", data_type="Number")
    ]
    
    # Create the agent in Salesforce
    result = agent.create()
    print(f"Agent with variables creation result: {result}")

def create_agent_with_system_messages():
    """Demonstrate creating an agent with system messages."""
    # Initialize AgentForce client
    agent_force = Agentforce()
    
    # Create the agent
    agent = Agent(
        name="MessageTestAgent",
        description="Agent with system messages for integration tests",
        agent_type="External",
        company_name="Test Company"
    )
    
    # Add system messages to the agent
    agent.system_messages = [
        SystemMessage(message="Test message 1", msg_type="system"),
        SystemMessage(message="Test message 2", msg_type="system")
    ]
    
    # Create the agent in Salesforce
    result = agent.create()
    print(f"Agent with system messages creation result: {result}")

def create_agent_with_sample_utterances():
    """Demonstrate creating an agent with sample utterances."""
    # Initialize AgentForce client
    agent_force = Agentforce()
    
    # Create the agent
    agent = Agent(
        name="UtteranceTestAgent",
        description="Agent with sample utterances for integration tests",
        agent_type="External",
        company_name="Test Company"
    )
    
    # Add sample utterances to the agent
    agent.sample_utterances = [
        "Test utterance 1",
        "Test utterance 2",
        "Test utterance 3"
    ]
    
    # Create the agent in Salesforce
    result = agent.create()
    print(f"Agent with sample utterances creation result: {result}")

def create_agent_with_complete_config():
    """Demonstrate creating an agent with complete configuration."""
    # Initialize AgentForce client
    agent_force = Agentforce()
    
    # Create the agent
    agent = Agent(
        name="CompleteTestAgent",
        description="Agent with complete configuration for integration tests",
        agent_type="External",
        company_name="Test Company"
    )
    
    # Add all components to the agent
    agent.topics = [
        Topic(
            name="Test Topic",
            description="Test topic description",
            scope="public",
            instructions=["Test instruction"],
            actions=[
                Action(
                    name="Test Action",
                    inputs=[Input(name="test_input", description="Test input", data_type="String", required=True)],
                    example_output=Output(status="success", details={"message": "Test output"})
                )
            ]
        )
    ]
    
    agent.variables = [Variable(name="var1", data_type="String")]
    agent.system_messages = [SystemMessage(message="Test message", msg_type="system")]
    agent.sample_utterances = ["Test utterance"]
    
    # Create the agent in Salesforce
    result = agent.create()
    print(f"Complete agent creation result: {result}")

if __name__ == "__main__":
    # Run all integration tests
    print("Running integration tests for agent creation...")
    
    print("\n1. Testing basic agent creation...")
    create_basic_agent()
    
    print("\n2. Testing agent creation with topics...")
    create_agent_with_topics()
    
    print("\n3. Testing agent creation with variables...")
    create_agent_with_variables()
    
    print("\n4. Testing agent creation with system messages...")
    create_agent_with_system_messages()
    
    print("\n5. Testing agent creation with sample utterances...")
    create_agent_with_sample_utterances()
    
    print("\n6. Testing agent creation with complete configuration...")
    create_agent_with_complete_config()
    
    print("\nIntegration tests completed.") 