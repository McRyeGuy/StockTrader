from tda import auth, client
import json
from tda.orders.equities import equity_buy_limit
from tda.orders.common import Duration, Session
token_path = 'token'
api_key = '----your_api_key'
#redirect_uri = 'http://localhost'
account_id = "-your account id"


client = auth.client_from_token_file('token',api_key)

payload={
    "session": "NORMAL",
    "duration": "DAY",
    "orderType": "MARKET",
    #"price": "190.90",
    "orderLegCollection": [
        {
            "instruction": "BUY",
            "instrument": {
                "assetType": "EQUITY",
                "symbol": "CTRM"
            },
            "quantity": 1
        }
    ],
    "orderStrategyType": "SINGLE"
}
client.place_order(account_id, order_spec=payload)
