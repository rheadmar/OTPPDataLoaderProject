import argparse
import asyncio
import websockets
import json
import datetime
import pandas

def main(arguments):
	client_args = vars(arguments)
	for i in list(client_args.keys()):
		if client_args[i] is None:
			client_args.pop(i)
	print(client_args)
	uri = uri = "ws://"+client_args['serverAdd']
	if "price" in client_args.keys():
		reqtime = datetime.datetime.strptime(client_args["price"],"%Y-%m-%d-%H:%M")
		req = json.dumps({'action' : 'getPrices', 'date' : reqtime.strftime("%Y/%m/%d %H:%M:%S.%f")})
	elif "signals" in client_args.keys():
		reqtime = datetime.datetime.strptime(client_args["signals"],"%Y-%m-%d-%H:%M")
		req = json.dumps({'action' : 'getSignals', 'date' : reqtime.strftime("%Y/%m/%d %H:%M:%S.%f")})
	elif "delticker" in client_args.keys():
		req = json.dumps({'action' : 'delTicker', 'ticker' : client_args["delticker"]})
	elif "newticker" in client_args.keys():
		req = json.dumps({'action' : 'addTicker', 'ticker' : client_args["newticker"]})
	elif "reset" in client_args.keys():
		req = json.dumps({'action' : 'reset'})
	else:
		return 1
	try:
		asyncio.get_event_loop().run_until_complete(send_request(uri,req))
	except:
		#TODO add send Email code here
		exit(1)


async def send_request(uri,req):
    async with websockets.connect(uri) as websocket:
        request = req
        await websocket.send(request)
        print(f"> {request}")
        response = await websocket.recv()
        print("got response:{res}".format(res= response))



if __name__ == "__main__":
	argparser = argparse.ArgumentParser(description="""This is a script which connects and can be used to query or modify a host process that is building signals for wether to buy or sell stocks.""")
	group = argparser.add_mutually_exclusive_group()
	group.add_argument("--price",dest="price",metavar = "YYYY-MM-DD-HH:MM",default = None,help='These are the tickers for which data will be gathered and accumulated')
	group.add_argument("--signal",dest="signals",metavar = "YYYY-MM-DD-HH:MM", default = None,help='This call will return the most recent data for all stocks that were subscribed at the given time')
	argparser.add_argument("--server_address",dest="serverAdd",metavar='192.168.0.1:8052',default = "localhost:8000",help='This is the IP address and port at which you can reach the server you are attempting to access data from.')
	group.add_argument("--del_ticker",dest="delticker",metavar='AAPL',help='This call will remove monitoring for a given ticker.Return codes 0=success, 1=server error, 2=ticker not found')
	group.add_argument("--add_ticker",dest="newticker",metavar='AAPL',help='This will inform the server to start monitoring this ticker and report signals for this ticker. Return code 0=success, 1=error, 2=invalid ticker')
	group.add_argument("--reset",dest="reset",action='store_const',const = True, default = None,help='Informs the server to reload all data from source vendors and recalculates signals')
	args = argparser.parse_args()
	main(args)
