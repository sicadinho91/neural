import pandas as pd
import numpy as np
from scipy.stats import spearmanr
import matplotlib.pyplot as plt

class Transform():

    def tradesignal(self, delta, start, end, trend):
        if start == 0:
            tf = [0.5]
            delta_t = float(1/(delta+1))
        else:
            tf = []
            delta_t = float(1/(delta))
        delta = delta + 1
        t = 0.5
        i = 1
        if trend == 'up':
            for i in range(1, delta):
                if float(i/delta) < 0.5:
                    t = t - delta_t
                elif float(i/delta) == 0.5:
                    t = t
                else:                
                    t = t + delta_t
                tf.append(t)
                i = i + 1
        
        elif trend == 'down':
            for i in range(1, delta):
                if float(i/delta) < 0.5:
                    t = t + delta_t
                elif float(i/delta) == 0.5:
                    t = t
                else:
                    t = t - delta_t
                tf.append(t)
                i = i + 1
        
        else:
            for i in range(1, delta):
                t = 0.5
                tf.append(t)
                i = i + 1
        return tf

    def correlation(self, df):
        i = 0
        corr = []
        pvals = []
        cols = list(df.columns.values)
        for i in range(0, len(df.columns)):
            corr.append(spearmanr(df.iloc[:,i:i+1], df.iloc[:,-1:])[0])
            pvals.append(spearmanr(df.iloc[:,i:i+1], df.iloc[:,-1:])[1])
            i = i + 1
        sra = pd.DataFrame({
            'Field': cols,
            'Correlation': corr,
            'P-Values': pvals
            })
        #sra.to_excel('./sra.xlsx')
        return sra
        
    def significant(self, df):
        significant = df[(df['P-Values'] < .01) & (df['P-Values'] > 0)]
        return significant
        
    def normalize(self, df):
        df_norm = (df - df.min()) / (df.max() - df.min())
        return df_norm
        
    def trend(self, indices, closes):
        self.indices = indices
        self.closes = closes
        self.startIndex = 0
        self.endIndex = 1
        self.trade_signal = []
        self.df = pd.DataFrame({'Field': self.indices, 'Adj Close': self.closes})
        self.Hi = np.where((self.df['Adj Close']>self.df['Adj Close'].shift(1)) & (self.df['Adj Close']>self.df['Adj Close'].shift(-1)), self.df['Field'], 0)
        self.Lo = np.where((self.df['Adj Close']<self.df['Adj Close'].shift(1)) & (self.df['Adj Close']<self.df['Adj Close'].shift(-1)), self.df['Field'], 0)
        self.df['endpoints'] = self.Hi + self.Lo
        self.df.iloc[-1, self.df.columns.get_loc('endpoints')] = max(self.df['Field'])
        while self.endIndex != (len(self.df)):
            if self.df['endpoints'].loc[self.endIndex] == 0:
                pass
            else:
                segment = self.df['Field'].loc[self.startIndex:self.endIndex]
                length = len(self.df['Field'].loc[self.startIndex:self.endIndex]) - 1
                if self.df['Adj Close'].loc[self.endIndex] > self.df['Adj Close'].loc[self.startIndex]:
                    trend = 'up'
                elif self.df['Adj Close'].loc[self.endIndex] < self.df['Adj Close'].loc[self.startIndex]:
                    trend = 'down'
                else:
                    trend = 'flat'
                signal = self.tradesignal((self.df['Field'].loc[self.endIndex]) - self.df['Field'].loc[self.startIndex], self.df['Field'].loc[self.startIndex], self.df['Field'].loc[self.endIndex], trend)
                self.trade_signal = self.trade_signal + signal
                self.startIndex = self.endIndex
            self.endIndex = self.endIndex + 1
        #plt.plot(range(0, len(self.trade_signal)), self.trade_signal)
        #plt.show()
        return self.trade_signal