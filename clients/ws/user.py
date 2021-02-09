import cbpro
from queue import Queue
from clients.keys import api_keys as keys
# This channel is a version of the full channel that only contains messages that include the authenticated user.
# Consequently, you need to be authenticated to receive any messages.


class Channel(cbpro.WebsocketClient):
    def __init__(self, url="wss://ws-feed.pro.coinbase.com", products=None, message_type="subscribe",
                 mongo_collection=None, should_print=True, auth=False, api_key="", api_secret="", api_passphrase="",
                 channels=None):
        super().__init__(url, products, message_type, mongo_collection, should_print, auth, api_key, api_secret,
                         api_passphrase, channels)
        self.msg_queue = Queue(maxsize=0)
        self.channels = ["user"]
        self.auth = True
        self.api_key = keys.key
        self.api_secret = keys.b64secret
        self.api_passphrase = keys.passphrase
        self.products = ['BTC-USD']

    def on_message(self, msg):
        self.msg_queue.put(msg)

    def on_close(self):
        print(f"-- Closed User Channel --")


channel = Channel()
channel.start()
