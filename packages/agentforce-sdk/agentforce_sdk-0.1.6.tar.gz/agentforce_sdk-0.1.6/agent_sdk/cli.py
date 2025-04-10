"""Command line interface for AgentForce SDK."""

import os
import sys
import click
import json
import logging
from pathlib import Path

from .models import Agent
from . import Agentforce
from .core.auth import BasicAuth
from .utils.agent_utils import AgentUtils
from .exceptions import AgentforceAuthError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@click.group()
def cli():
    """AgentForce SDK command line interface.
    
    Use this CLI to create, deploy, and manage agents on Salesforce.
    """
    pass

@cli.command()
@click.option('--username', '-u', required=True, help='Salesforce username')
@click.option('--password', '-p', required=True, help='Salesforce password')
@click.option('--agent-file', '-f', help='Path to agent JSON file')
@click.option('--agent-name', '-n', help='Name of the agent of the agent json file')
@click.option('--agent-dir', '-d', help='Path to agent directory (for modular files)')
@click.option('--deploy', is_flag=True, help='Deploy the agent to Salesforce')
def create(username, password, agent_file, agent_name, agent_dir, deploy):
    """Create an agent from a file or directory."""
    if not agent_file and not agent_dir:
        click.echo("Error: Either --agent-file or --agent-dir must be provided.")
        sys.exit(1)
        
    if agent_file and agent_dir:
        click.echo("Error: Cannot provide both --agent-file and --agent-dir.")
        sys.exit(1)
        
    # Initialize the client
    client = Agentforce(auth=BasicAuth(username=username, password=password))
    
    try:
        # Create agent from file or directory
        if agent_file:
            click.echo(f"Creating agent from file: {agent_file}")
            with open(agent_file, 'r') as f:
                agent_data = json.load(f)
            agent = Agent.from_dict(agent_data)
        else:
            click.echo(f"Creating agent from directory: {agent_dir}")
            agent = AgentUtils.create_agent_from_modular_files(base_dir =agent_dir, agent_name = agent_name)
            
        # Print agent details
        click.echo(f"Agent Name: {agent.name}")
        click.echo(f"Agent Type: {agent.agent_type}")
        click.echo(f"Topics: {len(agent.topics)}")
        
        # Deploy if requested
        if deploy:
            click.echo("Deploying agent to Salesforce...")
            result = client.create(agent)
            if result:
                click.echo(f"Agent deployed successfully: {result}")
            else:
                click.echo("Agent deployment failed.")
                sys.exit(1)
    
    except AgentforceAuthError as e:
        click.echo(f"Authentication error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error creating agent: {str(e)}")
        sys.exit(1)

@cli.command()
@click.option('--username', '-u', required=True, help='Salesforce username')
@click.option('--password', '-p', required=True, help='Salesforce password')
@click.option('--agent-name', '-n', required=True, help='Agent name to chat with')
@click.option('--message', '-m', required=True, help='Message to send to the agent')
@click.option('--session-id', '-s', help='Session ID for continuing a conversation')
def chat(username, password, agent_name, message, session_id):
    """Send a message to an agent."""
    # Initialize the client
    client = Agentforce(auth=BasicAuth(username=username, password=password))
    
    try:
        # Send message to agent
        click.echo(f"Sending message to agent '{agent_name}': {message}")
        response = client.send_message(
            agent_name=agent_name,
            user_message=message,
            session_id=session_id
        )
        
        # Print response
        click.echo(f"\nAgent response: {response['agent_response']}")
        click.echo(f"Session ID: {response['session_id']}")
    
    except AgentforceAuthError as e:
        click.echo(f"Authentication error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error sending message: {str(e)}")
        sys.exit(1)

@cli.command()
@click.option('--username', '-u', required=True, help='Salesforce username')
@click.option('--password', '-p', required=True, help='Salesforce password')
def list_agents(username, password):
    """List all agents in the Salesforce org."""
    # Initialize the client
    client = Agentforce(auth=BasicAuth(username=username, password=password))
    
    try:
        # List agents
        agents = client.list_agents()
        
        # Print agent details
        click.echo(f"Found {len(agents)} agents:")
        for agent in agents:
            click.echo(f"- {agent['MasterLabel']} (API Name: {agent['DeveloperName']})")
    
    except AgentforceAuthError as e:
        click.echo(f"Authentication error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error listing agents: {str(e)}")
        sys.exit(1)

def main():
    """Main entry point for the CLI."""
    cli()

if __name__ == '__main__':
    main() 