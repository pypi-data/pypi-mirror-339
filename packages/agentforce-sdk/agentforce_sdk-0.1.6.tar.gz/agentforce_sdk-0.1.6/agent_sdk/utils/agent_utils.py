"""Utility class for AgentForce SDK."""

import os
import json
from typing import Dict, Any, List, Optional, Union
from ..models import Agent, Topic, Action, Variable, SystemMessage, Input, Output
import openai

class AgentUtils:
    """Utility class for agent-related operations."""

    @staticmethod
    def _generate_action_description(action_name: str) -> str:
        """Generate a default description for an action based on its name.
        
        Args:
            action_name (str): The name of the action
            
        Returns:
            str: A generated description for the action
        """
        # Convert camelCase to space-separated words
        words = []
        current_word = ""
        for char in action_name:
            if char.isupper() and current_word:
                words.append(current_word)
                current_word = char
            else:
                current_word += char
        words.append(current_word)
        
        # Join words and capitalize first letter
        description = " ".join(words).lower()
        return description[0].upper() + description[1:]

    @staticmethod
    def load_json(file_path: str) -> Dict[str, Any]:
        """Load a JSON file.
        
        Args:
            file_path (str): Path to the JSON file
            
        Returns:
            dict: Loaded JSON data
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            json.JSONDecodeError: If the file isn't valid JSON
        """
        with open(file_path, 'r') as f:
            return json.load(f)

    @staticmethod
    def save_json(file_path: str, data: Dict[str, Any], indent: int = 2) -> None:
        """Save data to a JSON file.
        
        Args:
            file_path (str): Path to save the file to
            data (dict): Data to save
            indent (int): Indentation level for the JSON output
            
        Raises:
            IOError: If the file can't be written
        """
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=indent)

    @staticmethod
    def create_agent_from_file(file_path: str) -> Agent:
        """Create an Agent instance from a JSON file.
        
        Args:
            file_path (str): Path to the JSON file containing agent configuration
            
        Returns:
            Agent: Created Agent instance
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            json.JSONDecodeError: If the file isn't valid JSON
            KeyError: If required fields are missing from the JSON
        """
        agent_config = AgentUtils.load_json(file_path)
        
        # Create the agent with required fields
        agent = Agent(
            name=agent_config['name'],
            description=agent_config['description'],
            agent_type=agent_config['agent_type'],
            company_name=agent_config['company_name']
        )
        
        # Set optional fields
        if 'sample_utterances' in agent_config:
            agent.sample_utterances = agent_config['sample_utterances']
        
        # Set system messages if present
        if 'system_messages' in agent_config:
            agent.system_messages = [
                SystemMessage(**msg) for msg in agent_config['system_messages']
            ]
        
        # Set variables if present
        if 'variables' in agent_config:
            agent.variables = [
                Variable(**var) for var in agent_config['variables']
            ]
        
        # Create topics if present
        if 'topics' in agent_config:
            topics = []
            for topic_data in agent_config['topics']:
                # Create topic
                topic = Topic(
                    name=topic_data['name'],
                    description=topic_data['description'],
                    scope=topic_data['scope']
                )
                
                # Set instructions if present
                if 'instructions' in topic_data:
                    topic.instructions = topic_data['instructions']
                
                # Create actions if present
                if 'actions' in topic_data:
                    actions = []
                    for action_data in topic_data['actions']:
                        # Convert example_output to proper Output format
                        example_output = action_data['example_output']
                        if isinstance(example_output, dict):
                            # Extract status and details from the example output
                            status = example_output.get('status', 'success')
                            # Remove status from details if it exists
                            details = example_output.copy()
                            details.pop('status', None)
                            output = Output(status=status, details=details)
                        else:
                            # If it's not a dict, create a simple success output
                            output = Output(status='success', details={'output': example_output})
                        
                        # Generate description if not provided
                        description = action_data.get('description', AgentUtils._generate_action_description(action_data['name']))
                        
                        action = Action(
                            name=action_data['name'],
                            description=description,
                            inputs=[Input(**input_data) for input_data in action_data['inputs']],
                            example_output=output
                        )
                        actions.append(action)
                    topic.actions = actions
                
                topics.append(topic)
            agent.topics = topics
        
        return agent

    @staticmethod
    def create_agent_directory_structure(base_dir: str, agent_data: Union[Dict[str, Any], str]) -> None:
        """Create a directory structure for an agent.
        
        This creates the following structure:
        - base_dir/
          - agent.json: Main agent configuration (without topics)
          - topics/
            - <topic_name>.json: Topic configuration (without actions)
            - <topic_name>/
              - actions/
                - <action_name>.json: Action configuration
                
        Args:
            base_dir (str): Base directory to create the structure in
            agent_data (Union[Dict[str, Any], str]): Either a dictionary with agent data or a path to a JSON file
        """
        # Handle string input (file path)
        if isinstance(agent_data, str):
            try:
                # If it's a path to a JSON file, load it
                agent_data = AgentUtils.load_json(agent_data)
            except Exception as e:
                raise ValueError(f"Failed to load agent data from {agent_data}: {str(e)}")
        
        # Create directories
        os.makedirs(base_dir, exist_ok=True)
        topics_dir = os.path.join(base_dir, 'topics')
        os.makedirs(topics_dir, exist_ok=True)
        
        # Copy agent data and remove topics
        agent_copy = agent_data.copy()
        topics = agent_copy.pop('topics', [])
        
        # Save agent.json
        agent_filename = os.path.basename(base_dir) + '.json' if os.path.basename(base_dir) else 'agent.json'
        AgentUtils.save_json(os.path.join(base_dir, agent_filename), agent_copy)
        
        # Process topics
        for topic in topics:
            # Check if topic is a dictionary or an object
            if isinstance(topic, dict):
                topic_name = topic['name'].lower().replace(' ', '_')
                topic_copy = topic.copy()
                actions = topic_copy.pop('actions', [])
            else:
                topic_name = topic.name.lower().replace(' ', '_')
                topic_copy = topic.__dict__.copy()
                actions = topic_copy.pop('actions', [])
            
            # Save topic json
            AgentUtils.save_json(os.path.join(topics_dir, f'{topic_name}.json'), topic_copy)
            
            # Process actions
            if actions:
                # Create actions directory
                actions_dir = os.path.join(topics_dir, topic_name, 'actions')
                os.makedirs(actions_dir, exist_ok=True)
                
                for action in actions:
                    # Check if action is a dictionary or an object
                    if isinstance(action, dict):
                        action_name = action['name'].lower().replace(' ', '_')
                        action_data = action
                    else:
                        action_name = action.name.lower().replace(' ', '_')
                        action_data = action.__dict__
                    
                    AgentUtils.save_json(os.path.join(actions_dir, f'{action_name}.json'), action_data)

    @staticmethod
    def create_agent_from_directory_structure(base_dir: str, agent_name: str) -> Agent:
        """Load an agent from a directory structure.
        
        This expects the following structure:
        - base_dir/
          - agent.json: Main agent configuration
          - topics/
            - <topic_name>.json: Topic configuration
            - <topic_name>/
              - actions/
                - <action_name>.json: Action configuration
                
        Returns:
            Agent: Created Agent instance
        """
        # Load agent.json
        agent_file = os.path.join(base_dir, f'{agent_name}.json')
        if not os.path.exists(agent_file):
            raise FileNotFoundError(f"Agent configuration file not found: {agent_file}")
        
        agent_data = AgentUtils.load_json(agent_file)
        
        # Initialize topics array if not present
        if 'topics' not in agent_data:
            agent_data['topics'] = []
        
        # Load topics
        topics_dir = os.path.join(base_dir, 'topics')
        if os.path.exists(topics_dir):
            topic_files = [f for f in os.listdir(topics_dir) if f.endswith('.json')]
            
            for topic_file in topic_files:
                topic_path = os.path.join(topics_dir, topic_file)
                if os.path.exists(topic_path):
                    topic_data = AgentUtils.load_json(topic_path)
                    
                    # Initialize actions array if not present
                    if 'actions' not in topic_data:
                        topic_data['actions'] = []
                    
                    # Load actions
                    topic_name = os.path.splitext(topic_file)[0]
                    actions_dir = os.path.join(topics_dir, topic_name, 'actions')
                    
                    if os.path.exists(actions_dir):
                        action_files = [f for f in os.listdir(actions_dir) if f.endswith('.json')]
                        
                        for action_file in action_files:
                            action_path = os.path.join(actions_dir, action_file)
                            if os.path.exists(action_path):
                                action_data = AgentUtils.load_json(action_path)
                                topic_data['actions'].append(action_data)
                    
                    # Add topic to agent
                    agent_data['topics'].append(topic_data)
        
        # Create agent from the collected data
        return AgentUtils.create_agent_from_dict(agent_data)
        
    @staticmethod
    def create_agent_from_dict(agent_data: Dict[str, Any]) -> Agent:
        """Create an Agent instance from a dictionary.
        
        Args:
            agent_data (Dict[str, Any]): Dictionary containing agent configuration
            
        Returns:
            Agent: Created Agent instance
        """
        # Create the agent with required fields
        agent = Agent(
            name=agent_data['name'],
            description=agent_data['description'],
            agent_type=agent_data['agent_type'],
            company_name=agent_data['company_name']
        )
        
        # Set optional fields
        if 'sample_utterances' in agent_data:
            agent.sample_utterances = agent_data['sample_utterances']
        
        # Set system messages if present
        if 'system_messages' in agent_data:
            agent.system_messages = [
                SystemMessage(**msg) for msg in agent_data['system_messages']
            ]
        
        # Set variables if present
        if 'variables' in agent_data:
            agent.variables = [
                Variable(**var) for var in agent_data['variables']
            ]
        
        # Create topics if present
        if 'topics' in agent_data:
            topics = []
            for topic_data in agent_data['topics']:
                # Create topic
                topic = Topic(
                    name=topic_data['name'],
                    description=topic_data['description'],
                    scope=topic_data['scope']
                )
                
                # Set instructions if present
                if 'instructions' in topic_data:
                    topic.instructions = topic_data['instructions']
                
                # Create actions if present
                if 'actions' in topic_data:
                    actions = []
                    for action_data in topic_data['actions']:
                        # Convert example_output to proper Output format
                        example_output = action_data['example_output']
                        if isinstance(example_output, dict):
                            # Extract status and details from the example output
                            status = example_output.get('status', 'success')
                            # Remove status from details if it exists
                            details = example_output.copy()
                            details.pop('status', None)
                            output = Output(status=status, details=details)
                        else:
                            # If it's not a dict, create a simple success output
                            output = Output(status='success', details={'output': example_output})
                        
                        # Generate description if not provided
                        description = action_data.get('description', AgentUtils._generate_action_description(action_data['name']))
                        
                        action = Action(
                            name=action_data['name'],
                            description=description,
                            inputs=[Input(**input_data) for input_data in action_data['inputs']],
                            example_output=output
                        )
                        actions.append(action)
                    topic.actions = actions
                
                topics.append(topic)
            agent.topics = topics
        
        return agent
        
    # Alias for clarity
    @staticmethod
    def create_agent_from_json_file(file_path: str) -> Agent:
        """Alias for create_agent_from_file. Creates an Agent instance from a JSON file.
        
        Args:
            file_path (str): Path to the JSON file containing agent configuration
            
        Returns:
            Agent: Created Agent instance
        """
        return AgentUtils.create_agent_from_file(file_path)

    @staticmethod
    def export_agent_to_modular_files(agent_data: Dict[str, Any], export_path: str) -> None:
        """Export an agent configuration to modular files.
        
        This creates the following structure:
        - export_path/
          - agents/
            - <agent_name>.json: Agent configuration (with topic references)
          - topics/
            - <topic_name>.json: Topic configuration (with action references)
          - actions/
            - <action_name>.json: Action configuration
        """
        # Create directories
        agents_dir = os.path.join(export_path, 'agents')
        topics_dir = os.path.join(export_path, 'topics')
        actions_dir = os.path.join(export_path, 'actions')
        
        os.makedirs(agents_dir, exist_ok=True)
        os.makedirs(topics_dir, exist_ok=True)
        os.makedirs(actions_dir, exist_ok=True)
        
        # Create a copy of the agent data
        agent_copy = agent_data.copy()
        
        # Create a list of topic references and copy topics
        agent_copy['topics'] = []
        topics = agent_copy.pop('topics', [])
        
        # Process each topic
        for topic in topics:
            topic_name = topic.name.lower().replace(' ', '_')
            agent_copy['topics'].append(topic_name)
            
            # Create a copy of the topic data
            topic_copy = topic.__dict__.copy()
            
            # Create a list of action references and copy actions
            topic_copy['actions'] = []
            actions = topic_copy.pop('actions', [])
            
            # Process each action
            for action in actions:
                action_name = action.name.lower().replace(' ', '_')
                topic_copy['actions'].append(action_name)
                
                # Add topic reference to the action
                action_copy = action.__dict__.copy()
                action_copy['topic'] = topic_name
                
                # Save action
                AgentUtils.save_json(os.path.join(actions_dir, f'{action_name}.json'), action_copy)
            
            # Save topic
            AgentUtils.save_json(os.path.join(topics_dir, f'{topic_name}.json'), topic_copy)
        
        # Save agent
        agent_name = agent_copy.get('agent_api_name', 'agent').lower().replace(' ', '_')
        AgentUtils.save_json(os.path.join(agents_dir, f'{agent_name}.json'), agent_copy)

    @staticmethod
    def create_agent_from_modular_files(base_dir: str, agent_name: str) -> Agent:
        """Create an agent from modular JSON files."""
        # Load agent configuration
        agent_config = AgentUtils.load_json(os.path.join(base_dir, 'agents', f'{agent_name}.json'))
        
        # Create the agent
        agent = Agent(
            name=agent_config['name'],
            description=agent_config['description'],
            agent_type=agent_config['agent_type'],
            company_name=agent_config['company_name']
        )
        
        # Set sample utterances
        agent.sample_utterances = agent_config['sample_utterances']
        
        # Set system messages
        agent.system_messages = [
            SystemMessage(**msg) for msg in agent_config['system_messages']
        ]
        
        # Set variables
        agent.variables = [
            Variable(**var) for var in agent_config['variables']
        ]
        
        # Load and create topics
        topics = []
        for topic_name in agent_config['topics']:
            topic_config = AgentUtils.load_json(os.path.join(base_dir, 'topics', f'{topic_name}.json'))
            
            # Create topic
            topic = Topic(
                name=topic_config['name'],
                description=topic_config['description'],
                scope=topic_config['scope']
            )
            
            # Set instructions
            topic.instructions = topic_config['instructions']
            
            # Load and set actions
            actions = []
            for action_name in topic_config['actions']:
                action_config = AgentUtils.load_json(os.path.join(base_dir, 'actions', f'{action_name}.json'))
                
                # Get description or generate one if not present
                description = action_config.get('description', AgentUtils._generate_action_description(action_config['name']))
                
                # Handle example_output to properly create Output object
                example_output = action_config['example_output']
                if isinstance(example_output, dict):
                    # Extract status and details from the example output
                    status = example_output.get('status', 'success')
                    # Remove status from details if it exists
                    details = example_output.copy()
                    details.pop('status', None)
                    output = Output(status=status, details=details)
                else:
                    # If it's not a dict, create a simple success output
                    output = Output(status='success', details={'output': example_output})
                
                # Create action
                action = Action(
                    name=action_config['name'],
                    description=description,
                    inputs=[Input(**input_data) for input_data in action_config['inputs']],
                    example_output=output
                )
                actions.append(action)
            
            topic.actions = actions
            topics.append(topic)
        
        # Set topics for the agent
        agent.topics = topics
        return agent

    @staticmethod
    def generate_agent_info(
        description: str,
        company_name: str,
        agent_name: str,
        output_dir: str,
        model: str = "gpt-4o"
    ) -> None:
        """Generate agent information in modular format using OpenAI.
        
        Args:
            description (str): Description of what the agent should do
            company_name (str): Name of the company
            agent_name (str): Name of the agent
            openai_api_key (str): OpenAI API key
            output_dir (str): Directory to save the generated files
            model (str): OpenAI model to use
            
        Returns:
            None
        """
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
        # System message to guide the LLM
        system_message = """You are an expert at creating AI agents. Your task is to generate a complete agent configuration 
        with topics and actions based on the description provided. The output should follow this structure:
        {
            "name": "agent name",
            "description": "agent description",
            "agent_type": "custom",
            "company_name": "company name",
            "sample_utterances": ["utterance1", "utterance2"],
            "topics": [
                {
                    "name": "TopicName",
                    "description": "topic description",
                    "scope": "topic scope",
                    "actions": [
                        {
                            "name": "actionName",
                            "description": "action description",
                            "inputs": [
                                {
                                    "name": "inputName",
                                    "description": "input description",
                                    "data_type": "String/Number/Boolean/etc",
                                    "required": true/false
                                }
                            ],
                            "outputs": [
                                {
                                    "name": "outputName",
                                    "description": "output description",
                                    "data_type": "String/Number/Boolean/etc",
                                    "required": true/false
                                }
                            ],
                            "example_output": {
                                "status": "success",
                                "outputName": "example value"
                            }
                        }
                    ]
                }
            ]
        }"""

        # User message with the agent requirements
        user_message = f"""Create a complete agent configuration for an agent with these details:
        Description: {description}
        Company Name: {company_name}
        Agent Name: {agent_name}
        
        Please ensure:
        1. All actions have meaningful inputs and outputs
        2. Example outputs match the defined output structure
        3. Data types are appropriate for each input/output
        4. Sample utterances are relevant to the agent's purpose
        5. Topics are logically organized
        6. All descriptions are clear and detailed"""

        # Call OpenAI API
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7
        )

        # Parse the response
        try:
            agent_data = json.loads(response.choices[0].message.content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse OpenAI response as JSON: {str(e)}")

        # Create the modular directory structure
        AgentUtils.export_agent_to_modular_files(agent_data, output_dir)
        print(f"Successfully generated agent information in {output_dir}") 