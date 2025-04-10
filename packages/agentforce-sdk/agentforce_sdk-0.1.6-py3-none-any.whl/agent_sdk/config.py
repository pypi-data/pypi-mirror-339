"""Configuration settings for the Agentforce SDK."""

import os
import logging
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class Config:
    """Configuration settings for the Agentforce SDK."""
    
    # API versions and endpoints
    API_VERSION = "v63.0"
    API_ENDPOINT = "https://asa-metadata-upload-4cd530090dac.herokuapp.com/deploy_agent"
    
    # Retry settings
    MAX_RETRIES = 30
    RETRY_DELAY = 5
    POLLING_MAX_RETRIES = 20
    POLLING_RETRY_DELAY = 15
    MAX_RETRY_DELAY = 60
    POLLING_INTERVAL = 10  # Interval between polling attempts in seconds
    
    # Connection settings
    REQUEST_TIMEOUT = 30
    
    # Deployment settings
    DEPLOYMENT_DIR = "agentforce_deployments"
    
    # Environment settings
    ENV = os.environ.get("AGENTFORCE_ENV", "development")
    
    @classmethod
    def get_auth_token(cls) -> str:
        """Get the API authentication token from environment or default.
        
        Returns:
            str: API authentication token
        """
        return os.environ.get(
            "AGENTFORCE_API_AUTH_TOKEN", 
            "zZUrgDeRPH1ewhboQHThPlrLjeuwB2tSS+AK2q0dFnirqdfFfTThQq8vKArjp4kcRAuAadnJfveH+2+v2ONA5w=="
        )
    
    @classmethod
    def get_api_endpoint(cls) -> str:
        """Get the API endpoint from environment or default.
        
        Returns:
            str: API endpoint
        """
        return os.environ.get("AGENTFORCE_API_ENDPOINT", cls.API_ENDPOINT)
    
    @classmethod
    def get_default_agent_id(cls) -> str:
        """Get the default agent ID from environment or default.
        
        Returns:
            str: Default agent ID
        """
        return os.environ.get("AGENTFORCE_DEFAULT_AGENT_ID", "a004W00000oXNDKQA4")
    
    @classmethod
    def get_deployment_dir(cls) -> str:
        """Get the deployment directory from environment or default.
        
        Returns:
            str: Deployment directory
        """
        return os.environ.get("AGENTFORCE_DEPLOYMENT_DIR", cls.DEPLOYMENT_DIR)
    
    @classmethod
    def is_production(cls) -> bool:
        """Check if the environment is production.
        
        Returns:
            bool: True if production, False otherwise
        """
        return cls.ENV.lower() == "production"
    
    @classmethod
    def get_log_level(cls) -> int:
        """Get the log level based on environment.
        
        Returns:
            int: Log level
        """
        if cls.is_production():
            return logging.WARNING
        return logging.INFO 