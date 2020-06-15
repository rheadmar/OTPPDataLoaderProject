import configparser

class configHandler():
    #This is the main class I am using to handle anything that could be considered config.
    #TODO this could benefit from a bit more consistency in terms of access methods
    def __init__(self,file = "conf\\server.conf"):
        self.config = configparser.ConfigParser()
        self.config.read(file)
        self.inter = int(self.config['DEFAULT']['loadinterval'])
        self.intervalString = str(self.inter) + "min"
        self.loadFromFile = self.config['LOADOPTIONS']['loadFromFile']=='True'
        self.loadFile = ""
        self.requestPort =  int(self.config['SERVERPROPERTY']['port'])
        self.tickers = eval(self.config['DEFAULT']['tickers'])
        self.outputfiles = eval(self.config['OUTPUTCONFIG']['outputconfigs'])
        
    def applyOverides(self, overides):
        for i in overides.keys():
            if not overides[i] is None:
                if i == "tickers":
                    self.tickers = eval(overides[i])
                elif i == 'loadinterval':
                    self.inter = int(overides[i])
                    self.intervalString = str(self.inter) + "min"
                elif i == 'loadfile':
                    self.loadFile=overides[i]
                    self.loadFromFile = True
                elif i == "port":
                    self.config['SERVERPROPERTY']['port']=overides[i]
                    self.port = overides[i]
                    self.requestPort = overides[i]
        