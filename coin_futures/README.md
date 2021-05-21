# Binance Toolbox - Coin Futures

## Preparation
Some api endpoints requires sending a valid API-Key and signature, therefore in order for some scripts to work, please 
set up your account's api key pair as environment variables.

```shell
export BINANCE_API_KEY=<your_api_key>
export BINANCE_API_SECRET=<your_secret_key>
```

Note: By default, the scripts uses Testnet's REST and Websocket as base urls.

## Scripts
Each script file contains its purpose and instructions information. Current available scripts:

- test_user_data_stream_request.py
- cancel_batch_orders.py