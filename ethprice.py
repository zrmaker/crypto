import gdax
import numpy as np
import pandas as pd
from array import *
import json
import datetime
import time
import sys
# import matplotlib.pyplot as plt
# from matplotlib.finance import candlestick2_ohlc
# import plotly
# import plotly.plotly as py
# import plotly.graph_objs as go
# import threading
# from threading import Thread
from src.from_gdax import gdax_import
from src.technical_indicatiors import technical_indicators

def __print__():
    sys.stdout.write('.')
    sys.stdout.flush()
    
def __format_float__(num):
    return "%.2f" % num

def __format_time__(time):
    return datetime.datetime.fromtimestamp(time). \
        strftime('%H:%M')

def __column__(matrix, i):
    return [row[i] for row in matrix]

def __list_pd_conv__(thelist):
    return pd.Series((v for v in thelist))

# plotly.tools.set_credentials_file(username='zrmaker', api_key='p834WvtvEtuzG81A6f2n')

def main():
    datac=[]
    t=0
    lasttimec=0
    lasthis=0
    gdaximport=gdax_import()
    techind=technical_indicators()
    while 1:
        __print__()

        pric,timec=gdaximport.read_current()
        if timec!=lasttimec and pric!=0 and timec!=0:
            lasttimec=timec
            # sys.stdout.write("\033[F") # Cursor up one line
            sys.stdout.write("\r\033[K") # Clear to the end of line
            sys.stdout.write('\r'+str(timec)+' '+ \
                             str(__format_float__(pric))+'\n')

        __print__()
        history=gdaximport.read_history()
        if history!=0:
            if history[0][0] != lasthis:
                lasthis = history[0][0]
                tmp=list(reversed(__column__(history,4)))
                ma = techind.MA(__list_pd_conv__(tmp),5)
                sys.stdout.write("\r\033[K")
                sys.stdout.write('\rMA5: '+__format_time__(history[0][0])+\
                                 ' '+str(__format_float__(ma[399]))+'\n')
if __name__=='__main__':
    main()

