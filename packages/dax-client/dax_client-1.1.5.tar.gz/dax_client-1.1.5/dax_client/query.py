from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Union
from .models import DaxColumn, DaxTable, DaxValue, DaxString, DaxNumber, DaxBoolean, DaxDate

@dataclass
class DaxFunction:
    """Represents a DAX function call."""
    name: str
    arguments: List[Union['DaxExpression', DaxValue, DaxColumn]] = field(default_factory=list)

    def __str__(self) -> str:
        """Return the DAX representation of the function."""
        args_str = ", ".join(str(arg) for arg in self.arguments)
        return f"{self.name}({args_str})"

@dataclass
class DaxExpression:
    """Represents a DAX expression."""
    expression: str

    def __str__(self) -> str:
        """Return the DAX representation of the expression."""
        return self.expression

    @classmethod
    def from_str(cls, expression: str) -> 'DaxExpression':
        """Create a DaxExpression from a string.

        Args:
            expression: The DAX expression string

        Returns:
            A new DaxExpression instance
        """
        return cls(expression=expression)

@dataclass
class DaxQuery:
    """Represents a DAX query."""
    select_columns: List[Union[DaxColumn, DaxExpression, DaxFunction]] = field(default_factory=list)
    from_table: Optional[DaxTable] = None
    where_clause: Optional[DaxExpression] = None
    order_by: List[DaxColumn] = field(default_factory=list)
    group_by: List[DaxColumn] = field(default_factory=list)
    top_n: Optional[int] = None

    def select(self, *columns: Union[DaxColumn, DaxExpression, DaxFunction, str]) -> 'DaxQuery':
        """Add columns to the SELECT clause.

        Args:
            *columns: The columns to select

        Returns:
            The updated query object
        """
        for col in columns:
            if isinstance(col, str):
                self.select_columns.append(DaxColumn(name=col))
            else:
                self.select_columns.append(col)
        return self

    def from_table_name(self, table_name: str) -> 'DaxQuery':
        """Set the FROM table.

        Args:
            table_name: The name of the table

        Returns:
            The updated query object
        """
        self.from_table = DaxTable(name=table_name)
        return self

    def where(self, expression: Union[str, DaxExpression]) -> 'DaxQuery':
        """Set the WHERE clause.

        Args:
            expression: The where expression

        Returns:
            The updated query object
        """
        if isinstance(expression, str):
            self.where_clause = DaxExpression(expression=expression)
        else:
            self.where_clause = expression
        return self

    def order_by_columns(self, *columns: Union[DaxColumn, str]) -> 'DaxQuery':
        """Add columns to the ORDER BY clause.

        Args:
            *columns: The columns to order by

        Returns:
            The updated query object
        """
        for col in columns:
            if isinstance(col, str):
                self.order_by.append(DaxColumn(name=col))
            else:
                self.order_by.append(col)
        return self

    def group_by_columns(self, *columns: Union[DaxColumn, str]) -> 'DaxQuery':
        """Add columns to the GROUP BY clause.

        Args:
            *columns: The columns to group by

        Returns:
            The updated query object
        """
        for col in columns:
            if isinstance(col, str):
                self.group_by.append(DaxColumn(name=col))
            else:
                self.group_by.append(col)
        return self

    def top(self, n: int) -> 'DaxQuery':
        """Set the TOP N clause.

        Args:
            n: The number of rows to return

        Returns:
            The updated query object
        """
        self.top_n = n
        return self

    def to_dax_string(self) -> str:
        """Convert the query to a DAX query string.

        Returns:
            The DAX query string
        """
        if not self.select_columns:
            raise ValueError("Query must have at least one column in SELECT clause")

        if not self.from_table:
            raise ValueError("Query must have a FROM table")

        query_parts = []

        # Build SELECT clause
        select_clause = "EVALUATE "
        if self.top_n is not None:
            select_clause += f"TOPN({self.top_n}, "

        select_clause += "ROW("
        select_items = []
        for col in self.select_columns:
            if isinstance(col, DaxColumn):
                select_items.append(f'"{col.name}", {str(col)}')
            elif isinstance(col, (DaxExpression, DaxFunction)):
                select_items.append(f'"{str(col)}", {str(col)}')
        select_clause += ", ".join(select_items)
        select_clause += ")"

        if self.top_n is not None:
            select_clause += ")"

        query_parts.append(select_clause)

        # Add filters if needed
        if self.where_clause:
            query_parts.append(f"FILTER({self.from_table}, {self.where_clause})")

        # Add ORDER BY if needed
        if self.order_by:
            order_by_cols = ", ".join(str(col) for col in self.order_by)
            query_parts.append(f"ORDER BY {order_by_cols}")

        return "\n".join(query_parts)

@dataclass
class DaxQueryBuilder:
    """A builder for DAX queries."""

    @classmethod
    def create_query(cls) -> DaxQuery:
        """Create a new DAX query.

        Returns:
            A new DaxQuery instance
        """
        return DaxQuery()

    @classmethod
    def column(cls, name: str, table: Optional[str] = None) -> DaxColumn:
        """Create a DAX column reference.

        Args:
            name: The column name
            table: The optional table name

        Returns:
            A new DaxColumn instance
        """
        return DaxColumn(name=name, table=table)

    @classmethod
    def table(cls, name: str) -> DaxTable:
        """Create a DAX table reference.

        Args:
            name: The table name

        Returns:
            A new DaxTable instance
        """
        return DaxTable(name=name)

    @classmethod
    def function(cls, name: str, *args: Any) -> DaxFunction:
        """Create a DAX function call.

        Args:
            name: The function name
            *args: The function arguments

        Returns:
            A new DaxFunction instance
        """
        return DaxFunction(name=name, arguments=list(args))

    @classmethod
    def expression(cls, expression: str) -> DaxExpression:
        """Create a DAX expression.

        Args:
            expression: The DAX expression string

        Returns:
            A new DaxExpression instance
        """
        return DaxExpression(expression=expression)
