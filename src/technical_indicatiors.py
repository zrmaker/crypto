import numpy as np
import pandas as pd

class technical_indicators():
    def __init__(self):
        self.alpha = .35
        self.BBands_N = 20
        self.BBands_K = 2
        self.RSI_N = 14

    def MA(self, adj_close, window_length):
        if window_length > len(adj_close): window_length = len(adj_close)
        ma_list = adj_close[-window_length:]
        tmp = pd.Series(ma_list).rolling(window = window_length).mean().tolist()
        return tmp[-1]

    def MAlist(self, adj_close, window_length):
        if window_length > len(adj_close): window_length = len(adj_close)
        return pd.Series(adj_close).rolling(window = window_length).mean().tolist()

    def EMA(self, adj_close, window_length):
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
        std_list = adj_close[-window_length:]
        return np.std(np.array(std_list))

    def BBands(self, adj_close):
        ma = self.MA(adj_close[-self.BBands_N:], self.BBands_N)
        sigma = self.std_dev(adj_close[-self.BBands_N:], self.BBands_N)
        lb = ma-self.BBands_K*sigma
        ub = ma+self.BBands_K*sigma
        percent_b = (adj_close[-1]-lb)/2/self.BBands_K/sigma
        bandwidth = 2*self.BBands_K*sigma/ma
        return lb, ub, percent_b, bandwidth

    def change(self, adj_close):
        return [x-y for x,y in zip(adj_close[1:],adj_close)]

    def RSI(self, adj_close):
        rs_list = adj_close[:self.RSI_N+1]
        change_list = np.array(self.change(rs_list))
        avg_gain = np.sum(change_list[change_list>0])/self.RSI_N
        avg_loss = np.sum(change_list[change_list<0])/self.RSI_N
        for i in range(self.RSI_N+1,len(adj_close)):
            tmp = self.change([adj_close[i-1],adj_close[i]]).pop()
            if tmp > 0:
                avg_gain = (avg_gain*(self.RSI_N-1) + tmp) / self.RSI_N
                avg_loss = avg_loss*(self.RSI_N-1)/self.RSI_N
            elif tmp < 0:
                avg_gain = avg_gain*(self.RSI_N-1)/self.RSI_N
                avg_loss = (avg_loss*(self.RSI_N-1) + tmp) / self.RSI_N
        RS = avg_gain/-avg_loss
        RSI = 100 - 100 / (1 + RS)
        if RSI > 70:
            indicator = 'Overbought'
        elif RSI < 30:
            indicator = 'Oversold'
        else:
            indicator = ''
        return RSI, indicator

    def RSIlist(self, adj_close):
        rs_list = adj_close[:self.RSI_N+1]
        change_list = np.array(self.change(rs_list))
        avg_gain = np.sum(change_list[change_list>0])/self.RSI_N
        avg_loss = np.sum(change_list[change_list<0])/self.RSI_N
        RSI = 100 - 100 / (1 + avg_gain/-avg_loss)
        for i in range(self.RSI_N+1,len(adj_close)):
            tmp = self.change([adj_close[i-1],adj_close[i]]).pop()
            if tmp > 0:
                avg_gain = (avg_gain*(self.RSI_N-1) + tmp) / self.RSI_N
                avg_loss = avg_loss*(self.RSI_N-1)/self.RSI_N
            elif tmp < 0:
                avg_gain = avg_gain*(self.RSI_N-1)/self.RSI_N
                avg_loss = (avg_loss*(self.RSI_N-1) + tmp) / self.RSI_N
            RSI = np.append(RSI, 100 - 100 / (1 + avg_gain/-avg_loss))
        return RSI

    def STOCH(self):
        self.close=0

if __name__ == '__main__':
    print(technical_indicators().RSI([44.34,44.09,44.15,43.61,44.33,44.83,45.10,45.42,45.84,46.08,45.89,46.03,45.61,46.28,46.28,46.00,46.03,46.41,46.22,45.64,46.21,46.25,45.71,46.45,45.78,45.35,44.03,44.18,44.22,44.57,43.42,42.66,43.13]))
    import matplotlib.pyplot as plt
    plt.plot(technical_indicators().RSIlist([44.34,44.09,44.15,43.61,44.33,44.83,45.10,45.42,45.84,46.08,45.89,46.03,45.61,46.28,46.28,46.00,46.03,46.41,46.22,45.64,46.21,46.25,45.71,46.45,45.78,45.35,44.03,44.18,44.22,44.57,43.42,42.66,43.13]))
    plt.show()
    # print(technical_indicators().EMA([11.98,12.18,12,12.31,12.19,12.35,12.4,12.64,13.05,13.96],10))
    # print(technical_indicators().EMA([11.98,12.18,12,12.31,12.19,12.35,12.4,12.64,13.05,13.96,14.47],10))
    # print(technical_indicators().EMA([11.98,12.18,12,12.31,12.19,12.35,12.4,12.64,13.05,13.96,14.47,13.34],10))
    # print(technical_indicators().EMA([11.98,12.18,12,12.31,12.19,12.35,12.4,12.64,13.05,13.96,14.47,13.34,13.77],10))
    # print(technical_indicators().EMA([29.18,34.9,33,26.59,28.45,26.39,22.8,23.27,22.19,24.9],10))
    # print(technical_indicators().MA([29.18,34.9,33,26.59,28.45,26.39,22.8,23.27,22.19,24.9],10))
    # print(technical_indicators().BBands([29.18,34.9,33,26.59,28.45,26.39,22.8,23.27,22.19,24.9,27.05,25.27,25.02,27.1,27.52,26.01,25.47,27.51,27.23,25.16]))
    # print(technical_indicators().MA([22.81,23.09,22.91,23.23,22.83,23.05,23.02,23.29,23.41,23.49,24.6,24.63,24.51,23.73,23.31,23.53,23.06,23.25,23.12,22.8],10))