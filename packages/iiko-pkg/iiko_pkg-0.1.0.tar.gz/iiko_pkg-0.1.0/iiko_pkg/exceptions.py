"""
Exceptions for iiko.services API
"""

class IikoError(Exception):
    """Base exception for iiko.services API"""
    pass


class AuthenticationError(IikoError):
    """Authentication error"""
    pass


class ApiError(IikoError):
    """API error"""
    def __init__(self, status_code, error_message, response=None):
        self.status_code = status_code
        self.error_message = error_message
        self.response = response
        super().__init__(f"API Error {status_code}: {error_message}")


class ValidationError(IikoError):
    """Validation error"""
    pass


class NetworkError(IikoError):
    """Network error"""
    pass
