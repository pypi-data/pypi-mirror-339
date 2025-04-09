import re
import types
from dataclasses import dataclass
from enum import Enum
from typing import (
    Any,
    Dict,
    List,
    Literal,
    NotRequired,
    Optional,
    Type,
    TypedDict,
    Union,
    get_args,
    get_origin,
)
from uuid import UUID

PRIMARY_KEY_TYPES = int | str | UUID


class SQLType(Enum):
    INTEGER = "INTEGER"
    TEXT = "TEXT"
    REAL = "REAL"
    BOOLEAN = "BOOLEAN"


@dataclass
class TableConfig:
    """Configuration for table definitions."""

    primary_key_name: str
    primary_key_type: PRIMARY_KEY_TYPES
    name: str | None = None
    schema: str = "public"


class TableDefinition(TypedDict):
    """Base class for table definitions that can be used to generate SQL."""


@dataclass
class ExplicitTable:
    config: TableConfig
    table_definition: Type[TableDefinition]


class Column(TypedDict):
    name: str
    type: SQLType


def _camel_to_snake(name: str) -> str:
    """Convert CamelCase string to snake_case."""
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def _format_value(value: Any) -> str:
    """Format Python values for SQL insertion."""
    if value is None:
        return "NULL"
    elif isinstance(value, str):
        escaped = value.replace("'", "''")
        return f"'{escaped}'"
    elif isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, list):
        elements = [_format_value(v) for v in value]
        return f"[{', '.join(elements)}]"
    elif isinstance(value, dict):
        import json

        json_str = json.dumps(value)
        return f"'{json_str.replace("'", "''")}'"
    else:
        return f"'{str(value)}'"


def _python_type_to_sql_type(py_type: type) -> SQLType:
    """Map Python types to SQL types, handling Nullable types."""
    origin = get_origin(py_type)
    args = get_args(py_type)

    is_nullable = False
    base_type = py_type
    base_origin = get_origin(base_type)

    # Check for Union[T, None] or Optional[T]
    if origin in (Union, types.UnionType) and types.NoneType in args:
        is_nullable = True
        # Get the type other than NoneType, default to str if only NoneType is present
        base_type = next((t for t in args if t is not types.NoneType), str)
        base_origin = get_origin(base_type)

    match base_type:
        case _ if base_type is int:
            sql_type = SQLType.INTEGER
        case _ if base_type is str:
            sql_type = SQLType.TEXT
        case _ if base_type is float:
            # TODO: Maybe need to add FLOAT to support some dialects?
            sql_type = SQLType.REAL
        case _ if base_type is bool:
            sql_type = SQLType.BOOLEAN
        case _:
            # Check origin for Literal in the default case
            if base_origin is Literal:
                # Map Literal[...] to TEXT.
                # Proper SQL ENUM support would require generating CREATE TYPE statements separately.
                sql_type = SQLType.TEXT
            else:
                # Simple fallback for other types
                sql_type = SQLType.TEXT

    return sql_type


def _get_table_name(duck_table: "ExplicitTable") -> str:
    """Get the table name from a DuckTable object."""
    if duck_table.config.name:
        return duck_table.config.name

    table_name = _camel_to_snake(duck_table.table_definition.__name__)
    # TODO(@m0n0x41d): add in docs that behavior
    if table_name.endswith("_table"):
        table_name = table_name[:-6]

    return table_name


### LIBRARY HELPERS ###


