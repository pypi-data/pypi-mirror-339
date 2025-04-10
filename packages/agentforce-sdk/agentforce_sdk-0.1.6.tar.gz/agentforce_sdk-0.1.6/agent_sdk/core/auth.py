"""Authentication flows for the Agentforce SDK.

This module provides different authentication flows for Salesforce:
- SOAP Login (username/password)
- OAuth 2.0 Client Credentials Flow
- OAuth 2.0 JWT Bearer Flow
- Direct Auth (session ID and instance URL)

All flows use the simple-salesforce library's SalesforceLogin function.
"""

from typing import Optional, Tuple
from abc import ABC, abstractmethod
from simple_salesforce import SalesforceLogin

class BaseAuth(ABC):
    """Base class for authentication flows."""
    
    def __init__(self, domain: str = 'login'):
        """Initialize the authentication flow.
        
        Args:
            domain (str): Salesforce domain ('login' for production, 'test' for sandbox)
        """
        self.domain = domain
        self.session_id: Optional[str] = None
        self.instance_url: Optional[str] = None
    
    @abstractmethod
    def login(self) -> Tuple[str, str]:
        """Authenticate and return session ID and instance URL.
        
        Returns:
            Tuple[str, str]: Session ID and instance URL
        """
        pass

class BasicAuth(BaseAuth):
    """SOAP Login authentication using username and password."""
    
    def __init__(
        self, 
        username: str,
        password: str,
        security_token: Optional[str] = None,
        domain: str = 'login'
    ):
        """Initialize SOAP Login authentication.
        
        Args:
            username (str): Salesforce username
            password (str): Salesforce password
            security_token (str, optional): Security token for the username
            domain (str): Salesforce domain ('login' for production, 'test' for sandbox)
        """
        super().__init__(domain)
        self.username = username
        self.password = password
        self.security_token = security_token
    
    def login(self) -> Tuple[str, str]:
        """Authenticate using username and password.
        
        Returns:
            Tuple[str, str]: Session ID and instance URL
        """
        session_id, instance = SalesforceLogin(
            username=self.username,
            password=self.password,
            security_token=self.security_token,
            domain=self.domain
        )
        self.session_id = session_id
        self.instance_url = f"https://{instance}"
        return session_id, instance

class ClientCredentialsAuth(BaseAuth):
    """OAuth 2.0 Client Credentials Flow authentication."""
    
    def __init__(
        self,
        consumer_key: str,
        consumer_secret: str,
        domain: str = 'login'
    ):
        """Initialize Client Credentials Flow authentication.
        
        Args:
            consumer_key (str): Connected App's consumer key
            consumer_secret (str): Connected App's consumer secret
            domain (str): Salesforce domain ('login' for production, 'test' for sandbox)
        """
        super().__init__(domain)
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
    
    def login(self) -> Tuple[str, str]:
        """Authenticate using client credentials.
        
        Returns:
            Tuple[str, str]: Session ID and instance URL
        """
        session_id, instance = SalesforceLogin(
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
            domain=self.domain
        )
        self.session_id = session_id
        self.instance_url = f"https://{instance}"
        return session_id, instance

class JwtBearerAuth(BaseAuth):
    """OAuth 2.0 JWT Bearer Flow authentication."""
    
    def __init__(
        self,
        username: str,
        consumer_key: str,
        private_key_path: Optional[str] = None,
        private_key: Optional[str] = None,
        domain: str = 'login'
    ):
        """Initialize JWT Bearer Flow authentication.
        
        Args:
            username (str): Salesforce username
            consumer_key (str): Connected App's consumer key
            private_key_path (str, optional): Path to private key file
            private_key (str, optional): Private key as string
            domain (str): Salesforce domain ('login' for production, 'test' for sandbox)
        """
        super().__init__(domain)
        self.username = username
        self.consumer_key = consumer_key
        self.private_key_path = private_key_path
        self.private_key = private_key
        
        if not private_key_path and not private_key:
            raise ValueError("Either private_key_path or private_key must be provided")
    
    def login(self) -> Tuple[str, str]:
        """Authenticate using JWT Bearer token.
        
        Returns:
            Tuple[str, str]: Session ID and instance URL
        """
        session_id, instance = SalesforceLogin(
            username=self.username,
            consumer_key=self.consumer_key,
            privatekey_file=self.private_key_path,
            privatekey=self.private_key,
            domain=self.domain
        )
        self.session_id = session_id
        self.instance_url = f"https://{instance}"
        return session_id, instance

class DirectAuth(BaseAuth):
    """Direct authentication using existing session ID and instance URL."""
    
    def __init__(
        self,
        session_id: str,
        instance_url: str,
        domain: str = 'login'
    ):
        """Initialize direct authentication.
        
        Args:
            session_id (str): Valid Salesforce session ID
            instance_url (str): Salesforce instance URL
            domain (str): Salesforce domain ('login' for production, 'test' for sandbox)
        """
        super().__init__(domain)
        self.session_id = session_id
        self.instance_url = instance_url
    
    def login(self) -> Tuple[str, str]:
        """Return the existing session ID and instance.
        
        Returns:
            Tuple[str, str]: Session ID and instance URL
        """
        # Extract instance from instance_url (remove https://)
        instance = self.instance_url.replace('https://', '')
        return self.session_id, instance 