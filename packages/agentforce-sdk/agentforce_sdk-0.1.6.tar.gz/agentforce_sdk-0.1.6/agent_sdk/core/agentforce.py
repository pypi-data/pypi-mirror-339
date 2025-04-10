"""Agentforce main class for agent creation and deployment."""

import os
import json
import shutil
import zipfile
import time
import requests
import logging
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Union, Tuple
from pathlib import Path
import base64
from collections import defaultdict
import tempfile
from typing import Any
from datetime import datetime

from agent_sdk.core.auth import BaseAuth

from agent_sdk.core.base import AgentforceBase
from agent_sdk.models.agent import Agent
from agent_sdk.models.topic import Topic
from agent_sdk.models.action import Action, Input, Output
from agent_sdk.models.prompt_template import PromptTemplate, PromptInput
from agent_sdk.exceptions import MetadataDeploymentError, AgentforceApiError, AgentforceAuthError, ValidationError
from agent_sdk.config import Config
from agent_sdk.core.deploy_tools.generate_metadata import MetadataGenerator
from agent_sdk.core.deploy_tools.deploy_zipfile import deploy_and_monitor, deploy_metadata_to_salesforce
from openai import OpenAI
from simple_salesforce import Salesforce
from agent_sdk.core.prompt_template_utils import PromptTemplateUtils
from simple_salesforce.exceptions import SalesforceError
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(Config.get_log_level())

class Agentforce(AgentforceBase):
    """Main class for interacting with Salesforce and managing prompt templates."""
    
    DEFAULT_API_VERSION = Config.API_VERSION
    DEFAULT_POLLING_INTERVAL = Config.POLLING_INTERVAL
    DEFAULT_POLLING_RETRY_DELAY = Config.POLLING_RETRY_DELAY
    
    def __init__(self, auth: BaseAuth = None):
        """Initialize the Agentforce SDK.
        
        Args:
            auth (BaseAuth, optional): Authentication provider
        """
        super().__init__(auth)
        logger.info("Initializing Agentforce SDK")
        
        # Initialize session for connection pooling
        self.session = requests.Session()
        
        # Configure session with appropriate timeouts
        self.session.timeout = Config.REQUEST_TIMEOUT
        
        # Initialize PromptTemplateUtils after Salesforce connection is established
        self.prompt_template_utils = PromptTemplateUtils(self.sf)
        
        # Log environment info
        if Config.is_production():
            logger.info("Running in production environment")
        else:
            logger.info("Running in development environment")

    def create_apex_class(self, topic: Topic, action: Action, output_dir: str = None) -> str:
        """Create an Invocable Action Apex class based on topic and action information.
        
        Args:
            topic (Topic): The topic containing the action
            action (Action): The action to create an Apex class for
            output_dir (str, optional): Directory to save the Apex class. Defaults to current directory.
            
        Returns:
            str: Path to the created Apex class file
            
        Raises:
            ValidationError: If required information is missing
            MetadataDeploymentError: If class creation fails
        """
        logger.info(f"Creating Invocable Action Apex class for action: {action.name} in topic: {topic.name}")
        
        try:
            # Validate inputs
            if not topic.name or not action.name:
                raise ValidationError("Topic name and action name are required")

            class_dir_path = os.path.join(output_dir, 'classes')
            os.makedirs(class_dir_path, exist_ok=True)

            action_name = MetadataGenerator._sanitize_name(action.name)
            # Create sanitized names for the class
            class_name = action_name
            
            # Prepare input/output schema information
            input_fields = []
            for input_param in action.inputs:
                input_fields.append({
                    "name": input_param.name,
                    "type": input_param.data_type,
                    "description": input_param.description,
                    "required": input_param.required
                })
            
            # Convert example output to schema format
            output_fields = []
            if action.outputs:
                for output_param in action.inputs:
                    output_fields.append({
                        "name": output_param.name,
                        #"type": output_param.data_type,
                        "type": "string",
                        "description": output_param.description
                    })
            elif action.example_output:
                for key, value in action.example_output["details"].items():
                    print(key + " " + str(value))
                    output_fields.append({
                        "name": key,
                        "type": "string"
                    })

            
            # Prepare prompt for OpenAI to generate Apex class structure
            prompt = f"""Generate an Apex Invocable Action class with the following specifications:

Action Name: {action.name}
Action Description: {topic.description}.{action.description}

Input Parameters:
{json.dumps(input_fields, indent=2)}

Output Schema:
{json.dumps(output_fields, indent=2)}

Requirements:
1. Create an Invocable Action class that can be used in Salesforce Flow
2. Include proper input/output wrapper classes with @InvocableVariable annotations
3. Use appropriate Apex data types for the parameters
4. Include proper error handling and validation
5. Generate a test class with comprehensive test coverage
6. Follow Salesforce best practices for invocable actions
7. Use proper documentation and comments
8. Make sure the class is named correctly and uses {class_name} as the class name
9. Expand output schema with each output parameter and not the entire map.


Please provide the complete Apex class implementation."""
            # Call OpenAI API to generate the Apex class
            client = OpenAI()
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an expert Salesforce developer specializing in Apex invocable actions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,  # Lower temperature for more consistent output
                max_tokens=4000
            )
            
            # Extract the generated Apex code
            apex_code = response.choices[0].message.content
            
            # Clean up the code (remove markdown formatting if present)
            if "```apex" in apex_code:
                apex_code = apex_code.split("```apex")[1].split("```")[0].strip()
            elif "```java" in apex_code:
                apex_code = apex_code.split("```java")[1].split("```")[0].strip()
            elif "```" in apex_code:
                apex_code = apex_code.split("```")[1].split("```")[0].strip()
            
            # Create the Apex class file
            class_file_path = os.path.join(class_dir_path, f"{class_name}.cls")
            with open(class_file_path, 'w') as f:
                f.write(apex_code)
                
            # Create the meta XML file
            meta_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<ApexClass xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>{self.API_VERSION}</apiVersion>
    <status>Active</status>
    <description>{action.description}</description>