# PRECONDITIONS:
# - explicit_table is a valid ExplicitTable instance.
# - explicit_table.table_definition is a valid TypedDict.
# POSTCONDITIONS:
# - Returns a string containing a valid SQL CREATE TABLE statement.
# - The statement reflects the table name, schema, columns, and types defined in explicit_table.
def create_table_sql(duck_table: ExplicitTable, if_not_exists: bool = True) -> str:
    """Generate SQL CREATE TABLE statement from a TypedDict definition.

    Args:
        table_definition: A TypedDict class that inherits from TableDefinition

    Returns:
        str: SQL CREATE TABLE statement
    """
    table_name = _get_table_name(duck_table)
    schema_prefix = f"{duck_table.config.schema}." if duck_table.config.schema else ""
    full_table_name = f"{schema_prefix}{table_name}"

    if_not_exists_clause = "IF NOT EXISTS" if if_not_exists else ""
    base = f"CREATE TABLE {if_not_exists_clause} {full_table_name}"

    column_definitions_str = []
    pk_name_config = duck_table.config.primary_key_name
    pk_type_config = duck_table.config.primary_key_type

    # Use table_definition from ExplicitTable
    for field_name, field_type in duck_table.table_definition.__annotations__.items():
        column_name = _camel_to_snake(field_name)
        is_primary_key = pk_name_config is not None and field_name == pk_name_config

        # Determine the type to use for SQL mapping
        type_for_sql_mapping = field_type
        if is_primary_key and pk_type_config is not None:
            type_for_sql_mapping = pk_type_config  # Use config type for PK

        sql_type_enum = _python_type_to_sql_type(type_for_sql_mapping)
        sql_type_str = sql_type_enum.value

        col_def = f"{column_name} {sql_type_str}"

        is_nullable = False
        if not is_primary_key:
            origin = get_origin(field_type)
            args = get_args(field_type)
            is_nullable = (origin in (Union, types.UnionType) and types.NoneType in args) or get_origin(
                field_type
            ) is NotRequired

        if not is_nullable:  # Includes the PK case implicitly
            col_def += " NOT NULL"

        if is_primary_key:
            col_def += " PRIMARY KEY"

        column_definitions_str.append(col_def)

    query = f"{base} ({', '.join(column_definitions_str)});"
    return query


def insert_sql(
    explicit_table: ExplicitTable,
    insert_data: dict[str, Any],
) -> str:
    """Generate SQL INSERT statement from a TypedDict instance.

    Args:
        instance: A TypedDict instance inheriting from TableDefinition
        table_name: Optional table name override (if not specified, derives from class name)

    Returns:
        str: SQL INSERT statement
    """
    table_name = _get_table_name(explicit_table)
    schema_prefix = f"{explicit_table.config.schema}." if explicit_table.config.schema else ""
    full_table_name = f"{schema_prefix}{table_name}"

    fields = []
    values = []

    for field_name, field_value in insert_data.items():
        if field_name not in explicit_table.table_definition.__annotations__:
            raise ValueError(
                f"Field '{field_name}' not found in table definition '{explicit_table.table_definition.__name__}'."
            )

        if field_value is not None:  # Skip None values for optional fields
            fields.append(field_name)
            values.append(_format_value(field_value))

    fields_str = ", ".join(fields)
    values_str = ", ".join(values)

    return f"INSERT INTO {full_table_name} ({fields_str}) VALUES ({values_str});"


