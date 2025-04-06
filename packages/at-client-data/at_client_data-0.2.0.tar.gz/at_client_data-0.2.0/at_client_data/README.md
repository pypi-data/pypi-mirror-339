# AT Client Data

A Python package for accessing AT data API. Contains client and schema modules.

## Installation

```bash
pip install at-client-data
```

## Usage

```python
from at_client_data.client import BaseClient
from at_client_data.schema import Quote

# Use the client to fetch data
client = BaseClient(api_key="your_api_key")
# ...
```

## Components

- `schema`: Data models and schemas for the AT data API
- `client`: Client classes for making API requests

## License

MIT