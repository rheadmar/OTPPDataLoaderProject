import json
import asyncio
import websockets
import datetime
import pandas

class requestListener():
    def __init__(self,conf,manager):
        self.conf = conf
        self.manager = manager

    async def service_request(self, websocket, path):
        request = await websocket.recv()
        req = json.loads(request)
        if req['action']=="reset":
            res = self.manager.reset()
        elif req['action']=="addTicker":
            res = self.manager.addTicker(req["ticker"])
        elif req['action']=="delTicker":
            res = self.manager.delTicker(req["ticker"])
        elif req['action']=="getPrices":
            date = datetime.datetime.strptime(req['date'],"%Y/%m/%d %H:%M:%S.%f")
            res = self.manager.getPrices(date)
        elif req['action']=="getSignals":
            date = datetime.datetime.strptime(req['date'],"%Y/%m/%d %H:%M:%S.%f")
            res = self.manager.getSignals(date)
        else:
            res = json.dumps("Unknown Command")
        await websocket.send(res)

    def start_server(self):
        start_server = websockets.serve(self.service_request, "localhost", self.conf.requestPort)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()