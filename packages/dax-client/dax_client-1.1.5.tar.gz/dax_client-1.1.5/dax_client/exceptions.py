# src/daxclient/exceptions.py
from typing import Optional, Any

class DaxClientError(Exception):
    """Base exception for DAX client errors."""
    pass

class DaxApiError(DaxClientError):
    """Exception raised when the DAX API returns an error."""

    def __init__(self, message: str, status_code: int, response: Any) -> None:
        """Initialize the exception.

        Args:
            message: The error message
            status_code: The HTTP status code
            response: The API response
        """
        super().__init__(message)
        self.status_code = status_code
        self.response = response
