# DuckTyped: TypedDict SQL Generator for DuckDB

## Project Milestones

### v0.1.0 - Core Functionality
- [x] Implement `create_table_sql()` function
- [ ] Fix `__annotations__` access in `create_table_sql()` to use `table_definition.__annotations__`
- [ ] Implement `drop_table_sql()` function
- [x] Implement `insert_sql()` function
- [x] Implement `select_sql()` basic function
- [ ] Add proper package structure (setup.py, pyproject.toml, README)
- [ ] Create simple documentation with examples
- [ ] Add basic test suite

### v0.2.0 - Query Building
- [x] Implement `update_sql()` function
- [x] Implement `delete_sql()` function
- [ ] Add `where_clause()` builder
- [ ] Add `join_clause()` builder
- [ ] Add `order_by_clause()` builder
- [ ] Implement type-safe column reference system
- [ ] Add support for primary keys and foreign keys
- [ ] Improve value formatting for different SQL types

### v0.3.0 - Extended Type Support
- [ ] Support for array types
- [ ] Support for date/time types
- [ ] Support for decimal types
- [ ] Support for enum types
- [ ] Support for struct types
- [ ] Support for map/dictionary types
- [ ] Add default value specification
- [ ] Add column comment/description support

### v0.4.0 - Batch Operations
- [ ] Implement `bulk_insert_sql()` function
- [ ] Implement `upsert_sql()` (INSERT ON CONFLICT) function
- [ ] Add transaction support helpers
- [ ] Add statement parameterization support
- [ ] Performance optimizations for large batches

### v0.5.0 - Schema Management
- [ ] Implement `alter_table_sql()` function
- [ ] Add index creation support
- [ ] Implement schema comparison tools
- [ ] Create migration generation utilities
- [ ] Add table constraint support (UNIQUE, CHECK, etc.)

### v1.0.0 - Production Ready
- [ ] Comprehensive documentation
- [ ] Interactive examples
- [ ] 90%+ test coverage
- [ ] CI/CD pipeline setup
- [ ] PyPI publication
- [ ] CLI tool for schema generation from Python files

## Future Ideas
- Schema visualization tools
- Custom type adapters
- Integration with common Python data libraries (pandas, polars, etc.)
- Schema validation against existing database