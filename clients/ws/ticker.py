import cbpro
from queue import Queue
# The ticker channel provides real-time price updates every time a match happens.
# It batches updates in case of cascading matches, greatly reducing bandwidth requirements.
#
# {
#     "type": "ticker",
#     "trade_id": 20153558,
#     "sequence": 3262786978,
#     "time": "2017-09-02T17:05:49.250000Z",
#     "product_id": "BTC-USD",
#     "price": "4388.01000000",
#     "side": "buy", // Taker side
#     "last_size": "0.03000000",
#     "best_bid": "4388",
#     "best_ask": "4388.01"
# }
# Please note that more information will be added to messages from this channel in the near future.


class Channel(cbpro.WebsocketClient):
    def __init__(self, url="wss://ws-feed.pro.coinbase.com", products=None, message_type="subscribe",
                 mongo_collection=None,
                 should_print=True, auth=False, api_key="", api_secret="", api_passphrase="", channels=None):
        super().__init__(url, products, message_type, mongo_collection, should_print, auth, api_key, api_secret,
                         api_passphrase, channels)
        self.channels = ["ticker"]
        self.msg_queue = Queue(maxsize=0)

    def on_message(self, msg):
        self.msg_queue.put(msg)


channel = Channel()
channel.start()
