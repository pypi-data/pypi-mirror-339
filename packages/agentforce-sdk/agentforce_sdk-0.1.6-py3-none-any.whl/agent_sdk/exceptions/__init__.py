"""Exception classes for the Agentforce SDK."""

class AgentforceError(Exception):
    """Base exception for all Agentforce errors."""
    pass

class AgentforceAuthError(AgentforceError):
    """Raised when authentication to Salesforce fails."""
    pass

class AgentforceApiError(AgentforceError):
    """Raised when there is an error calling an external API."""
    pass

class MetadataDeploymentError(AgentforceError):
    """Raised when there is an error deploying metadata to Salesforce."""
    pass

class ConfigurationError(AgentforceError):
    """Raised when there is an error with the configuration."""
    pass

class ResourceNotFoundError(AgentforceError):
    """Raised when a requested resource is not found."""
    pass

class ValidationError(AgentforceError):
    """Raised when validation of input data fails."""
    pass 