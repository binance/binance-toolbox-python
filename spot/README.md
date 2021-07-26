# Binance Toolbox - Spot

## Preparation
1. It's required to install the `binance-connector` package

    ```shell
    pip install binance-connector
    ```
   
2. Some api endpoints requires sending a valid API-Key and signature, so in order for some scripts to work, please set up 
your account's api key pair as environment variables.

    Note: By default, the scripts uses Testnet's REST and Websocket as base urls.

    ```shell
    export BINANCE_API_KEY=<your_api_key>
    export BINANCE_API_SECRET=<your_secret_key>
    ```
   
## Scripts
You can find each script's purpose and instructions information within each script file.
Current available scripts:

- `place_order.py`
- `list_break_symbols.py`
- `check_order_update_latency.py`
- `manage_orderbook.py`
- `multi_subs_market_ws.py`