# PRECONDITIONS:
# - explicit_table is a valid ExplicitTable instance.
# - explicit_table.config.primary_key is defined.
# - explicit_table.table_definition is a valid TypedDict.
# - update_data is a dictionary or TypedDict.
# - update_data contains the primary key field (as defined in explicit_table.config.primary_key) with a non-None value.
# - update_data contains at least one field other than the primary key.
# - All keys in update_data correspond to field names defined in explicit_table.table_definition.
# - If returning is not None, all names in the returning list correspond to field names defined in explicit_table.table_definition.
# POSTCONDITIONS:
# - Returns a string containing a valid SQL UPDATE statement.
# - The statement targets the table and schema defined in explicit_table.
# - The SET clause includes all fields from update_data except the primary key.
# - The WHERE clause filters based on the primary key field and value from update_data.
# - Includes a RETURNING clause if returning was specified.
def update_sql_by_id(
    explicit_table: "ExplicitTable",
    update_data: Dict[str, Any],
    returning: Optional[List[str]] = None,
) -> str:
    """Generate SQL UPDATE statement based on primary key.

    Updates fields present in update_data, excluding the primary key itself.

    Args:
        explicit_table: An ExplicitTable object containing table definition and config.
        update_data: Dictionary with field names (matching TypedDict keys)
                     and values to update, including the primary key.
        returning: List of fields (Python names) to return after update.

    Returns:
        str: SQL UPDATE statement

    Raises:
        ValueError: If primary key is not defined in config, not found in
                    update_data, if no fields are left to update after
                    excluding the primary key, or if a field in update_data
                    does not exist in the table definition.
    """
    table_name = _get_table_name(explicit_table)
    schema_prefix = f"{explicit_table.config.schema}." if explicit_table.config.schema else ""
    full_table_name = f"{schema_prefix}{table_name}"

    primary_key_py_name = explicit_table.config.primary_key_name
    if not primary_key_py_name:
        raise ValueError("Primary key must be defined in TableConfig for update_sql.")

    if primary_key_py_name not in update_data:
        raise ValueError(f"Primary key '{primary_key_py_name}' not found in update_data.")

    primary_key_col_name = _camel_to_snake(primary_key_py_name)
    primary_key_value = update_data[primary_key_py_name]

    set_clauses = []

    # TODO: Add compatibility check: ensure keys in update_data exist in table_definition

    for field_name, field_value in update_data.items():
        # Don't include the primary key in the SET clause
        if field_name == primary_key_py_name:
            continue

        if field_name not in explicit_table.table_definition.__annotations__:
            raise ValueError(
                f"Field '{field_name}' not found in table definition '{explicit_table.table_definition.__name__}'."
            )

        column_name = _camel_to_snake(field_name)
        formatted_value = _format_value(field_value)
        set_clauses.append(f"{column_name} = {formatted_value}")

    if not set_clauses:
        raise ValueError("No fields to update (only primary key provided in update_data).")

    where_clause = f"{primary_key_col_name} = {_format_value(primary_key_value)}"

    query = f"UPDATE {full_table_name} SET {', '.join(set_clauses)} WHERE {where_clause}"

    if returning:
        # Convert Python field names to snake_case column names for RETURNING
        return_columns = [_camel_to_snake(col) for col in returning]
        query += f" RETURNING {', '.join(return_columns)}"

    return f"{query};"


# PRECONDITIONS:
# - explicit_table is a valid ExplicitTable instance.
# - explicit_table.config.primary_key_name is defined.
# - primary_key_value is a non-None value of the type specified in explicit_table.config.primary_key_type.
# POSTCONDITIONS:
# - Returns a string containing a valid SQL DELETE statement.
# - The statement targets the table and schema defined in explicit_table.
# - The WHERE clause filters based on the primary key column and the provided primary_key_value.
def delete_sql_by_id(
    explicit_table: "ExplicitTable",
    primary_key_value: PRIMARY_KEY_TYPES,
) -> str:
    """Generate SQL DELETE statement based on primary key.

    Args:
        explicit_table: An ExplicitTable object containing table definition and config.
        primary_key_value: The value of the primary key for the row to delete.

    Returns:
        str: SQL DELETE statement

    Raises:
        ValueError: If primary key is not defined in config.
    """
    table_name = _get_table_name(explicit_table)
    schema_prefix = f"{explicit_table.config.schema}." if explicit_table.config.schema else ""
    full_table_name = f"{schema_prefix}{table_name}"

    primary_key_py_name = explicit_table.config.primary_key_name
    if not primary_key_py_name:
        raise ValueError("Primary key must be defined in TableConfig for delete_sql_by_id.")

    primary_key_col_name = _camel_to_snake(primary_key_py_name)
    formatted_pk_value = _format_value(primary_key_value)

    query = f"DELETE FROM {full_table_name} WHERE {primary_key_col_name} = {formatted_pk_value};"
    return query


# PRECONDITIONS:
# - explicit_table is a valid ExplicitTable instance.
# - where_values is a non-empty dictionary.
# - All keys in where_values correspond to valid field names in explicit_table.table_definition.
# POSTCONDITIONS:
# - Returns a string containing a valid SQL DELETE statement.
# - The statement targets the table and schema defined in explicit_table.
# - The WHERE clause includes conditions for all key-value pairs in where_values.
def delete_where(
    explicit_table: "ExplicitTable",
    where_values: Dict[str, Any],
) -> str:
    """Generate SQL DELETE statement based on arbitrary WHERE conditions.

    Args:
        explicit_table: An ExplicitTable object containing table definition and config.
        where_values: Dictionary with field names (matching TypedDict keys)
                      and values to use in the WHERE clause.

    Returns:
        str: SQL DELETE statement

    Raises:
        ValueError: If where_values is empty or if a key in where_values
                    does not exist in the table definition.
    """
    if not where_values:
        raise ValueError("where_values cannot be empty for DELETE operation.")

    table_name = _get_table_name(explicit_table)
    schema_prefix = f"{explicit_table.config.schema}." if explicit_table.config.schema else ""
    full_table_name = f"{schema_prefix}{table_name}"

    where_clauses = []
    for field_name, field_value in where_values.items():
        if field_name not in explicit_table.table_definition.__annotations__:
            raise ValueError(
                f"Field '{field_name}' not found in table definition '{explicit_table.table_definition.__name__}'."
            )

        column_name = _camel_to_snake(field_name)
        formatted_value = _format_value(field_value)
        where_clauses.append(f"{column_name} = {formatted_value}")

    where_clause_str = " AND ".join(where_clauses)

    query = f"DELETE FROM {full_table_name} WHERE {where_clause_str};"
    return query


