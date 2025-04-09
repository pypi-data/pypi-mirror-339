from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from uuid import uuid4

@dataclass(frozen=True)
class DaxValue:
    """Base class for DAX values."""
    pass

@dataclass(frozen=True)
class DaxNumber(DaxValue):
    """Represents a numeric value in DAX."""
    value: Union[int, float]

    @classmethod
    def from_int(cls, value: int) -> 'DaxNumber':
        """Create a DaxNumber from an integer.

        Args:
            value: The integer value

        Returns:
            A new DaxNumber instance
        """
        return cls(value=value)

    @classmethod
    def from_float(cls, value: float) -> 'DaxNumber':
        """Create a DaxNumber from a float.

        Args:
            value: The float value

        Returns:
            A new DaxNumber instance
        """
        return cls(value=value)

@dataclass(frozen=True)
class DaxString(DaxValue):
    """Represents a string value in DAX."""
    value: str

    @classmethod
    def from_str(cls, value: str) -> 'DaxString':
        """Create a DaxString from a Python string.

        Args:
            value: The string value

        Returns:
            A new DaxString instance
        """
        return cls(value=value)

@dataclass(frozen=True)
class DaxBoolean(DaxValue):
    """Represents a boolean value in DAX."""
    value: bool

    @classmethod
    def from_bool(cls, value: bool) -> 'DaxBoolean':
        """Create a DaxBoolean from a Python boolean.

        Args:
            value: The boolean value

        Returns:
            A new DaxBoolean instance
        """
        return cls(value=value)

@dataclass(frozen=True)
class DaxDate(DaxValue):
    """Represents a date value in DAX."""
    value: datetime

    @classmethod
    def from_datetime(cls, value: datetime) -> 'DaxDate':
        """Create a DaxDate from a Python datetime.

        Args:
            value: The datetime value

        Returns:
            A new DaxDate instance
        """
        return cls(value=value)

    @classmethod
    def from_str(cls, value: str, format_str: str = "%Y-%m-%d") -> 'DaxDate':
        """Create a DaxDate from a string.

        Args:
            value: The date string
            format_str: The format string for parsing the date

        Returns:
            A new DaxDate instance
        """
        return cls(value=datetime.strptime(value, format_str))

@dataclass(frozen=True)
class DaxColumn:
    """Represents a column in a DAX query."""
    name: str
    table: Optional[str] = None

    def __str__(self) -> str:
        """Return the DAX representation of the column."""
        if self.table:
            return f"'{self.table}'[{self.name}]"
        return f"[{self.name}]"

@dataclass(frozen=True)
class DaxMeasure:
    """Represents a measure in a DAX query."""
    name: str
    expression: str

    def __str__(self) -> str:
        """Return the DAX representation of the measure."""
        return f"{self.name} = {self.expression}"

@dataclass(frozen=True)
class DaxTable:
    """Represents a table in a DAX query."""
    name: str
    columns: List[DaxColumn] = field(default_factory=list)

    def __str__(self) -> str:
        """Return the DAX representation of the table."""
        return f"'{self.name}'"

@dataclass(frozen=True)
class DaxQueryResult:
    """Represents the result of a DAX query."""
    data: List[Dict[str, Any]]
    columns: List[str]
    execution_time_ms: int
    query_id: str = field(default_factory=lambda: str(uuid4()))

    @classmethod
    def from_api_response(cls, response: Dict[str, Any]) -> 'DaxQueryResult':
        """Create a DaxQueryResult from an API response.

        Args:
            response: The API response dictionary

        Returns:
            A new DaxQueryResult instance
        """
        return cls(
            data=response.get("data", []),
            columns=response.get("columns", []),
            execution_time_ms=response.get("executionTimeMs", 0),
            query_id=response.get("queryId", str(uuid4()))
        )
