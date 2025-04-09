# src/daxclient/telemetry.py
import os
import platform
import uuid
import json
import requests
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging
import atexit
from threading import Thread, Lock

logger = logging.getLogger(__name__)

@dataclass
class TelemetryEvent:
    """Represents a telemetry event."""
    event_name: str
    properties: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.utcnow)
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self) -> Dict[str, Any]:
        """Convert the event to a dictionary.

        Returns:
            The event as a dictionary
        """
        return {
            "eventId": self.event_id,
            "eventName": self.event_name,
            "properties": self.properties,
            "timestamp": self.timestamp.isoformat()
        }

@dataclass
class TelemetryClient:
    """Client for collecting and sending telemetry data."""
    telemetry_endpoint: str = "https://api.example.com/telemetry"
    enabled: bool = True
    client_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    events: List[TelemetryEvent] = field(default_factory=list)
    _lock: Lock = field(default_factory=Lock)

    def __post_init__(self) -> None:
        """Initialize the telemetry client."""
        # Check if telemetry is disabled via environment variable
        if os.environ.get("DAX_CLIENT_TELEMETRY_DISABLED", "").lower() in ("true", "1", "yes"):
            self.enabled = False

        # Try to load or create a persistent client ID
        self._load_or_create_client_id()

        # Register the flush method to run at exit
        atexit.register(self.flush)

        # Track installation information
        if self.enabled:
            self.track_event("client_installed", self._get_system_info())

    def _load_or_create_client_id(self) -> None:
        """Load an existing client ID or create a new one."""
        config_dir = os.path.expanduser("~/.daxclient")
        config_file = os.path.join(config_dir, "config.json")

        try:
            if os.path.exists(config_file):
                with open(config_file, "r") as f:
                    config = json.load(f)
                    self.client_id = config.get("client_id", self.client_id)
            else:
                # Create the config directory if it doesn't exist
                os.makedirs(config_dir, exist_ok=True)

                # Save the client ID
                with open(config_file, "w") as f:
                    json.dump({"client_id": self.client_id}, f)
        except Exception as e:
            logger.warning(f"Failed to load or save client ID: {e}")

    def _get_system_info(self) -> Dict[str, str]:
        """Get system information for telemetry.

        Returns:
            A dictionary of system information
        """
        return {
            "os": platform.system(),
            "os_version": platform.version(),
            "python_version": platform.python_version(),
            "platform": platform.platform(),
            "machine": platform.machine(),
            "daxclient_version": "0.1.0"  # This should be updated with the actual version
        }

    def track_event(self, event_name: str, properties: Optional[Dict[str, Any]] = None) -> None:
        """Track a telemetry event.

        Args:
            event_name: The name of the event
            properties: Additional properties for the event
        """
        if not self.enabled:
            return

        if properties is None:
            properties = {}

        # Add common properties
        properties.update({
            "client_id": self.client_id,
            "session_id": self.session_id,
        })

        event = TelemetryEvent(event_name=event_name, properties=properties)

        with self._lock:
            self.events.append(event)

            # Flush events if we have accumulated enough
            if len(self.events) >= 10:
                self._flush_async()

    def _flush_async(self) -> None:
        """Flush events asynchronously."""
        thread = Thread(target=self.flush)
        thread.daemon = True
        thread.start()

    def flush(self) -> None:
        """Flush accumulated telemetry events to the endpoint."""
        if not self.enabled or not self.events:
            return

        # Make a copy of the events and clear the list
        with self._lock:
            events_to_send = self.events.copy()
            self.events.clear()

        if not events_to_send:
            return

        try:
            payload = {
                "clientId": self.client_id,
                "sessionId": self.session_id,
                "events": [event.to_dict() for event in events_to_send]
            }

            response = requests.post(
                self.telemetry_endpoint,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=5
            )

            if response.status_code >= 400:
                logger.warning(f"Failed to send telemetry: {response.status_code} - {response.text}")

                # Put the events back in the queue
                with self._lock:
                    self.events.extend(events_to_send)

        except Exception as e:
            logger.warning(f"Error sending telemetry: {e}")

            # Put the events back in the queue
            with self._lock:
                self.events.extend(events_to_send)
