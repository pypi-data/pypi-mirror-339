"""
REST API Server for AgentForce SDK
--------------------------------------------------------
This module provides a simple server that allows the SDK to be accessed via a network interface.
"""

import json
import logging
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Dict, Any, Optional, Type, List, Tuple

from agent_sdk import Agentforce
from agent_sdk.core.auth import BasicAuth, DirectAuth
from agent_sdk.models import Agent, Topic, Action, Input, Output, SystemMessage, Variable
from agent_sdk.utils.agent_utils import AgentUtils

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('mcp_server')

class AgentforceServer:
    """
    A server that exposes Agentforce SDK functionality over HTTP.
    """
    
    def __init__(self, 
                 host: str = 'localhost', 
                 port: int = 8000, 
                 auth_token: Optional[str] = None,
                 debug: bool = False):
        """
        Initialize the server.
        
        Args:
            host: The host to bind to
            port: The port to listen on
            auth_token: Optional authentication token for securing the API
            debug: Enable debug logging
        """
        self.host = host
        self.port = port
        self.auth_token = auth_token or os.environ.get('AGENTFORCE_API_TOKEN')
        self.debug = debug
        self.server = None
        self.thread = None
        self.clients: Dict[str, Agentforce] = {}
        
        if debug:
            logger.setLevel(logging.DEBUG)
    
    def start(self):
        """Start the server in a background thread."""
        if self.server:
            logger.warning("Server is already running")
            return
        
        handler = self._create_request_handler()
        self.server = ThreadingHTTPServer((self.host, self.port), handler)
        
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.daemon = True
        self.thread.start()
        
        logger.info(f"AgentForce MCP Server started on http://{self.host}:{self.port}")
    
    def stop(self):
        """Stop the server."""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.server = None
            self.thread = None
            logger.info("AgentForce Server stopped")
    
    def _create_request_handler(self) -> Type[BaseHTTPRequestHandler]:
        """Create a request handler class with access to the server instance."""
        server_instance = self
        
        class RequestHandler(BaseHTTPRequestHandler):
            def _send_response(self, status_code: int, data: Dict[str, Any] = None):
                self.send_response(status_code)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                
                if data is not None:
                    self.wfile.write(json.dumps(data).encode('utf-8'))
            
            def _send_error(self, status_code: int, message: str):
                self._send_response(status_code, {"error": message})
            
            def _parse_json_body(self) -> Dict[str, Any]:
                content_length = int(self.headers.get('Content-Length', 0))
                if content_length == 0:
                    return {}
                
                body = self.rfile.read(content_length).decode('utf-8')
                try:
                    return json.loads(body)
                except json.JSONDecodeError:
                    self._send_error(400, "Invalid JSON body")
                    return {}
            
            def _validate_auth(self) -> bool:
                if not server_instance.auth_token:
                    return True
                
                auth_header = self.headers.get('Authorization', '')
                if not auth_header.startswith('Bearer '):
                    self._send_error(401, "Authentication required")
                    return False
                
                token = auth_header[7:]  # Remove 'Bearer ' prefix
                if token != server_instance.auth_token:
                    self._send_error(401, "Invalid authentication token")
                    return False
                
                return True
            
            def _get_client(self, params: Dict[str, Any]) -> Optional[Agentforce]:
                client_id = params.get('client_id')
                if client_id and client_id in server_instance.clients:
                    return server_instance.clients[client_id]
                
                # Create a new client if credentials are provided
                if 'username' in params and 'password' in params:
                    auth = BasicAuth(
                        username=params['username'],
                        password=params['password']
                    )
                    client = Agentforce(auth=auth)
                    
                    # Generate a client ID if not provided
                    if not client_id:
                        import uuid
                        client_id = str(uuid.uuid4())
                    
                    server_instance.clients[client_id] = client
                    return client
                
                if 'session_id' in params and 'instance_url' in params:
                    auth: DirectAuth = DirectAuth(
                        session_id=params['session_id'],
                        instance_url=params['instance_url']
                    )
                    client = Agentforce(auth=auth)
                    
                    # Generate a client ID if not provided
                    if not client_id:
                        import uuid
                        client_id = str(uuid.uuid4())
                    
                    server_instance.clients[client_id] = client
                    return client
                
                self._send_error(400, "No valid authentication method provided")
                return None
            
            def _build_agent_from_json(self, data: Dict[str, Any]) -> Agent:
                """Build an Agent object from JSON data."""
                if 'agent_dict' in data:
                    # Use from_dict if a full agent dictionary is provided
                    return Agent.from_dict(data['agent_dict'])
                
                # Otherwise, construct from individual fields
                agent = Agent(
                    name=data.get('name', ''),
                    description=data.get('description', ''),
                    agent_type=data.get('agent_type', 'External'),
                    agent_template_type=data.get('agent_template_type', 'Einstein'),
                    company_name=data.get('company_name', 'Salesforce')
                )
                
                # Add optional fields if present
                if 'sample_utterances' in data:
                    agent.sample_utterances = data['sample_utterances']
                
                # Add topics if present
                if 'topics' in data:
                    for topic_data in data['topics']:
                        topic = Topic(
                            name=topic_data.get('name', ''),
                            description=topic_data.get('description', ''),
                            scope=topic_data.get('scope', '')
                        )
                        
                        # Add instructions if present
                        if 'instructions' in topic_data:
                            topic.instructions = topic_data['instructions']
                        
                        # Add actions if present
                        if 'actions' in topic_data:
                            for action_data in topic_data['actions']:
                                action = Action(
                                    name=action_data.get('name', ''),
                                    description=action_data.get('description', '')
                                )
                                
                                # Add inputs if present
                                if 'inputs' in action_data:
                                    for input_data in action_data['inputs']:
                                        input_obj = Input(
                                            name=input_data.get('name', ''),
                                            description=input_data.get('description', ''),
                                            data_type=input_data.get('data_type', 'String'),
                                            required=input_data.get('required', False)
                                        )
                                        action.add_input(input_obj)
                                
                                # Add example output if present
                                if 'example_output' in action_data:
                                    action.example_output = action_data['example_output']
                                
                                topic.add_action(action)
                        
                        agent.add_topic(topic)
                
                # Add system messages if present
                if 'system_messages' in data:
                    for msg_data in data['system_messages']:
                        msg = SystemMessage(
                            content=msg_data.get('content', ''),
                            name=msg_data.get('name', ''),
                            msg_type=msg_data.get('msg_type', 'system')
                        )
                        agent.add_system_message(msg)
                
                # Add variables if present
                if 'variables' in data:
                    for var_data in data['variables']:
                        var = Variable(
                            name=var_data.get('name', ''),
                            data_type=var_data.get('data_type', 'String'),
                            default_value=var_data.get('default_value', ''),
                            var_type=var_data.get('var_type', 'custom')
                        )
                        agent.add_variable(var)
                
                return agent
            
            def do_GET(self):
                """Handle GET requests."""
                if not self._validate_auth():
                    return
                
                # Basic route handling
                if self.path == '/':
                    self._send_response(200, {
                        "name": "AgentForce MCP Server",
                        "version": "0.1.0",
                        "status": "running"
                    })
                    return
                
                if self.path == '/health':
                    self._send_response(200, {"status": "ok"})
                    return
                
                # Route not found
                self._send_error(404, f"Route not found: {self.path}")
            
            def do_POST(self):
                """Handle POST requests."""
                if not self._validate_auth():
                    return
                
                # Parse the request body
                params = self._parse_json_body()
                
                # Route handling for agent operations
                if self.path == '/create':
                    client = self._get_client(params)
                    if not client:
                        return
                    
                    try:
                        agent = self._build_agent_from_json(params)
                        result = client.create(agent)
                        self._send_response(200, {
                            "status": "success",
                            "result": result,
                            "client_id": params.get('client_id', list(server_instance.clients.keys())[-1])
                        })
                    except Exception as e:
                        logger.error(f"Error creating agent: {str(e)}", exc_info=server_instance.debug)
                        self._send_error(500, f"Error creating agent: {str(e)}")
                
                elif self.path == '/retrieve':
                    client = self._get_client(params)
                    if not client:
                        return
                    
                    try:
                        agent_id = params.get('agent_id')
                        if not agent_id:
                            self._send_error(400, "Missing agent_id parameter")
                            return
                        
                        result = client.retrieve(agent_id)
                        self._send_response(200, {
                            "status": "success",
                            "agent": result,
                            "client_id": params.get('client_id', list(server_instance.clients.keys())[-1])
                        })
                    except Exception as e:
                        logger.error(f"Error retrieving agent: {str(e)}", exc_info=server_instance.debug)
                        self._send_error(500, f"Error retrieving agent: {str(e)}")
                
                elif self.path == '/update':
                    client = self._get_client(params)
                    if not client:
                        return
                    
                    try:
                        agent = self._build_agent_from_json(params)
                        result = client.update(agent)
                        self._send_response(200, {
                            "status": "success",
                            "result": result,
                            "client_id": params.get('client_id', list(server_instance.clients.keys())[-1])
                        })
                    except Exception as e:
                        logger.error(f"Error updating agent: {str(e)}", exc_info=server_instance.debug)
                        self._send_error(500, f"Error updating agent: {str(e)}")
                
                elif self.path == '/delete':
                    client = self._get_client(params)
                    if not client:
                        return
                    
                    try:
                        agent_id = params.get('agent_id')
                        if not agent_id:
                            self._send_error(400, "Missing agent_id parameter")
                            return
                        
                        result = client.delete(agent_id)
                        self._send_response(200, {
                            "status": "success",
                            "result": result,
                            "client_id": params.get('client_id', list(server_instance.clients.keys())[-1])
                        })
                    except Exception as e:
                        logger.error(f"Error deleting agent: {str(e)}", exc_info=server_instance.debug)
                        self._send_error(500, f"Error deleting agent: {str(e)}")
                
                elif self.path == '/run':
                    client = self._get_client(params)
                    if not client:
                        return
                    
                    try:
                        agent_id = params.get('agent_id')
                        input_text = params.get('input_text')
                        
                        if not agent_id:
                            self._send_error(400, "Missing agent_id parameter")
                            return
                        
                        if not input_text:
                            self._send_error(400, "Missing input_text parameter")
                            return
                        
                        result = client.run(agent_id, input_text)
                        self._send_response(200, {
                            "status": "success",
                            "result": result,
                            "client_id": params.get('client_id', list(server_instance.clients.keys())[-1])
                        })
                    except Exception as e:
                        logger.error(f"Error running agent: {str(e)}", exc_info=server_instance.debug)
                        self._send_error(500, f"Error running agent: {str(e)}")
                
                elif self.path == '/export':
                    client = self._get_client(params)
                    if not client:
                        return
                    
                    try:
                        agent_id = params.get('agent_id')
                        export_path = params.get('export_path')
                        
                        if not agent_id:
                            self._send_error(400, "Missing agent_id parameter")
                            return
                        
                        result = client.export(agent_id, export_path)
                        self._send_response(200, {
                            "status": "success",
                            "result": result,
                            "client_id": params.get('client_id', list(server_instance.clients.keys())[-1])
                        })
                    except Exception as e:
                        logger.error(f"Error exporting agent: {str(e)}", exc_info=server_instance.debug)
                        self._send_error(500, f"Error exporting agent: {str(e)}")
                
                elif self.path == '/import':
                    client = self._get_client(params)
                    if not client:
                        return
                    
                    try:
                        agent_path = params.get('agent_path')
                        
                        if not agent_path:
                            self._send_error(400, "Missing agent_path parameter")
                            return
                        
                        result = client.import_agent(agent_path)
                        self._send_response(200, {
                            "status": "success",
                            "result": result,
                            "client_id": params.get('client_id', list(server_instance.clients.keys())[-1])
                        })
                    except Exception as e:
                        logger.error(f"Error importing agent: {str(e)}", exc_info=server_instance.debug)
                        self._send_error(500, f"Error importing agent: {str(e)}")
                
                elif self.path == '/retrieve_metadata':
                    client = self._get_client(params)
                    if not client:
                        return
                    
                    try:
                        metadata_type = params.get('metadata_type')
                        agent_name = params.get('agent_name')
                        
                        if not metadata_type:
                            self._send_error(400, "Missing metadata_type parameter")
                            return
                        
                        result = client.retrieve_metadata(metadata_type, agent_name)
                        self._send_response(200, {
                            "status": "success",
                            "result": result,
                            "client_id": params.get('client_id', list(server_instance.clients.keys())[-1])
                        })
                    except Exception as e:
                        logger.error(f"Error retrieving metadata: {str(e)}", exc_info=server_instance.debug)
                        self._send_error(500, f"Error retrieving metadata: {str(e)}")
                
                else:
                    # Route not found
                    self._send_error(404, f"Route not found: {self.path}")
        
        return RequestHandler