</ApexClass>'''
            
            meta_file_path = os.path.join(class_dir_path, f"{class_name}.cls-meta.xml")
            with open(meta_file_path, 'w') as f:
                f.write(meta_content)
                
            logger.info(f"Successfully created Invocable Action Apex class: {class_name}")
            return class_file_path
            
        except Exception as e:
            logger.error(f"Failed to create Apex class: {str(e)}")
            raise MetadataDeploymentError(f"Failed to create Apex class: {str(e)}")

    def deploy_agent(self, agent: Agent) -> Dict:
        """Deploy an agent to Salesforce.
        
        Args:
            agent (Agent): The agent to deploy
            deploy_via_api (bool): Flag to determine if metadata should be uploaded via API
        """
        return self.create(agent)

    def create(self, agent: Agent) -> Dict:
        """Deploy an agent to Salesforce.
        
        Args:
            agent (Agent): The agent to deploy
            deploy_via_api (bool): Flag to determine if metadata should be uploaded via API
            
        Returns:
            Dict: Response from Salesforce containing deployment status
            
        Raises:
            AgentforceAuthError: If authentication to Salesforce fails
            MetadataDeploymentError: If deployment to Salesforce fails
            ValidationError: If agent data is invalid
        """
        logger.info(f"Deploying agent: {agent.name}")
        
        try:
            # Validate agent data
            if not agent.name:
                raise ValidationError("Agent name is required")
            
            # Check authentication
            self._check_auth()
            
            # Create deployment directory
            deployment_dir = Config.get_deployment_dir()
            os.makedirs(deployment_dir, exist_ok=True)
            
            # Create a specific directory for this deployment using timestamp
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            agent_name = agent.name.replace(' ', '_')
            temp_dir = os.path.join(deployment_dir, f"{agent_name}_{timestamp}")
            os.makedirs(temp_dir, exist_ok=True)
            
            # Get the template directories
            core_dir = os.path.dirname(os.path.abspath(__file__))
            templates_dir = os.path.join(core_dir, 'templates')
            
            # Fallback to project root if templates not in core
            if not os.path.exists(templates_dir):
                templates_dir = os.path.join(os.getcwd(), 'templates')
                if not os.path.exists(templates_dir):
                    raise MetadataDeploymentError(f"Templates directory not found at: {templates_dir}")
            
            # Create metadata output directory
            metadata_dir = os.path.join(temp_dir, 'metadata')
            os.makedirs(metadata_dir, exist_ok=True)

            # Generate metadata
            try:
                metadata_generator = MetadataGenerator(template_dir=templates_dir, base_output_dir=metadata_dir)
                agent_data = agent.to_dict()
                logger.info("Generating metadata files...")
                metadata_generator.generate_agent_metadata(
                    input_json=agent_data,
                    site_url=agent.domain or '',
                    company_name=agent.company_name or 'Salesforce',
                    bot_api_name=agent.name,
                    bot_username=None,
                    session_id=self.session_id,
                    instance_url=self.instance_url,
                    asa_agent=agent.agent_type.lower() == 'internal'
                )
                logger.info("Metadata generation completed successfully")
            except Exception as e:
                logger.error(f"Failed to generate metadata: {str(e)}")
                raise MetadataDeploymentError(f"Failed to generate metadata: {str(e)}")
            
            # Create zip file for deployment
            zip_filename = f"{agent_name}_{timestamp}.zip"
            zip_path = os.path.join(Config.DEPLOYMENT_DIR, zip_filename)
            try:
                logger.info("Creating deployment zip file...")
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root, dirs, files in os.walk(metadata_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, metadata_dir)
                            logger.debug(f"Adding to zip: {arcname}")
                            zipf.write(file_path, arcname)
                logger.info("Deployment zip file created successfully")
            except Exception as e:
                logger.error(f"Failed to create deployment zip file: {str(e)}")
                raise MetadataDeploymentError(f"Failed to create deployment zip file: {str(e)}")
            
            # Deploy to Salesforce
            try:
                logger.info("Initiating deployment to Salesforce...")
                self._check_auth()
                response = deploy_and_monitor(
                    session=self.session,
                    zip_path=zip_path,
                    agent_name=MetadataGenerator._sanitize_name(agent.name),
                    instance_url=self.instance_url,
                    session_id=self.session_id,
                    check_auth_callback=lambda: self._check_auth()
                )
                
                logger.info("Deployment started successfully")
                return response
                
            except Exception as e:
                logger.error(f"Failed to deploy to Salesforce: {str(e)}")
                raise MetadataDeploymentError(f"Failed to deploy to Salesforce: {str(e)}")
                
        except Exception as e:
            logger.warning(f"Failed to deploy agent: {str(e)}")
    
    def is_agent_created(self, agent_api_name: str, max_retries: int = None, initial_retry_delay: int = None, 
                      max_retry_delay: int = None) -> Optional[Dict]:
        """Poll the Salesforce org for the agent with the given API name.
        
        Args:
            agent_api_name (str): The API name of the agent to check for
            max_retries (int, optional): Maximum number of retries. Defaults to DEFAULT_MAX_RETRIES.
            initial_retry_delay (int, optional): Initial delay between retries in seconds.
                                               Defaults to DEFAULT_RETRY_DELAY.
            max_retry_delay (int, optional): Maximum delay between retries in seconds.
                                           Defaults to MAX_RETRY_DELAY.
            
        Returns:
            Optional[Dict]: The agent record if found, None otherwise
        """
        # Use provided values or defaults from Config
        max_retries = max_retries or self.DEFAULT_MAX_RETRIES
        initial_retry_delay = initial_retry_delay or self.DEFAULT_RETRY_DELAY
        max_retry_delay = max_retry_delay or Config.MAX_RETRY_DELAY
        agent_api_name = MetadataGenerator._sanitize_name(agent_api_name)
        retry_delay = initial_retry_delay
        
        for attempt in range(max_retries):
            try:
                # Query for the agent
                result = self.sf.query(
                    f"SELECT Id, DeveloperName FROM BotDefinition WHERE DeveloperName = '{agent_api_name}'"
                )
                
                if result['records']:
                    logger.info(f"Found agent: {agent_api_name}")
                    return result['records'][0]
                
                logger.info(f"Agent not found yet. Attempt {attempt + 1} of {max_retries}")
                
            except Exception as e:
                logger.error(f"Error querying for agent: {str(e)}")
                # Don't raise here to allow for retries
                time.sleep(retry_delay)
            
            # Implement exponential backoff with a maximum delay
            retry_delay = min(retry_delay * 1.5, max_retry_delay)
            time.sleep(retry_delay)
        
        logger.warning(f"Agent not found after {max_retries} attempts")
        return None
    
    def list_agents(self) -> List[Dict]:
        """List all deployed agents.
        
        Returns:
            list: List of agents in the org
            
        Raises:
            AgentforceAuthError: If authentication to Salesforce fails
            AgentforceApiError: If querying Salesforce fails
        """
        try:
            self._check_auth()
        except Exception as e:
            logger.error(f"Authentication check failed: {str(e)}")
            raise AgentforceAuthError(f"Failed to authenticate to Salesforce: {str(e)}")
        
        # Query the Salesforce API for deployed agents
        try:
            logger.info("Querying for deployed agents")
            agents = self.sf.query("SELECT Id, DeveloperName, MasterLabel, Description FROM GenAIAgent__c")
            logger.info(f"Found {len(agents.get('records', []))} agents")
            return agents.get('records', [])
        except Exception as e:
            logger.error(f"Error listing agents: {str(e)}")
            raise AgentforceApiError(f"Failed to list agents: {str(e)}")
    
    def get_agent(self, agent_id: str) -> Dict:
        """Get an agent by ID.
        
        Args:
            agent_id (str): The ID of the agent
            
        Returns:
            Dict: Agent data
            
        Raises:
            AgentforceAuthError: If authentication to Salesforce fails
        """
        self._check_auth()
        return self.sf.GenAIAgent__c.get(agent_id)
    
    def send_message(self, agent_name: str, user_message: str, session_id: str = None) -> Dict:
        """Send a message to an agent and get the response.
        
        Args:
            agent_name (str): The API name of the agent to send the message to
            user_message (str): The message to send to the agent
            session_id (str, optional): Session ID for continuing a conversation. Defaults to None.
            
        Returns:
            Dict: The agent's response containing the message and new session ID
            
        Raises:
            AgentforceAuthError: If authentication to Salesforce fails
            AgentforceApiError: If the API call fails
        """
        try:
            self._check_auth()
            
            # Prepare the request body
            request_body = {
                "inputs": [{
                    "sessionId": session_id,
                    "userMessage": user_message
                }]
            }
            agent_name = MetadataGenerator._sanitize_name(agent_name)
            # Make the API call
            url = f"actions/custom/generateAiAgentResponse/{agent_name}"
            response = self.post(url, data=request_body)
            
            if not response or not isinstance(response, list) or not response[0].get('outputValues'):
                raise AgentforceApiError("Invalid response format from agent")
                
            output_values = response[0]['outputValues']
            return {
                'session_id': output_values.get('sessionId'),
                'agent_response': output_values.get('agentResponse'),
                'is_success': response[0].get('isSuccess', False)
            }
            
        except Exception as e:
            logger.error(f"Failed to send message to agent: {str(e)}")
            raise AgentforceApiError(f"Failed to send message to agent: {str(e)}")
    
    def export_agent_from_salesforce(self, agent_name: str, output_dir: str) -> str:
        """Export a Salesforce agent to modular agent format.
        
        Args:
            agent_name (str): Name of the Salesforce bot/agent to export
            output_dir (str): Directory to save the exported agent
            
        Returns:
            str: Path to the output directory
            
        Raises:
            MetadataDeploymentError: If metadata retrieval or conversion fails
            ValidationError: If agent not found
        """
        logger.info(f"Exporting Salesforce agent '{agent_name}' to modular format")
        
        try:
            # Create output directory
            os.makedirs(output_dir, exist_ok=True)
            
            # Retrieve the bot metadata
            bot_metadata = self.retrieve_metadata(agent_name)
            if not bot_metadata or not bot_metadata.get("records"):
                raise ValidationError(f"Bot '{agent_name}' not found in Salesforce")
            
            # Convert metadata directly to modular agent format
            agent_data = self._convert_metadata_to_agent(bot_metadata)
            
            # Create agent directory with sanitized name
            agent_name_sanitized = MetadataGenerator._sanitize_name(agent_data["name"]).lower()
            agent_dir = os.path.join(output_dir, agent_name_sanitized)
            os.makedirs(agent_dir, exist_ok=True)
            
            # Save agent.json (e.g., order_management_agent.json)
            agent_file = os.path.join(agent_dir, f"{agent_name_sanitized}.json")
            with open(agent_file, 'w') as f:
                json.dump({
                    "name": agent_data["name"],
                    "description": agent_data["description"],
                    "agent_type": "custom",
                    "company_name": agent_data.get("company_name", ""),
                    "sample_utterances": agent_data.get("sample_utterances", [])
                }, f, indent=2)
            
            # Create topics directory
            topics_dir = os.path.join(agent_dir, "topics")
            os.makedirs(topics_dir, exist_ok=True)
            
            # Save topics and actions
            for topic in agent_data.get("topics", []):
                topic_name = MetadataGenerator._sanitize_name(topic["name"]).lower()
                
                # Create topic directory
                topic_dir = os.path.join(topics_dir, topic_name)
                os.makedirs(topic_dir, exist_ok=True)
                
                # Save topic.json in topics directory
                topic_file = os.path.join(topics_dir, f"{topic_name}.json")
                with open(topic_file, 'w') as f:
                    json.dump({
                        "name": topic["name"],
                        "description": topic["description"],
                        "scope": topic.get("scope", topic["description"]),
                        "instructions": topic.get("instructions", [])
                    }, f, indent=2)
                
                # Create actions directory
                actions_dir = os.path.join(topic_dir, "actions")
                os.makedirs(actions_dir, exist_ok=True)
                
                # Save actions
                for action in topic.get("actions", []):
                    action_name = MetadataGenerator._sanitize_name(action["name"]).lower()
                    action_file = os.path.join(actions_dir, f"{action_name}.json")
                    
                    # Format action data
                    action_data = {
                        "name": action["name"],
                        "description": action["description"],
                        "inputs": action["inputs"],
                        "outputs": action["outputs"],
                        "example_output": action["example_output"]
                    }
                    
                    with open(action_file, 'w') as f:
                        json.dump(action_data, f, indent=2)
            
            logger.info(f"Successfully exported agent to modular format in: {agent_dir}")
            return agent_dir
            
        except Exception as e:
            logger.error(f"Failed to export agent: {str(e)}")
            raise MetadataDeploymentError(f"Failed to export agent: {str(e)}")
            
    def _convert_metadata_to_agent(self, metadata: Dict) -> Dict:
        """Convert Salesforce metadata to agent format.
        
        Args:
            metadata (Dict): Metadata retrieved from Salesforce
            
        Returns:
            Dict: Agent data in the required format
        """
        agent_data = {
            "name": "Salesforce Agent",
            "description": "Agent generated from Salesforce metadata",
            "agent_type": "",
            "company_name": "",
            "sample_utterances": [],
            "topics": []
        }
        
        # Process Bot metadata
        if metadata.get("records"):
            bot = metadata["records"][0]
            agent_data["name"] = bot.get("MasterLabel", "Salesforce Agent")
            agent_data["description"] = bot.get("Description", "")
            agent_data["agent_template_type"] = bot.get("AgentType", "")
            agent_data["agent_type"] = bot.get("Type", "").replace("Copilot", "")

        
        # Extract all the related metadata
        related_data = metadata.get("related", {})
        
        # Create lookup maps for easier reference
        function_map = {f["Id"]: f for f in related_data.get("GenAiFunctionDefinition", [])}
        
        plugin_instruction_map = {}
        for instruction in related_data.get("GenAiPluginInstruction", []):
            plugin_id = instruction.get("GenAiPluginDefinitionId", "")
            if plugin_id not in plugin_instruction_map:
                plugin_instruction_map[plugin_id] = []
            plugin_instruction_map[plugin_id].append(instruction)
        
        plugin_function_map = {}
        for pf in related_data.get("GenAiPluginFunction", []):
            plugin_id = pf.get("PluginId", "")
            if plugin_id not in plugin_function_map:
                plugin_function_map[plugin_id] = []
            plugin_function_map[plugin_id].append(pf)
        
        # Process plugins (topics)
        for plugin in related_data.get("GenAiPlugin", []):
            topic = {
                "name": plugin.get("MasterLabel", plugin.get("DeveloperName", "Unknown Topic")),
                "description": plugin.get("Description", ""),
                "scope": plugin.get("Scope", ""),
                "instructions": [],
                "actions": []
            }
            
            # Add instructions to topic if available
            plugin_id = plugin.get("Id")
            if plugin_id in plugin_instruction_map:
                instructions = plugin_instruction_map[plugin_id]
                for instruction in instructions:
                    topic["instructions"].append(instruction.get("Description", ""))
            
            # Add actions associated with this topic
            if plugin_id in plugin_function_map:
                for plugin_function in plugin_function_map[plugin_id]:
                    function_id = plugin_function.get("Function") or plugin_function.get("FunctionId")
                    if function_id in function_map:
                        function = function_map[function_id]
                        
                        action = {
                            "name": function.get("MasterLabel", function.get("DeveloperName", "Unknown Action")),
                            "description": function.get("Description", ""),
                            "inputs": [],
                            "outputs": [],
                            "example_output": {
                                "status": "success"
                            }
                        }
                        
                        # Parse input parameters
                        input_params_str = function.get("InputParameters")
                        if input_params_str:
                            try:
                                input_params = json.loads(input_params_str)
                                for param in input_params:
                                    action["inputs"].append({
                                        "name": param["name"],
                                        "description": param.get("description", ""),
                                        "data_type": param.get("type", "String"),
                                        "required": param.get("required", True)
                                    })
                            except json.JSONDecodeError:
                                logger.warning(f"Could not parse InputParameters for function {function.get('DeveloperName')}")
                        
                        # Parse output parameters
                        output_params_str = function.get("OutputParameters")
                        if output_params_str:
                            try:
                                output_params = json.loads(output_params_str)
                                for param in output_params:
                                    action["outputs"].append({
                                        "name": param["name"],
                                        "description": param.get("description", ""),
                                        "data_type": param.get("type", "String"),
                                        "required": param.get("required", True)
                                    })
                                    # Add to example output
                                    action["example_output"][param["name"]] = ""
                            except json.JSONDecodeError:
                                logger.warning(f"Could not parse OutputParameters for function {function.get('DeveloperName')}")
                        
                        topic["actions"].append(action)
            
            # Only add topics that have actions
            if topic["actions"]:
                agent_data["topics"].append(topic)
        
        return agent_data
    
    def retrieve_metadata(self, agent_name: str = None) -> Dict:
        """Retrieve metadata from Salesforce using direct queries.
        
        Args:
            agent_name (str, optional): Name of the agent to filter by
            
        Returns:
            Dict: Retrieved metadata
        """
        try:
            # Ensure we have a valid session
            self._check_auth()
            
            # Initialize our results container
            result = {"records": []}
            
            # Get sf instance that we can use for queries
            sf = Salesforce(instance_url=self.instance_url, session_id=self.session_id, version="63.0")
            
            # Define SOQL queries for each metadata type
        
            # First query the Bot to get basic info and ID
            bot_query = f"SELECT Id, AgentType, AgentTemplate, DeveloperName, MasterLabel, Type FROM BotDefinition"
            if agent_name:
                bot_query += f" WHERE MasterLabel = '{agent_name}' OR DeveloperName = '{agent_name}'"
            
            bot_result = sf.query_all(bot_query)
            logger.debug(f"Bot query returned {len(bot_result.get('records', []))} records")
            
            if not bot_result.get('records'):
                return {"records": []}
            
            # Get the Bot ID for further queries
            bot_id = bot_result['records'][0]['Id']
            bot_records = bot_result['records']
            bot_developer_name = bot_result['records'][0]['DeveloperName']
            
            # Get associated BotVersions
            version_query = f"SELECT Id, BotDefinitionId, VersionNumber FROM BotVersion WHERE BotDefinitionId = '{bot_id}' ORDER BY VersionNumber DESC"
            version_result = sf.query_all(version_query)
            logger.debug(f"BotVersion query returned {len(version_result.get('records', []))} records")
            bot_version_id = version_result['records'][0]['VersionNumber']
            # Get associated GenAiPlanner
            planner_query = f"SELECT Id, DeveloperName FROM GenAiPlannerDefinition WHERE DeveloperName = '{bot_developer_name}_v{bot_version_id}'"
            planner_result = sf.query_all(planner_query)
            logger.debug(f"GenAiPlanner query returned {len(planner_result.get('records', []))} records")
            
            planner_ids = [record['Id'] for record in planner_result.get('records', [])]
            
            # Get associated GenAiPlannerFunction linking to GenAiFunctionDefinition
            if planner_ids:
                planner_plugin_ids = ",".join([f"'{pid}'" for pid in planner_ids])
                planner_plugin_query = f"SELECT Plugin FROM GenAiPlannerFunctionDef WHERE PlannerId IN ({planner_plugin_ids})"
                planner_plugin_result = sf.query_all(planner_plugin_query)
                logger.debug(f"GenAiPlannerFunction query returned {len(planner_plugin_result.get('records', []))} records")
                
                # Get all the plugin IDs
                plugin_ids = [record['Plugin'] for record in planner_plugin_result.get('records', [])]
                
                # Get details of all associated functions
                if plugin_ids:
                    plugin_ids_str = ",".join([f"'{fid}'" for fid in plugin_ids])
                    plugin_function_query = f"SELECT PluginId, Function FROM GenAiPluginFunctionDef WHERE PluginId IN ({plugin_ids_str})"
                    plugin_function_result = sf.query_all(plugin_function_query)
                    function_ids = [record['Function'] for record in plugin_function_result.get('records', [])]
                    logger.debug(f"GenAiPluginFunctionDef query returned {len(plugin_function_result.get('records', []))} records")
                    function_ids_str = ",".join([f"'{fid}'" for fid in function_ids])
            
                    # Get associated GenAiPluginDefinition
                    plugin_query = f"SELECT Id, DeveloperName, MasterLabel, Description, Scope FROM GenAiPluginDefinition WHERE Id IN ({plugin_ids_str})"
                    plugin_result = sf.query_all(plugin_query)
                    logger.debug(f"GenAiPlugin query returned {len(plugin_result.get('records', []))} records")
                    
                    # Get plugin instructions
                    plugin_instr_query = f"SELECT Id, GenAiPluginDefinitionId, DeveloperName, Description, MasterLabel FROM GenAiPluginInstructionDef WHERE GenAiPluginDefinitionId IN ({plugin_ids_str})"
                    plugin_instr_result = sf.query_all(plugin_instr_query)
                    logger.debug(f"GenAiPluginInstruction query returned {len(plugin_instr_result.get('records', []))} records")
                    
                    # Get associated GenAiFunctionDefinition
                    function_query = f"SELECT Id, DeveloperName, MasterLabel, Description FROM GenAiFunctionDefinition WHERE Id IN ({function_ids_str})"
                    function_result = sf.query_all(function_query)
                    logger.debug(f"GenAiFunctionDefinition query returned {len(function_result.get('records', []))} records")
            
            # Combine all results into a comprehensive response
            return {
                "records": bot_records,
                "related": {
                    "GenAiPlugin": plugin_result.get('records', []) if 'plugin_result' in locals() else [],
                    "GenAiPluginInstruction": plugin_instr_result.get('records', []) if 'plugin_instr_result' in locals() else [],
                    "GenAiPluginFunction": plugin_function_result.get('records', []) if 'plugin_function_result' in locals() else [],
                    "GenAiFunctionDefinition": function_result.get('records', []) if 'function_result' in locals() else []
                }
            }
        except Exception as e:
            logger.error(f"Failed to retrieve metadata: {str(e)}")
            raise AgentforceApiError(f"Failed to retrieve metadata: {str(e)}")
    
    def check_deploy_status(self, deployment_id: str) -> Dict[str, Any]:
        """Check the status of a metadata deployment.
        
        Args:
            deployment_id (str): The deployment ID to check
            
        Returns:
            Dict[str, Any]: Dictionary containing deployment status information
            
        Raises:
            AgentforceApiError: If status check fails
        """
        try:
            status = self.sf.check_deploy_status(deployment_id)
            return {
                'id': deployment_id,
                'done': status['done'],
                'success': status['success'],
                'status': status['status'],
                'errors': status.get('details', {}).get('componentFailures', []),
                'error_message': status.get('errorMessage', '')
            }
        except Exception as e:
            logger.error(f"Failed to check deployment status: {str(e)}")
            raise AgentforceApiError(f"Failed to check deployment status: {str(e)}")
    
    def create_prompt_template_metadata(self, template_path: str, output_dir: str = None, deploy: bool = False) -> Dict[str, Any]:
        """Create metadata files for a prompt template and optionally deploy to Salesforce.
        
        Args:
            template_path (str): Path to the prompt template JSON file
            output_dir (str, optional): Directory to save metadata files. If not provided, uses a temp directory.
            deploy (bool, optional): Whether to deploy the metadata to Salesforce. Defaults to False.
            
        Returns:
            Dict[str, Any]: Dictionary containing metadata file paths and deployment status if deployed
            
        Raises:
            ValidationError: If required information is missing
            AgentforceApiError: If metadata generation fails
            MetadataDeploymentError: If deployment fails
        """
        try:
            # Load the template
            template = self.prompt_template_utils.load_template(template_path)
            if not template:
                raise ValidationError("Failed to load template from provided path")
            
            # Validate template has required fields
            if not template.name:
                raise ValidationError("Template must have a name")
            
            # Create output directory if not provided
            if not output_dir:
                output_dir = os.path.join(os.getcwd(), 'metadata')
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate metadata files
            metadata_generator = MetadataGenerator()
            metadata_files = metadata_generator.generate_prompt_template_metadata(
                template=template,
                output_dir=output_dir
            )
            
            if not metadata_files:
                raise AgentforceApiError("No metadata files were generated")
            
            result = {
                'metadata_dir': output_dir,
                'files': metadata_files
            }
            
            # Deploy if requested
            if deploy:
                try:
                    # Ensure we have a valid session before deploying
                    self._check_auth()
                    
                    # Create deployment zip
                    zip_filename = f"{template.name}_{int(time.time())}.zip"
                    zip_path = os.path.join(output_dir, zip_filename)
                    
                    logger.info(f"Creating deployment zip file at: {zip_path}")
                    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                        for root, _, files in os.walk(output_dir):
                            for file in files:
                                file_path = os.path.join(root, file)
                                arcname = os.path.relpath(file_path, output_dir)
                                logger.debug(f"Adding to zip: {arcname}")
                                zipf.write(file_path, arcname)
                    
                    if not os.path.exists(zip_path):
                        raise MetadataDeploymentError("Failed to create deployment zip file")
                    
                    # Deploy metadata to Salesforce
                    logger.info("Initiating deployment to Salesforce...")
                    deployment_result = deploy_metadata_to_salesforce(
                        zip_path=zip_path,
                        agent_name=template.name,
                        instance_url=self.instance_url,
                        session_id=self.session_id,
                        check_auth_callback=lambda: self._check_auth()
                    )
                    
                    if not deployment_result:
                        raise MetadataDeploymentError("No deployment result returned from Salesforce")
                    
                    # Add deployment info to result
                    result.update({
                        'deployment_id': deployment_result.get('id'),
                        'deployment_done': deployment_result.get('done', False),
                        'deployment_success': deployment_result.get('success', False),
                        'deployment_status': deployment_result.get('status', 'Unknown'),
                        'deployment_errors': deployment_result.get('errors', []),
                        'deployment_error_message': deployment_result.get('error_message', '')
                    })
                    
                    # Check deployment status
                    if not deployment_result.get('id'):
                        raise MetadataDeploymentError("No deployment ID returned from Salesforce")
                        
                    if not deployment_result.get('success', False) or deployment_result.get('status') == 'SucceededPartial':
                        error_msg = deployment_result.get('error_message')
                        if not error_msg:
                            errors = deployment_result.get('errors', [])
                            if errors:
                                error_msg = f"Partial success with errors: {'; '.join([str(err) for err in errors])}"
                            else:
                                error_msg = f"Deployment status was '{deployment_result.get('status', 'Unknown')}' but reported as success: {deployment_result.get('id')}"
                        
                        # Add specific message for partial success
                        if deployment_result.get('status') == 'SucceededPartial':
                           error_msg = f"Deployment partially succeeded with failures: {error_msg}"

                        raise MetadataDeploymentError(f"Failed to deploy metadata: {error_msg}")
                        
                    logger.info(f"Successfully deployed prompt template metadata: {deployment_result.get('id')}")
                    
                except Exception as e:
                    logger.error(f"Failed to deploy metadata: {str(e)}")
                    raise MetadataDeploymentError(f"Failed to deploy metadata: {str(e)}")
                finally:
                    # Clean up zip file
                    if 'zip_path' in locals() and os.path.exists(zip_path):
                        try:
                            os.remove(zip_path)
                        except Exception as e:
                            logger.warning(f"Failed to clean up deployment zip file: {str(e)}")
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to create prompt template metadata: {str(e)}")
            raise AgentforceApiError(f"Failed to create prompt template metadata: {str(e)}")
    