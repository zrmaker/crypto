import gdax
import numpy as np
from array import *
import json
import datetime
import time
import sys
#import matplotlib.pyplot as plt
from matplotlib.finance import candlestick2_ohlc
#import plotly
#import plotly.plotly as py
#import plotly.graph_objs as go

def __format_float__(num):
    return "%.2f" % num

def __format_time__(t):
    t2 = datetime.datetime.strptime(t, "%Y-%m-%dT%H:%M:%S.%fZ" )
    s = t2.strftime('%Y-%m-%d %H:%M:%S.%f')
    return s[:-3]

def __column__(matrix, i):
    return [row[i] for row in matrix]

# plotly.tools.set_credentials_file(username='zrmaker', api_key='p834WvtvEtuzG81A6f2n')

public_client = gdax.PublicClient()

datac=[]
t=0
lasttimec=0
try:
    while 1:
        sys.stdout.write('.')
        sys.stdout.flush()
        try:
            tmp = public_client.get_product_ticker(product_id='ETH-USD')
            datas=json.loads(json.dumps(tmp))
        except:
            continue
        try:
            tmp=public_client.get_product_historic_rates('ETH-USD')
            if type(tmp) == list:
                print(tmp[0])
        except:
            continue
        try:
            pric=round(float(datas["price"]),2)
            timec=__format_time__(datas["time"])
            if timec!=lasttimec:
                lasttimec=timec
                # sys.stdout.write("\033[F") # Cursor up one line
                sys.stdout.write("\r\033[K") # Clear to the end of line
                sys.stdout.write('\r'+str(timec)+' '+str(__format_float__(pric))+'\n')
        except:
            continue
except KeyboardInterrupt:
    pass
datad = json.dumps(datac)
print(len(datad))
f = open("dict.json", "w")
f.write(datad)
f.close()
exit()

