import argparse
from lib.Manager import Manager
import sys 

def main(args):
	try:
		mana_args = vars(args)
		for i in list(mana_args.keys()):
			if mana_args[i] is None:
				mana_args.pop(i)
		if not mana_args["loadinterval"] in ["5","15","30","60"]:
			print("invalid load interval detected {}".format(mana_args["loadinterval"]))
			sys.exit(1)
		mana = Manager(mana_args)
		mana.provider.start_daemon()
		mana.reqlist.start_server()
	except KeyboardInterrupt:
		sys.exit(0)

if __name__ == "__main__":
	argparser = argparse.ArgumentParser(description="""This is the host process for a stock market signal generator.
	Upon startup this application will gather data at a regular interval to calculate whether stock should be purchased or sold.""")
	argparser.add_argument("--tickers",dest="tickers", metavar="['IBM','BBM']",help='These are the tickers for which data will be gathered and accumulated')
	argparser.add_argument("--port",dest="port", metavar='8052',default = '8000',help='This is the port that the server will be accessable on')
	argparser.add_argument("--reload",dest="loadfile", metavar='mycsv.csv',help='This option allows  you to specify a file that will be used for reloading data.')
	argparser.add_argument("--minutes",dest="loadinterval", metavar='15',default = "5",help='This can be 5,15,30 or 60 and represents the number of minutes between updates to the data signals')
	args = argparser.parse_args()
	main(args)