def start_server(host: str = 'localhost', port: int = 8000, auth_token: Optional[str] = None, debug: bool = False):
    """
    Start the AgentForce MCP server.
    
    Args:
        host: The host to bind to
        port: The port to listen on
        auth_token: Optional authentication token for securing the API
        debug: Enable debug logging
    
    Returns:
        The server instance
    """
    server = AgentforceServer(host, port, auth_token, debug)
    server.start()
    return server

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Start the AgentForce MCP server')
    parser.add_argument('--host', default='localhost', help='Host to bind to')
    parser.add_argument('--port', type=int, default=8000, help='Port to listen on')
    parser.add_argument('--token', help='Authentication token for securing the API')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    
    args = parser.parse_args()
    
    server = start_server(args.host, args.port, args.token, args.debug)
    
    try:
        # Keep the main thread alive
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down server...")
        server.stop()

def main():
    """
    Main entry point for the console script.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Start the AgentForce API server')
    parser.add_argument('--host', default='localhost', help='Host to bind to')
    parser.add_argument('--port', type=int, default=8000, help='Port to listen on')
    parser.add_argument('--token', help='Authentication token for securing the API')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    
    args = parser.parse_args()
    
    server = start_server(args.host, args.port, args.token, args.debug)
    
    print(f"AgentForce REST API Server started on http://{args.host}:{args.port}")
    print("Press Ctrl+C to stop the server")
    
    try:
        # Keep the main thread alive
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down server...")
        server.stop() 