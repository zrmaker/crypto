import gdax
import numpy as np
import json
import datetime
import time

class gdax_import():


    def __init__(self):
        self.price=0.
        self.time=0.
        self.public_client = gdax.PublicClient()

    def __format_time__(t):
        t1 = datetime.datetime.strptime(t, "%Y-%m-%dT%H:%M:%S.%fZ")
        t2 = time.mktime(t1.timetuple())+(t1.microsecond/1000000.)-float(time.altzone)
        s = datetime.datetime.fromtimestamp(t2).strftime('%Y-%m-%d %H:%M:%S.%f')
        return s[:-3]

    def read_current(self):

        try:
            tmp = self.public_client.get_product_ticker(product_id='ETH-USD')
            datas=json.loads(json.dumps(tmp))
            self.price = round(float(datas["price"]), 2)
            self.time = gdax_import.__format_time__(datas["time"])
        except:
            self.price=0.
            self.time=0.
        return self.price,self.time

    def read_history(self):
        try:
            tmp=self.public_client.get_product_historic_rates('ETH-USD')
            if type(tmp) != list:
                tmp=0
        except:
            tmp=0
        return tmp