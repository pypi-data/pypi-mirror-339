# src/daxclient/client.py
import json
import requests
from dataclasses import dataclass, field
from typing import Dict, Optional, Any, Union
from .models import DaxQueryResult
from .query import DaxQuery
from .exceptions import DaxClientError, DaxApiError
from .telemetry import TelemetryClient

@dataclass
class DaxClient:
    """Client for executing DAX queries against a remote API."""
    base_url: str
    api_key: Optional[str] = None
    headers: Dict[str, str] = field(default_factory=dict)
    timeout: int = 30
    telemetry_client: TelemetryClient = field(default_factory=TelemetryClient)

    def __post_init__(self) -> None:
        """Initialize the client with default headers."""
        self.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

        if self.api_key:
            self.headers["Authorization"] = f"Bearer {self.api_key}"

        # Track client initialization
        self.telemetry_client.track_event("client_initialized", {
            "base_url": self.base_url,
            "has_api_key": self.api_key is not None
        })

    def execute_query(self, query: Union[DaxQuery, str]) -> DaxQueryResult:
        """Execute a DAX query against the remote API.

        Args:
            query: The DAX query to execute

        Returns:
            The query result

        Raises:
            DaxClientError: If there's a client-side error
            DaxApiError: If there's an API error
        """
        query_str = query if isinstance(query, str) else query.to_dax_string()

        try:
            # Track query execution
            self.telemetry_client.track_event("query_executed", {
                "query_length": len(query_str)
            })

            response = requests.post(
                f"{self.base_url}/api/dax/query",
                headers=self.headers,
                json={"query": query_str},
                timeout=self.timeout
            )

            if response.status_code >= 400:
                # Track query error
                self.telemetry_client.track_event("query_error", {
                    "status_code": response.status_code,
                    "error": response.text[:100]  # Truncate long error messages
                })

                raise DaxApiError(
                    f"API error: {response.status_code} - {response.text}",
                    status_code=response.status_code,
                    response=response.text
                )

            result_data = response.json()

            # Track query success
            self.telemetry_client.track_event("query_success", {
                "execution_time_ms": result_data.get("executionTimeMs", 0),
                "row_count": len(result_data.get("data", []))
            })

            return DaxQueryResult.from_api_response(result_data)

        except requests.RequestException as e:
            # Track network error
            self.telemetry_client.track_event("network_error", {
                "error_type": type(e).__name__,
                "error_message": str(e)
            })

            raise DaxClientError(f"Request error: {str(e)}") from e
        except json.JSONDecodeError as e:
            # Track JSON parsing error
            self.telemetry_client.track_event("json_error", {
                "error_message": str(e)
            })

            raise DaxClientError(f"JSON decode error: {str(e)}") from e
