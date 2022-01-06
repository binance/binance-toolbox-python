# Binance Toolbox Python

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
   
## License
MIT
