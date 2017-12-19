import numpy as np
import urllib.request
import json

class nanopool():
    def __init__(self):
        self.address='0x1b40335c8d882dad3fd3180f5ce457802c8a8cd8'
        self.head='https://api.nanopool.org/v1/eth/'
        self.agent={'User-Agent': 'Chrome/63.0.3239.84'}
       
    def read(req):
        s = urllib.request.urlopen(req).read()
        return json.loads(s.decode("utf-8"))
        
    def account_balance(self):
        req=urllib.request.Request(self.head+'balance/'+self.address, \
                    headers = self.agent)
        ss = nanopool.read(req)
        return ss["data"]
    
    def average_hashrate(self):
        # 1h, 3h, 6h, 12h, 24h
        req=urllib.request.Request(self.head+'avghashrate/'+self.address, \
                    headers = self.agent)
        ss = nanopool.read(req)
        return np.fromiter(iter(ss["data"].values()),dtype=float)
    
if __name__ == '__main__':
    n=nanopool()
    print(n.average_hashrate())