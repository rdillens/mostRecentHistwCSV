import cbpro
from queue import Queue
# The status channel will send all products and currencies on a preset interval.
#
# // Status Message
# {
#     "type": "status",
#     "products": [
#         {
#             "id": "BTC-USD",
#             "base_currency": "BTC",
#             "quote_currency": "USD",
#             "base_min_size": "0.001",
#             "base_max_size": "70",
#             "base_increment": "0.00000001",
#             "quote_increment": "0.01",
#             "display_name": "BTC/USD",
#             "status": "online",
#             "status_message": null,
#             "min_market_funds": "10",
#             "max_market_funds": "1000000",
#             "post_only": false,
#             "limit_only": false,
#             "cancel_only": false
#         }
#     ],
#     "currencies": [
#         {
#             "id": "USD",
#             "name": "United States Dollar",
#             "min_size": "0.01000000",
#             "status": "online",
#             "status_message": null,
#             "max_precision": "0.01",
#             "convertible_to": ["USDC"], "details": {}
#         },
#         {
#             "id": "USDC",
#             "name": "USD Coin",
#             "min_size": "0.00000100",
#             "status": "online",
#             "status_message": null,
#             "max_precision": "0.000001",
#             "convertible_to": ["USD"], "details": {}
#         },
#         {
#             "id": "BTC",
#             "name": "Bitcoin",
#             "min_size":" 0.00000001",
#             "status": "online",
#             "status_message": null,
#             "max_precision": "0.00000001",
#             "convertible_to": []
#         }
#     ]
# }


class Channel(cbpro.WebsocketClient):
    def __init__(self, url="wss://ws-feed.pro.coinbase.com", products=None, message_type="subscribe",
                 mongo_collection=None,
                 should_print=True, auth=False, api_key="", api_secret="", api_passphrase="", channels=None):
        super().__init__(url, products, message_type, mongo_collection, should_print, auth, api_key, api_secret,
                         api_passphrase, channels)
        self.msg_queue = Queue(maxsize=0)
        self.currencies = []
        self.products = []
        self.channels = ["status"]

    def on_message(self, msg):
        self.msg_queue.put(msg)
        try:
            if 'currencies' in msg:
                if msg['currencies'] != self.currencies:
                    self.currencies = msg['currencies']
                    print('Currencies updated from status channel')
            if 'products' in msg:
                if msg['products'] != self.products:
                    self.products = msg['products']
                    print('Products updated from status channel')
        except Exception as inst:
            print(f'{type(inst)}: {inst} Unable process status message.')
            raise


channel = Channel()
channel.start()
