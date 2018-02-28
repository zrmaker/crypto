import numpy as np
import pandas as pd

class technical_indicators:
    def __init__(self):
        self.alpha = .35
        self.BBands_param = [20, 2]
        self.RSI_param = 14
        self.MACD_param = [12, 26, 9]
        self.STOCH_param = [14, 3]
        self.ATR_param = 14
        self.DMI_param = 14
        self.ADX_param = 14
        self.MFI_param = 14

    def MA(self, adj_close, window_length):
        if window_length > len(adj_close): window_length = len(adj_close)
        return pd.Series(adj_close).rolling(window = window_length).mean().tolist()

    def EMA(self, adj_close, window_length):
        if window_length > len(adj_close): window_length = len(adj_close)
        self.alpha = 2 / (1 + window_length)
        ema_list = self.MA(adj_close[:window_length],window_length)
        for i in range(window_length, len(adj_close)):
            ema_list.append((adj_close[i]-ema_list[-1])*self.alpha+ema_list[-1])
        return ema_list
    
    def EMA_old(self, adj_close, window_length):
        if window_length > len(adj_close): window_length = len(adj_close)
        self.alpha = 2 / (1 + window_length)
        ema_list =  adj_close[-window_length:]
        size_ = len(ema_list)
        sum_ = .0
        for i in range(size_):
            sum_ += self.alpha * ema_list[i] * (1-self.alpha)**(size_-1-i) 
        return sum_ / (1 - (1 - self.alpha)**size_)

    def std_dev(self, adj_close, window_length):
        if window_length > len(adj_close): window_length = len(adj_close)
        std_list = []
        for i in range(window_length-1,len(adj_close)):
            std_list.append(np.std(np.array(adj_close[i-window_length+1:i+1])))
        return std_list
    
    def BBands(self, adj_close):
        ma = self.MA(adj_close, self.BBands_param[0])
        while np.isnan(ma[0]): ma.pop(0)
        ma = np.array(ma)
        sigma = np.array(self.std_dev(adj_close, self.BBands_param[0]))
        lb = ma - self.BBands_param[1] * sigma
        ub = ma + self.BBands_param[1] * sigma
        percent_b = (adj_close[-1]-lb) / 2 / self.BBands_param[1] / sigma
        bandwidth = 2 * self.BBands_param[1] * sigma / ma
        return lb, ub, percent_b, bandwidth

    def change(self, adj_close):
        return [x-y for x,y in zip(adj_close[1:],adj_close)]
    '''
    if RSI > 70:
        indicator = 'Overbought'
    elif RSI < 30:
        indicator = 'Oversold'
    '''

    def RSI(self, adj_close):
        rs_list = adj_close[:self.RSI_param+1]
        change_list = np.array(self.change(rs_list))
        avg_gain = np.sum(change_list[change_list>0])/self.RSI_param
        avg_loss = np.sum(change_list[change_list<0])/self.RSI_param
        RSI = 100 - 100 / (1 + avg_gain/-avg_loss)
        for i in range(self.RSI_N+1,len(adj_close)):
            tmp = self.change([adj_close[i-1],adj_close[i]]).pop()
            if tmp > 0:
                avg_gain = (avg_gain*(self.RSI_param-1) + tmp) / self.RSI_param
                avg_loss = avg_loss*(self.RSI_param-1)/self.RSI_param
            elif tmp < 0:
                avg_gain = avg_gain*(self.RSI_param-1)/self.RSI_param
                avg_loss = (avg_loss*(self.RSI_param-1) + tmp) / self.RSI_param
            RSI = np.append(RSI, 100 - 100 / (1 + avg_gain/-avg_loss))
        return RSI.tolist()
    
    def MACD(self, adj_close):
        MACD_line = np.array(self.EMA(adj_close, self.MACD_param[0]))-np.array(self.EMA(adj_close, self.MACD_param[1]))
        tmp, tmp2 = MACD_line.tolist(), 0
        while np.isnan(tmp[0]):
            tmp.pop(0)
            tmp2+=1
        signal_line = np.append(np.full(tmp2, np.nan), np.array(self.EMA(tmp, self.MACD_param[2])))
        MACD_histo = MACD_line - signal_line
        return MACD_line.tolist(), signal_line.tolist(), MACD_histo.tolist()
        
    def max_min(self, adj_close, window_length):
        vmax = np.full(window_length-1, np.nan)
        vmin = np.full(window_length-1, np.nan)
        for i in range(window_length-1,len(adj_close)):
            vmax = np.append(vmax, np.amax(adj_close[i-window_length+1:i+1]))
            vmin = np.append(vmin, np.amin(adj_close[i-window_length+1:i+1]))
        return vmax, vmin

    def STOCH(self, adj_close, high, low):
        '''
        %K = (Current Close - Lowest Low)/(Highest High - Lowest Low) * 100
        %D = 3-day SMA of %K

        Lowest Low = lowest low for the look-back period
        Highest High = highest high for the look-back period
        %K is multiplied by 100 to move the decimal point two places
        '''
        hmax, val = self.max_min(high, self.STOCH_param[0])
        val, lmin = self.max_min(low, self.STOCH_param[0])
        stoch_k_list = np.full(self.STOCH_param[0]-1, np.nan)
        for i in range(self.STOCH_param[0]-1, len(adj_close)):
            print(adj_close[i],hmax[i],lmin[i])
            stoch_k_list = np.append(stoch_k_list, (adj_close[i]-lmin[i])/(hmax[i]-lmin[i])*100)
        stoch_d_list = self.MA(stoch_k_list, self.STOCH_param[1])
        return stoch_k_list.tolist(), stoch_d_list

    def TR(self, adj_close, high, low):
        high = np.array(high)
        low = np.array(low)
        h_l = high - low
        cc = np.array(adj_close[:-1])
        h_cp = np.append(np.nan, np.absolute(high[1:] - cc))
        l_cp = np.append(np.nan, np.absolute(low[1:] - cc))
        tr = np.append(h_l[0], np.amax(np.vstack((h_l[1:], h_cp[1:], l_cp[1:])), axis=0))
        return tr

    def ATR(self, adj_close, high, low):
        '''
        Average True Range

        Current ATR = [(Prior ATR x 13) + Current TR] / 14
        '''
        tr = self.TR(adj_close, high, low)
        atr_list = np.append(np.full(self.ATR_param-1,np.nan), np.mean(tr[:self.ATR_param]))
        for i in range(self.ATR_param, len(adj_close)):
            atr_list = np.append(atr_list, (atr_list[i-1]*(self.ATR_param-1)+tr[i])/self.ATR_param)
        return atr_list.tolist()

    def ADX(self, adj_close, high, low):
        tr = self.TR(adj_close, high, low)
        tr14 = np.append(np.full(self.ATR_param,np.nan), np.sum(tr[1:self.ATR_param+1]))
        for i in range(self.ATR_param+1, len(adj_close)):
            tr14 = np.append(tr14, tr14[i-1]/self.ATR_param*(self.ATR_param-1)+tr[i])

        dm1p, dm1n = np.nan, np.nan
        for i in range(1, len(adj_close)):
            if (high[i]-high[i-1])>(low[i-1]-low[i]):
                dm1p = np.append(dm1p, max(high[i]-high[i-1], 0))
                dm1n = np.append(dm1n, 0)
            elif (high[i]-high[i-1])<(low[i-1]-low[i]):
                dm1p = np.append(dm1p, 0)
                dm1n = np.append(dm1n, max(low[i-1]-low[i], 0))
            else:
                dm1p = np.append(dm1p, 0)
                dm1n = np.append(dm1n, 0)
        dm14p = np.append(np.full(self.DMI_param, np.nan), np.sum(dm1p[1:self.DMI_param+1]))
        dm14n = np.append(np.full(self.DMI_param, np.nan), np.sum(dm1n[1:self.DMI_param+1]))
        for i in range(self.DMI_param+1, len(adj_close)):
            dm14p = np.append(dm14p, (self.DMI_param-1)/self.DMI_param*dm14p[i-1]+dm1p[i])
            dm14n = np.append(dm14n, (self.DMI_param-1)/self.DMI_param*dm14n[i-1]+dm1n[i])
        di14p = dm14p/tr14*100
        di14n = dm14n/tr14*100
        di14diff = np.absolute(di14p-di14n)
        di14sum = di14p+di14n
        dx = di14diff/di14sum*100
        adx_list = np.append(np.full(self.DMI_param+self.ADX_param-1,np.nan), np.mean(dx[self.DMI_param:self.DMI_param+self.ADX_param]))
        for i in range(self.DMI_param+self.ADX_param,len(adj_close)):
            adx_list = np.append(adx_list, ((self.ADX_param-1)*adx_list[i-1]+dx[i])/self.ADX_param)
        return adx_list.tolist(), di14p.tolist(), di14n.tolist()

    def MFI(self, adj_close, volume):
        '''
        Typical Price = (High + Low + Close)/3

        Raw Money Flow = Typical Price x Volume
        Money Flow Ratio = (14-period Positive Money Flow)/(14-period Negative Money Flow)

        Money Flow Index = 100 - 100/(1 + Money Flow Ratio)
        '''
        mf1p,mf1n = np.nan,np.nan
        for i in range(1,len(adj_close)):
            if adj_close[i]>adj_close[i-1]:
                mf1p=np.append(mf1p,adj_close[i]*volume[i])
                mf1n=np.append(mf1n,0)
            elif adj_close[i]<adj_close[i-1]:
                mf1p=np.append(mf1p,0)
                mf1n=np.append(mf1n,adj_close[i]*volume[i])
            else:
                mf1p=np.append(mf1p,0)
                mf1n=np.append(mf1n,0)
        mf14p,mf14n = np.full(self.MFI_param,np.nan), np.full(self.MFI_param,np.nan)
        for i in range(self.MFI_param,len(adj_close)):
            mf14p = np.append(mf14p,np.sum(mf1p[i-self.MFI_param+1:i+1]))
            mf14n = np.append(mf14n,np.sum(mf1n[i-self.MFI_param+1:i+1]))
        mfr = mf14p/mf14n
        mfi = 100-(100/(1+mfr))
        return mfi.tolist()

    def PVT(self, adj_close, volume):
        '''
        PVT = [((CurrentClose - PreviousClose) / PreviousClose) x Volume] + PreviousPVT
        '''
        PVT_list = np.array(np.nan,(adj_close[1]-adj_close[0])/adj_close[0]*volume[1])
        for i in range(2, len(adj_close)):
            PVT_list=np.append(PVT_list,(adj_close[i]-adj_close[i-1])/adj_close[i-1]*volume[i]+PVT_list[i-1])
        return PVT_list.tolist()