# PRECONDITIONS:
# - explicit_table is a valid ExplicitTable instance.
# - If select_columns is provided, all names correspond to valid field names in explicit_table.table_definition.
# - If where_values is provided, all keys correspond to valid field names in explicit_table.table_definition.
# - If order_by is provided, all names correspond to valid field names in explicit_table.table_definition.
# - limit, if provided, is a non-negative integer.
# POSTCONDITIONS:
# - Returns a string containing a valid SQL SELECT statement.
# - The statement targets the table and schema defined in explicit_table.
# - Includes specified columns, WHERE clause, ORDER BY clause, and LIMIT clause as requested.
def select_sql(
    explicit_table: "ExplicitTable",
    select_columns: Optional[List[str]] = None,
    where_values: Optional[Dict[str, Any]] = None,
    order_by: Optional[List[str]] = None,  # List of Python field names
    limit: Optional[int] = None,
) -> str:
    """Generate SQL SELECT statement.

    Args:
        explicit_table: An ExplicitTable object containing table definition and config.
        select_columns: List of Python field names to select. Selects all (*) if None.
        where_values: Dictionary with field names (matching TypedDict keys)
                      and values to use in the WHERE clause.
        order_by: List of Python field names to order the results by.
        limit: Maximum number of rows to return.

    Returns:
        str: SQL SELECT statement

    Raises:
        ValueError: If an invalid field name is provided in select_columns,
                    where_values, or order_by, or if limit is negative.
    """
    table_name = _get_table_name(explicit_table)
    schema_prefix = f"{explicit_table.config.schema}." if explicit_table.config.schema else ""
    full_table_name = f"{schema_prefix}{table_name}"

    # Select columns
    if not select_columns:
        select_clause = "*"
    else:
        selected_cols_sql = []
        for col_py_name in select_columns:
            if col_py_name not in explicit_table.table_definition.__annotations__:
                raise ValueError(
                    f"Select column '{col_py_name}' not found in table definition '{explicit_table.table_definition.__name__}'."
                )
            selected_cols_sql.append(_camel_to_snake(col_py_name))
        select_clause = ", ".join(selected_cols_sql)

    query = f"SELECT {select_clause} FROM {full_table_name}"

    if where_values:
        where_clauses = []
        for field_name, field_value in where_values.items():
            if field_name not in explicit_table.table_definition.__annotations__:
                raise ValueError(
                    f"WHERE field '{field_name}' not found in table definition '{explicit_table.table_definition.__name__}'."
                )
            column_name = _camel_to_snake(field_name)
            formatted_value = _format_value(field_value)
            where_clauses.append(f"{column_name} = {formatted_value}")
        if where_clauses:
            query += f" WHERE {' AND '.join(where_clauses)}"

    if order_by:
        order_by_sql = []
        for col_py_name in order_by:
            if col_py_name not in explicit_table.table_definition.__annotations__:
                raise ValueError(
                    f"ORDER BY column '{col_py_name}' not found in table definition '{explicit_table.table_definition.__name__}'."
                )
            order_by_sql.append(_camel_to_snake(col_py_name))
        if order_by_sql:
            query += f" ORDER BY {', '.join(order_by_sql)}"

    if limit is not None:
        if not isinstance(limit, int) or limit < 0:
            raise ValueError("LIMIT must be a non-negative integer.")
        query += f" LIMIT {limit}"

    return f"{query};"
