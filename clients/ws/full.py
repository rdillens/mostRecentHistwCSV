import cbpro
from queue import Queue


class Channel(cbpro.WebsocketClient):
    def __init__(self, url="wss://ws-feed.pro.coinbase.com", products=None, message_type="subscribe",
                 mongo_collection=None,
                 should_print=True, auth=False, api_key="", api_secret="", api_passphrase="", channels=None):
        super().__init__(url, products, message_type, mongo_collection, should_print, auth, api_key, api_secret,
                         api_passphrase, channels)
        self.channels, self.products, self.msg_queue = ["full"], ["BTC-USD"], Queue(maxsize=0)

    def on_message(self, msg):
        self.msg_queue.put(msg)


channel = Channel()
