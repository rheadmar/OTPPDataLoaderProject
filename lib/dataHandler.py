from alpha_vantage.timeseries import TimeSeries
import pandas
import json
import datetime
import os
import logging

class dataHandler():
    '''This class is the main class designed for handling all data. It maintains a pandas data frame represnting all time series data related to a given ticker.
    '''
    def __init__(self,ticker,config,ts):
        self.conf = config
        self.ticker = ticker
        if config.loadFromFile:
            self.loadTickerFromFile(ticker,config.loadFile)
        else:
            #TODO add meta checking for errors
            self.rawtik, self.meta = ts.get_intraday(symbol=ticker,interval = config.intervalString)
            self.dataframe = pandas.DataFrame.from_dict(self.rawtik).transpose()
            self.createSignalFrame(self.dataframe[config.config['DEFAULT']['pricekey']].astype(float).to_frame())
            self.writeFiles(self.conf.config['DEFAULT']['outputDirectory'])
        
    def loadTickerFromFile(self, ticker, filepath):
        #TODO: add File Validation to ensure its a valid file
        pandas.read_csv(filepath)
        data = pandas.read_csv(filepath)
        data.datetime = pandas.to_datetime(data.datetime)
        data = data.set_index("datetime")
        data = data.rename(columns={"datetime":"index","price":"S"})
        self.signal_frame = self.appendCalculatedFields(data)
        
    def appendCalculatedFields(self,df):
        df['S_avg'] = df.iloc[:,0].rolling(window = 60*24 // self.conf.inter ,min_periods=1).mean()
        df['S_sig'] = df.iloc[:,0].rolling(window = 60*24 // self.conf.inter ,min_periods=1).std()
        df["trades"] = df.apply(lambda x: self.calculateTrade(x),axis =1,raw=True)
        df["position"] = df["trades"].cumsum()
        df["costbasis"] = (df["trades"]*df["S"]).cumsum()
        df["pnl"] = df["position"]*df["S"]-df["costbasis"]
        return df
        
    def createSignalFrame(self,sourcedata):
        df = sourcedata.rename(columns={self.conf.config['DEFAULT']['pricekey']:"S"})
        df.index = pandas.to_datetime(df.index)
        df = self.appendCalculatedFields(df)
        self.signal_frame = df
        
    def calculateTrade(self,x):
        #x[0] = price
        #x[1] = moving average
        #x[2] = standard deviation
        if x[0]>x[1]+x[2]:
            return 1
        if x[0]<x[1]-x[2]:
            return -1
        return 0
    
    def processUpdate(self,update):
        if update[0] > datetime.timedelta(minutes=self.conf.inter)+self.signal_frame.index.max():
            self.appendItem(update)
        
    def appendItem(self, item):
        agg = self.signal_frame[self.signal_frame.index > item[0]-datetime.timedelta(1)]["S"]
        trade = self.calculateTrade([item[1],agg.mean(),agg.std()])
        pos = self.signal_frame.tail(1)["position"].array[0]+trade
        costbasis = self.signal_frame.tail(1)["costbasis"].array[0] + trade*item[1]
        PnL = pos*item[1]-costbasis
        addition = pandas.DataFrame([[item[1],agg.mean(),agg.std(),trade,pos,PnL,costbasis]],index = [item[0]], columns = self.signal_frame.columns)
        self.signal_frame = self.signal_frame.append(addition)
        self.mostRecent = addition
        
    def writeFiles(self,outputpath):
        for key in self.conf.outputfiles:
            outputCols = eval(self.conf.config['OUTPUTCONFIG'][key])
            output = self.signal_frame.reset_index().rename(columns=outputCols)[outputCols.values()]
            output.to_csv(os.path.join(outputpath,self.ticker.replace(":","") +"_"+ key + ".csv"),index=False)
            
    def getPrice(self, datetime):
        if datetime < self.signal_frame.index.min():
            return pandas.DataFrame(["no data"],index = [self.ticker],columns = ["signal"])
        idx = self.signal_frame[self.signal_frame.index < datetime].index.max()
        val = self.signal_frame.loc[idx]["S"]
        return pandas.DataFrame([val],index = [self.ticker],columns = ["price"])
    
    def getSignal(self, datetime):
        if datetime < self.signal_frame.index.min():
            return pandas.DataFrame(["no data"],index = [self.ticker],columns = ["signal"])
        idx = self.signal_frame[self.signal_frame.index < datetime].index.max()
        val = self.signal_frame.loc[idx]["trades"]
        return pandas.DataFrame([int(val)],index = [self.ticker],columns = ["signal"])