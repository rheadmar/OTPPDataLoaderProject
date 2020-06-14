import threading
import websocket
import json
import logging

class finhubSubscirption():
    #TODO: this class needs to be cleaned up and properly extend the WebSocket App instead of being a wrapper of it using
    #so many lambda functions.
    def __init__(self,udpatefunc,finhubToken,subscriptionset):
        self.ws = websocket.WebSocketApp("wss://ws.finnhub.io?token="+finhubToken,
                                         on_message = lambda x,y: self.on_message(x,y),
                                         on_error = lambda x,y: self.on_error(x,y),
                                         on_close = lambda x: self.on_close(x)
                                        )
        
        self.updateFunction = udpatefunc
        self.finhubToken = finhubToken
        self.subscriptionset = subscriptionset
        self.additions = []
        self.thr = threading.Thread(target=self.run,name="finhubSubscirption",daemon=True)
    
    def start_daemon(self):
        self.thr.start()
        
    def run(self):
        self.ws.on_open = lambda x: self.on_open(x)
        self.ws.run_forever()
    
    def on_message(self,ws, message):
        self.updateFunction(message)
        self.subscribe_to_new_tickers()
    
    def subscribe_to_new_tickers(self):
        for i in self.additions:
            self.ws.send(i)
        self.additions = []
    
    def add_subscription(self,item):
        self.additions.append(item)
    
    def on_error(self,ws, error):
        logging.error(error)

    def on_close(self,ws):
        logging.info("### connection to Alpha Vantage Closed ###")

    def on_open(self,ws):
        for item in self.subscriptionset:
            self.ws.send(item)
            logging.info("subscirbed with string {}".format(item))