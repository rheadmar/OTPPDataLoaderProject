import json
import datetime
import os
import json
import sys
import pandas
import logging
from alpha_vantage.timeseries import TimeSeries
from lib.dataHandler import dataHandler
from lib.finhubSubscription import finhubSubscirption
from lib.requestListener import requestListener
from lib.configHandler import configHandler

class Manager():
    #This class is the general overseer for the project and instantiates all other classes and delegates function calls to where they belong.
    #it acts as a general starting point for where all requests should go.
    def __init__(self,overrides):
        self.stparams = overrides
        self.dataHandlers = {}
        self.conf = configHandler("conf\\server.conf")
        self.conf.applyOverides(overrides)
        self.provider = finhubSubscirption(self.processUpdate,self.conf.config['KEYS']['finhubKey'], self.getSubscirbeStringSet())
        self.ts = TimeSeries(self.conf.config['KEYS']['alphaVantageKey'])
        for i in self.conf.tickers:
            self.dataHandlers[i] = dataHandler(i,self.conf,self.ts)
        self.reqlist = requestListener(self.conf,self)
    
    def processUpdate(self,update):
        itemDict = json.loads(update)
        if "data" not in itemDict.keys():
            logging.info("non update message received")
            return 0
        item = [datetime.datetime.fromtimestamp(itemDict["data"][0]['t'] /1e3),itemDict["data"][0]['p']]
        sym = itemDict["data"][0]['s']
        if sym in self.dataHandlers.keys():
            self.dataHandlers[sym].processUpdate(item)
        else:
            logging.info("unknown ticker encountered, continuing operations")
            
    def getSubscirbeStringSet(self):
        res = []
        for item in self.conf.tickers:
            res.append('{"type":"subscribe","symbol":"'+ item +'"}')
        return res
            
        
    def reset(self):
        self.__init__(self.stparams)
        return json.dumps("0")
    
    def addTicker(self, ticker):
        try:
            if ticker in self.dataHandlers.keys():
                return json.dumps(1)
            self.conf.tickers.append(ticker)
            self.dataHandlers[ticker]=dataHandler(ticker,self.conf,self.ts)
            self.provider.add_subscription(ticker)
            return json.dumps(0)
        except:
            return json.dumps(2)

    def delTicker(self, ticker):
        if not ticker in self.conf.tickers:
            return json.dumps(1)
        self.dataHandlers.pop(ticker)
        self.conf.tickers.remove(ticker)
        return json.dumps(0)
    
    def getPrices(self, datetime):
        return pandas.concat(map(lambda x: x.getPrice(datetime),self.dataHandlers.values())).to_json()
        
    def getSignals(self, datetime):
        return pandas.concat(map(lambda x: x.getSignal(datetime),self.dataHandlers.values())).to_json()
    