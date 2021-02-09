import cbpro
from queue import Queue
# The easiest way to keep a snapshot of the order book is to use the level2 channel.
# It guarantees delivery of all updates, which reduce a lot of the overhead required when consuming the full channel.
#
# {
#     "type": "snapshot",
#     "product_id": "BTC-USD",
#     "bids": [["10101.10", "0.45054140"]],
#     "asks": [["10102.55", "0.57753524"]]
# }
# When subscribing to the channel it will send a message with the type snapshot and the corresponding product_id.
# bids and asks are arrays of [price, size] tuples and represent the entire order book.
#
# {
#   "type": "l2update",
#   "product_id": "BTC-USD",
#   "time": "2019-08-14T20:42:27.265Z",
#   "changes": [
#     [
#       "buy",
#       "10101.80000000",
#       "0.162567"
#     ]
#   ]
# }
# Subsequent updates will have the type l2update. The changes property of l2updates is an array with
# [side, price, size] tuples.
# The time property of l2update is the time of the event as recorded by our trading engine.
# Please note that size is the updated size at that price level, not a delta.
# A size of "0" indicates the price level can be removed.


class Channel(cbpro.WebsocketClient):
    def __init__(self, url="wss://ws-feed.pro.coinbase.com", products=None, message_type="subscribe",
                 mongo_collection=None,
                 should_print=True, auth=False, api_key="", api_secret="", api_passphrase="", channels=None):
        super().__init__(url, products, message_type, mongo_collection, should_print, auth, api_key, api_secret,
                         api_passphrase, channels)
        self.channels = ['level2']
        self.msg_queue = Queue(maxsize=0)

    def on_message(self, msg):
        self.msg_queue.put(msg)


channel = Channel()
channel.start()
