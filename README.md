# Binance Toolbox

Contains simple scripts to help the API users validate REST and STREAMING API endpoints.
The scripts can be for Spot or Futures product, please go to the respective directory's README.md to see
the requirements and each script's description.

Current structure:
```bash
.
├── README.md
├── coin_futures
│   ├── README.md
│   └── test_user_data_stream_request.py
└── spot
    ├── README.md
    ├── check_order_update_latency.py
    ├── config.py
    ├── list_break_symbols.py
    ├── manage_orderbook.py
    └── place_order.py
```