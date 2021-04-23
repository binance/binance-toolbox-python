# Binance Toolbox - Coin Futures

## Preparation
Some api endpoints requires sending a valid API-Key and signature, so in order for some scripts to work, please set up 
your account's api key pair as environment variables.

Note: By default, the scripts uses Testnet's REST and Websocket as base urls.

```shell
export BINANCE_API_KEY="<your_api_key>"
export BINANCE_API_SECRET="<your_secret_key>"
```

## Scripts
Each script contains purpose and instructions information. Current available scripts:

- test_user_data_stream_request.py;