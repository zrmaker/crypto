import numpy as np
import urllib.request
import json
import matplotlib.pyplot as plt
import datetime
from technical_indicatiors import technical_indicators

class nanopool():
    def __init__(self):
        self.eth_address='0x1b40335c8d882dad3fd3180f5ce457802c8a8cd8'
        self.pasc_address = '86646.93a45081d188bbbb'
        self.head='https://api.nanopool.org/v1/'
        self.agent={'User-Agent': 'Chrome/63.0.3239.84'}
        self.TI=technical_indicators()
        
    def read(self, req):
        s = urllib.request.urlopen(req).read()
        return json.loads(s.decode("utf-8"))
        
    def account_balance(self, ticker):
        if ticker == 'eth':
            req=urllib.request.Request(self.head+ticker+'/balance/'+self.eth_address, headers = self.agent)
        else:
            req=urllib.request.Request(self.head+ticker+'/balance/'+self.pasc_address, headers = self.agent)
        ss = self.read(req)
        return ss["data"]
    
    def average_hashrate(self, ticker):
        # 1h, 3h, 6h, 12h, 24h
        if ticker == 'eth':
            req=urllib.request.Request(self.head+ticker+'/avghashrate/'+self.eth_address, headers = self.agent)
        else:
            req=urllib.request.Request(self.head+ticker+'/avghashrate/'+self.pasc_address, headers = self.agent)
        ss = self.read(req)
        return np.fromiter(iter(ss["data"].values()),dtype=float)
    
    def chart_data(self, ticker):
        # 1h, 3h, 6h, 12h, 24h
        if ticker == 'eth':
            req=urllib.request.Request(self.head+ticker+'/hashratechart/'+self.eth_address, headers = self.agent)
        else:
            req=urllib.request.Request(self.head+ticker+'/hashratechart/'+self.pasc_address, headers = self.agent)
        ss = self.read(req)
        print(ss)
        return ss["data"]
    
    def history(self, ticker):
        # 1h, 3h, 6h, 12h, 24h
        if ticker == 'eth':
            req=urllib.request.Request(self.head+ticker+'/history/'+self.eth_address, headers = self.agent)
        else:
            req=urllib.request.Request(self.head+ticker+'/history/'+self.pasc_address, headers = self.agent)
        ss = self.read(req)
        print(ss)
        return ss["data"]
    
    def plot_chart(self, ticker):
        data=self.chart_data(ticker)
        data2=self.history(ticker)
        t,t2,shares,hr,hr2=[],[],[],[],[]
        for i in range(len(data)):
            t=np.append(t,datetime.datetime.fromtimestamp(data[i]['date']).strftime('%H:%M'))
            # t=np.append(t,data[i]['date'])
            shares=np.append(shares,data[i]['shares'])
            hr=np.append(hr,data[i]['hashrate']/1000.)
            
        for i in range(len(data2)):
            t2 = np.append(t2, datetime.datetime.fromtimestamp(data2[i]['date']).strftime('%H:%M'))
            hr2 = np.append(hr2, data2[i]['hashrate'])
        t=np.flip(t,0)
        t2=np.flip(t2,0)
        shares=np.flip(shares,0)
        hr=np.flip(hr,0)
        hr2=np.flip(hr2,0)
        mahr=self.TI.MAlist(hr2,12)
        # print(len(t),len(shares),len(hr))
        f,(ax1,ax2)=plt.subplots(2,1,figsize=(20, 8))
        if ticker == 'eth':
            print(hr2[-72:], mahr[-72:])
            print(t[-72:], t2[-72:])
            ax1.plot(t[-72:],hr[-72:],t2[-72:],hr2[-72:],t2[-72:],mahr[-72:])
        else:
            print(hr2[-72:],mahr[-72:])
            print(t[-72:],t2[-72:])
            ax1.plot(hr2[-72:])
            ax1.plot(mahr[-72:])
        ax2.bar(t[-72:],shares[-72:])
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
        plt.show()
        
if __name__ == '__main__':
    print(nanopool().plot_chart('pasc'))