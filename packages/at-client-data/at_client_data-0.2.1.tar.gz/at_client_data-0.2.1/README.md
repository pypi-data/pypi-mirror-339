# at-client-data

Client library for AT data services.

## Installation

```bash
pip install at-client-data
```

## Usage

```python
from at_client_data import CoreClient, ExternalClient
from at_client_data.schema import QuoteGetRequest, StockListRequest

# Create a client instance
client = CoreClient(base_url="https://api.example.com")

# Get stock quotes
response = client.get_quote(QuoteGetRequest(symbol="AAPL"))
print(f"Current price: {response.price}")

# List stocks
stock_list = client.list_stocks(StockListRequest(limit=10))
for stock in stock_list.stocks:
    print(f"{stock.symbol}: {stock.name}")
```

## Features

- Client for accessing AT data services
- Schema definitions for requests and responses
- Support for stock quotes, listings, news, and more

## License

MIT 