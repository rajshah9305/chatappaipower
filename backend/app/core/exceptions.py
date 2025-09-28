"""
Custom exceptions for the application
"""

from typing import Optional, Dict, Any


class CustomException(Exception):
    """Base custom exception"""
    
    def __init__(
        self,
        message: str,
        error_code: str = "CUSTOM_ERROR",
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(CustomException):
    """Validation error"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            status_code=400,
            details=details
        )


class NotFoundError(CustomException):
    """Resource not found error"""
    
    def __init__(self, resource: str, identifier: str):
        super().__init__(
            message=f"{resource} with identifier '{identifier}' not found",
            error_code="NOT_FOUND",
            status_code=404,
            details={"resource": resource, "identifier": identifier}
        )


class AuthenticationError(CustomException):
    """Authentication error"""
    
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(
            message=message,
            error_code="AUTHENTICATION_ERROR",
            status_code=401
        )


class AuthorizationError(CustomException):
    """Authorization error"""
    
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(
            message=message,
            error_code="AUTHORIZATION_ERROR",
            status_code=403
        )


class ConflictError(CustomException):
    """Resource conflict error"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="CONFLICT_ERROR",
            status_code=409,
            details=details
        )


class ExternalServiceError(CustomException):
    """External service error"""
    
    def __init__(self, service: str, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=f"Error with {service}: {message}",
            error_code="EXTERNAL_SERVICE_ERROR",
            status_code=502,
            details={"service": service, **(details or {})}
        )


class CerebrasAPIError(ExternalServiceError):
    """Cerebras API specific error"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            service="Cerebras API",
            message=message,
            details=details
        )


class WorkflowExecutionError(CustomException):
    """Workflow execution error"""
    
    def __init__(self, workflow_id: str, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=f"Workflow {workflow_id} execution failed: {message}",
            error_code="WORKFLOW_EXECUTION_ERROR",
            status_code=422,
            details={"workflow_id": workflow_id, **(details or {})}
        )


class AgentExecutionError(CustomException):
    """Agent execution error"""
    
    def __init__(self, agent_id: str, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=f"Agent {agent_id} execution failed: {message}",
            error_code="AGENT_EXECUTION_ERROR",
            status_code=422,
            details={"agent_id": agent_id, **(details or {})}
        )


class RateLimitError(CustomException):
    """Rate limit exceeded error"""
    
    def __init__(self, message: str = "Rate limit exceeded", retry_after: int = 60):
        super().__init__(
            message=message,
            error_code="RATE_LIMIT_ERROR",
            status_code=429,
            details={"retry_after": retry_after}
        )