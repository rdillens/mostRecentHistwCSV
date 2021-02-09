import cbpro
from queue import Queue
# If you are only interested in match messages you can subscribe to the matches channel.
# This is useful when you're consuming the remaining feed using the level 2 channel.
#
# Please note that messages can be dropped from this channel.
# By using the heartbeat channel you can track the last trade id and fetch trades that you missed from the REST API.


class Channel(cbpro.WebsocketClient):
    def __init__(self, url="wss://ws-feed.pro.coinbase.com", products=None, message_type="subscribe",
                 mongo_collection=None,
                 should_print=True, auth=False, api_key="", api_secret="", api_passphrase="", channels=None):
        super().__init__(url, products, message_type, mongo_collection, should_print, auth, api_key, api_secret,
                         api_passphrase, channels)
        self.channels = ["matches"]
        self.msg_queue = Queue(maxsize=0)

    def on_message(self, msg):
        self.msg_queue.put(msg)


channel = Channel()
channel.start()
