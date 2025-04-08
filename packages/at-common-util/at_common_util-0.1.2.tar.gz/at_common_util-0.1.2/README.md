# AT Common Utils

A collection of common utilities for AT backend services.

## Package Structure

```
at_common_util/
├── db/                      # Database related utilities
│   ├── __init__.py          # Package exports
│   ├── storage.py           # Database connection and data access (CRUD operations)
│   └── query.py             # Query building utilities
├── workflow/                # Workflow related utilities
│   ├── __init__.py          # Package exports
│   ├── core/                # Core workflow components
│   └── utils/               # Workflow utility functions
└── examples/                # Example implementations
    └── db/                  # Database usage examples
```

## Installation

```bash
pip install -e /path/to/at-common-util
```

Or include in your requirements.txt:

```
-e /path/to/at-common-util
```

## Database Utilities

The package provides a comprehensive database access layer with three main components:

1. **Storage** - Connection management, session handling, and CRUD operations
2. **StorageManager** - Registry for managing multiple storage instances (e.g., for multiple databases)
3. **QueryBuilder** - Fluent API for constructing complex queries

### Basic Usage

```python
from at_common_util.db import Storage, StorageManager
from app.config import settings

# Option 1: Use the Storage class directly
storage = Storage()
storage.init(settings.DB_CONNECTION_URL)

# Option 2: Use the StorageManager for multiple database connections
default_storage = StorageManager.get_storage("default", settings.DB_CONNECTION_URL)
analytics_storage = StorageManager.get_storage("analytics", settings.ANALYTICS_DB_URL)

# Use the storage in your data access layer
async def get_user_by_id(user_id):
    from app.models import User
    return await default_storage.get_by_field(User, "id", user_id)

async def create_user(user_data):
    from app.models import User
    user = User(**user_data)
    return await default_storage.create(user)

async def update_user(user_id, update_data):
    from app.models import User
    return await default_storage.update_by_field(User, "id", user_id, update_data)

async def delete_user(user_id):
    from app.models import User
    return await default_storage.delete_by_field(User, "id", user_id)
```

### Transaction Support

For operations that require transaction support:

```python
from app.models import User, Profile

async def create_user_with_profile(user_data, profile_data):
    async with storage.transaction() as session:
        # Create user
        user = User(**user_data)
        session.add(user)
        await session.flush()  # Flush to get the user ID
        
        # Create profile with user ID reference
        profile = Profile(user_id=user.id, **profile_data)
        session.add(profile)
        
        # Transaction is automatically committed if no exceptions occur
    
    return user
```

### Query Builder API

For more complex queries, use the QueryBuilder:

```python
from at_common_util.db import QueryBuilder
from sqlalchemy import desc
from app.models import User

async def search_users(criteria):
    # Use the query builder to construct a complex query
    query = QueryBuilder.for_model(User) \
        .filter_by(is_active=True) \
        .filter(User.age > 18) \
        .order_by(desc(User.created_at)) \
        .group_by(User.role) \
        .limit(10) \
        .offset(20) \
        .build()
        
    # Execute the query using storage's session
    async with storage.get_session() as session:
        result = await session.execute(query)
        return result.scalars().all()
```

### Available Storage Methods

- `query(model_class, filters=None, sort=None, limit=None, offset=None)`: Query records with optional filtering, sorting, and pagination
- `find_one(model_class, filters=None)`: Find a single record matching the filters
- `create(model_obj)`: Create a new record
- `create_many(model_objects)`: Create multiple records in a transaction
- `update_by_field(model_class, field_name, field_value, update_data)`: Update a record by a field value
- `get_by_field(model_class, field_name, field_value)`: Get a record by a field value
- `delete_by_field(model_class, field_name, field_value)`: Delete a record by field value
- `delete_many_by_field(model_class, field_name, values)`: Delete multiple records by field values
- `count(model_class, filters=None)`: Count the number of records
- `dispose()`: Cleanup database connections
- `shutdown()`: Close all database connections when shutting down the app 
