import cbpro
from queue import Queue
import helpful_methods as hm
# To receive heartbeat messages for specific products once a second subscribe to the heartbeat channel.
# Heartbeats also include sequence numbers and last trade ids that can be used to verify no messages were missed.
#
# // Heartbeat message
# {
#     "type": "heartbeat",
#     "sequence": 90,
#     "last_trade_id": 20,
#     "product_id": "BTC-USD",
#     "time": "2014-11-07T08:19:28.464459Z"
# }
hb_header = ['type', 'last_trade_id', 'product_id', 'sequence', 'time']


class Channel(cbpro.WebsocketClient):
    def __init__(self, url="wss://ws-feed.pro.coinbase.com", products=None, message_type="subscribe",
                 mongo_collection=None,
                 should_print=True, auth=False, api_key="", api_secret="", api_passphrase="", channels=None):
        super().__init__(url, products, message_type, mongo_collection, should_print, auth, api_key, api_secret,
                         api_passphrase, channels)
        self.output_file = 'output/heartbeat.csv'
        self.channels = ["heartbeat"]
        self.products = ["BTC-USD"]
        self.msg_queue = Queue(maxsize=60)
        self.header = hb_header
        self.msg = []

    def on_open(self):
        print('-- Subscribed to Heartbeat Channel! --')
        hm.gen_path('output')
        with open(self.output_file, 'w+') as csv:
            csv.write(str(', '.join(self.header) + '\n'))

    def on_message(self, msg):
        self.msg_queue.put(msg)
        for k, v in msg.items():
            self.msg.append(v)
            print(f'{v}', end=', ')
        print(self.msg)
        # with open(self.output_file, 'w+') as csv:
        #     csv.write()


channel = Channel()