if __name__ == '__main__':
    print(technical_indicators().MFI([24.63,24.69,24.99,25.36,25.19,25.17,25.01,24.96,25.08,25.25,25.21,25.37,25.61,25.58,25.46,25.33,25.09,25.03,24.91,24.89,25.13,24.64,24.51,24.15,23.98,24.07,24.36,24.35,24.14,24.81],[ 18730 , 12272 , 24691 , 18358 , 22964 , 15919 , 16067 , 16568 , 16019 , 9774 , 22573 , 12987 , 10907 , 5799 , 7395 , 5818 , 7165 , 5673 , 5625 , 5023 , 7457 , 11798 , 12366 , 13295 , 9257 , 9691 , 8870 , 7169 , 11356 , 13379 ]))
    # print(technical_indicators().ADX([29.8720,30.2381,30.0996,28.9028,28.9225,28.4775,28.5566,27.5576,28.4675,28.2796,27.4882,27.2310,26.3507,26.3309,27.0333,26.2221,26.0144,25.4605,27.0333,27.4487,28.3586,28.4278,27.9530,29.0116,29.3776,29.3576,28.9107,30.6149,30.0502,30.1890,31.1202,30.5356,29.7827,30.0402,30.4861,31.4670,32.0515,31.9724,31.1302,31.6551],[30.1983,30.2776,30.4458,29.3478,29.3477,29.2886,28.8334,28.7346,28.6654,28.8532,28.6356,27.6761,27.2112,26.8651,27.4090,26.9441,26.5189,26.5189,27.0927,27.6860,28.4477,28.5267,28.6654,29.0116,29.8720,29.8028,29.7529,30.6546,30.5951,30.7635,31.1698,30.8923,30.0402,30.6645,30.5951,31.9724,32.1011,32.0317,31.6255,31.8534],[29.4072,29.3182,29.9611,28.7443,28.5566,28.4081,28.0818,27.4289,27.6565,27.8345,27.3992,27.0927,26.1826,26.1332,26.6277,26.1332,25.4307,25.3518,25.8760,26.9640,27.1421,28.0123,27.8840,27.9928,28.7643,29.1402,28.7127,28.9290,30.0304,29.3863,30.1365,30.4267,29.3467,29.9906,29.5152,30.9418,31.5364,31.3580,30.9220,31.1994]))
    # print(technical_indicators().ATR([48.16,48.61,48.75,48.63,48.74,49.03,49.07,49.32,49.91,50.13,49.53,49.50,49.75,50.03,50.31,50.52,50.41,49.34,49.37,50.23,49.24,49.93,48.43,48.18,46.57,45.41,47.77,47.72,48.62,47.85],[48.70,48.72,48.90,48.87,48.82,49.05,49.20,49.35,49.92,50.19,50.12,49.66,49.88,50.19,50.36,50.57,50.65,50.43,49.63,50.33,50.29,50.17,49.32,48.50,48.32,46.80,47.80,48.39,48.66,48.79],[47.79,48.14,48.39,48.37,48.24,48.64,48.94,48.86,49.50,49.87,49.20,48.90,49.43,49.73,49.26,50.09,50.30,49.21,48.98,49.61,49.20,49.43,48.08,47.64,41.55,44.28,47.31,47.20,47.90,47.73]))
    # import matplotlib.pyplot as plt
    # plt.plot(technical_indicators().RSI([44.34,44.09,44.15,43.61,44.33,44.83,45.10,45.42,45.84,46.08,45.89,46.03,45.61,46.28,46.28,46.00,46.03,46.41,46.22,45.64,46.21,46.25,45.71,46.45,45.78,45.35,44.03,44.18,44.22,44.57,43.42,42.66,43.13]))
    
    # print(technical_indicators().MACD(
    #     [29.18, 34.9, 33, 26.59, 28.45, 26.39, 22.8, 23.27, 22.19, 24.9, 27.05, 25.27, 25.02, 27.1, 27.52, 26.01, 25.47,
    #      27.51, 27.23, 25.16, 24.98, 23.31, 21.2, 20.08, 19.31, 16.15, 12.22, 13.51, 13.76, 14.12, 13.6, 13.78, 12.45, 11.85, 11.49, 11.83, 13.65, 14.05]))
    # a,b = technical_indicators().STOCH([0,0,0,0,0,0,0,0,0,0,0,0,0,127.2876,127.1781,128.0138,127.1085,127.7253,127.06,127.33,128.71,127.87,128.58,128.60,127.93,128.11,127.60,127.60,128.69,128.27],[127.01,
    #     127.62,126.59,127.35,128.17,128.43,127.37,126.42,126.90,126.85,125.65,125.72,127.16,127.72,127.69,128.22,128.27,128.09,128.27,127.74,128.77,129.29,130.06,129.12,129.29,128.47,128.09,128.65,129.14,128.64,],[125.36,
    #     126.16,124.93,126.09,126.82,126.48,126.03,124.83,126.39,125.72,124.56,124.57,125.07,126.86,126.63,126.80,126.71,126.80,126.13,125.92,126.99,127.81,128.47,128.06,127.61,127.60,127.00,126.90,127.49,127.40,])
    # print(np.array(a),np.array(b))
    # plt.plot(a)
    # plt.plot(b)
    # print(technical_indicators().EMA([29.18,34.9,33,26.59,28.45,26.39,22.8,23.27,22.19,24.9,27.05,25.27,25.02,27.1,27.52,26.01,25.47,27.51,27.23,25.16],12))
    # print(technical_indicators().MA([29.18,34.9,33,26.59,28.45,26.39,22.8,23.27,22.19,24.9],10))
    # print(technical_indicators().BBands([29.18,34.9,33,26.59,28.45,26.39,22.8,23.27,22.19,24.9,27.05,25.27,25.02,27.1,27.52,26.01,25.47,27.51,27.23,25.16]))
    # print(technical_indicators().MA([22.81,23.09,22.91,23.23,22.83,23.05,23.02,23.29,23.41,23.49,24.6,24.63,24.51,23.73,23.31,23.53,23.06,23.25,23.12,22.8],10))
    # plt.show()