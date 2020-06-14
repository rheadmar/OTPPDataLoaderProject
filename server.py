import argparse
from lib.Manager import Manager

def main(args):
	#print(args)
	mana_args = vars(args)
	for i in list(mana_args.keys()):
		if mana_args[i] is None:
			mana_args.pop(i)
	mana = Manager(mana_args)
	mana.provider.start_daemon()
	mana.reqlist.start_server()

if __name__ == "__main__":
	argparser = argparse.ArgumentParser(description="""This is the host process for a stock market signal generator.
	Upon startup this application will gather data at a regular interval to calculate whether stock should be purchased or sold.""")
	argparser.add_argument("--tickers",dest="tickers", metavar='IBM BBM',help='These are the tickers for which data will be gathered and accumulated')
	argparser.add_argument("--port",dest="port", metavar='8052',default = 8000,help='This is the port that the server will be accessable on')
	argparser.add_argument("--reload",dest="reload", metavar='mycsv.csv',help='This option allows  you to specify a file that will be used for reloading data.')
	argparser.add_argument("--minutes",dest="interval", metavar='15',default = 5,help='This can be 5,15,30 or 60 and represents the number of minutes between updates to the data signals')
	args = argparser.parse_args()
	main(args)