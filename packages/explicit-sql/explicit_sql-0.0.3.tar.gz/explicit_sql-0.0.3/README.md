# explicit-sql

A human mind friendly SQL generator for DuckDB.

## Overview

I genuinely do not like ORMs because of the Object–relational impedance mismatch. 
While we have many good ORMs that can speed up development of POCs and MVPs drastically, 
this project aims at a simpler idea: implement a human mind friendly and type-safe SQL generator for all basic operations:

- CREATE TABLE
- DROP TABLE
- INSERT INTO
- SELECT FROM
- UPDATE
- DELETE
- And more...

I found myself developing this when working on simple side-projects using DuckDB and realized there was no interface to generate SQL queries from TypedDict definitions.

## Philosophy

The goal is to stay as close to "raw" Python as possible. 
For table schemas, I chose TypedDict, and besides that have only two classes:

1. TableConfig - for configuration settings
2. ExplicitTable - a container class for both the TypedDict definition and config

This minimalist approach should be enough to achieve a useful, type-safe SQL generator without the complexity of ORMs.

## Requirements

- Python 3.10+

## Installation

```bash
pip install explicit-sql
```

## Quick Example

```python
from explicit_sql import TableDefinition, TableConfig, ExplicitTable, create_table_sql

# Define your table schema
class UsersTable(TableDefinition):
    id: int
    name: str
    is_active: bool | None

users_config = TableConfig(
    name="users",
    schema="public",
    primary_key_name="id",
    primary_key_type=int,
)

users_table = ExplicitTable(
    config=users_config,
    table_definition=UsersTable
)

create_table_sql = create_table_sql(users_table)
print(create_table_sql)

insert_payload: UsersTable = {
    "amount": 500,
    "name": "John Doe",
    "is_active": True,
}
print(insert_sql(users_table, insert_payload))


print(
    select_sql(
        users_table,
        select_columns=["name", "amount"],
        where_values={"is_active": True},
        order_by=["amount"],
        limit=10,
    )
)

# Select all columns
print(select_sql(users_table, limit=10))

```

## Roadmap

See the [milestone plan](milestone_plan.md) for the development roadmap.

## License

MIT
