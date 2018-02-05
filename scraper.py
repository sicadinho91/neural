import pandas_datareader.data as web
import pandas as pd
import datetime
import numpy as np

#initial variable definition
time_delta = 1000
df = pd.DataFrame()
now = datetime.datetime.now()
end = datetime.datetime(now.year, now.month, now.day)
start = end - datetime.timedelta(days = time_delta)

class Scraper(object):
    
    def scrape(self, ticker):
        def adjustment(df):
            adjustment = (df['Adj Close']/df['Close'])
            df['Adj Open'], df['Adj High'], df['Adj Low'] = adjustment*df['Open'], adjustment*df['High'], adjustment*df['Low']
            del df['Open'], df['High'], df['Close'], df['Low']
            per = [1, 5]
            for i in per:
                df['%iD Delta'%i] = df['Adj Close'] - df['Adj Close'].shift(i)
            return df

        def avg_vol(df):
            per = [5, 10]
            for i in per:
                df['%i AV'%i] = df['Volume'].rolling(window = i).mean()
            return df

        def ema(df):
            per = [5, 12, 20, 26]
            for i in per:
                df['%i EMA'%i] = df['Adj Close'].ewm(ignore_na=False, span=i, min_periods=i, adjust=True).mean()
            df['12-26 EMA'] = df['12 EMA'] - df['26 EMA']
            return df

        def sma(df):
            per = [5, 6, 10, 20]
            for i in per:
                df['%i SMA'%i] = df['Adj Close'].rolling(window=i).mean()
                df['Delta_%i SMA' %i] = df['%i SMA'%i] - df['%i SMA'%i].shift(-1)
            return df

        def macd(df):
            i = 9
            df['macd line'] = df['12 EMA'] - df['26 EMA']
            df['Delta_macd line'] = df['macd line'] - df['macd line'].shift(-1)
            df['macd signal'] = df['macd line'].ewm(ignore_na=False,span=i,min_periods=i,adjust=True).mean()
            df['macd histogram'] = df['macd line'] - df['macd signal']
            return df

        def stoch(df):
            i, b = 14, 3
            df['stoch k'] = (df['Adj Close']-df['Adj Low'].rolling(window=i).min())/(df['Adj High'].rolling(window=i).max()-df['Adj Low'].rolling(window=i).min())*100
            df['Delta_stoch k'] = df['stoch k'] - df['stoch k'].shift(-1)
            df['stoch d'] = df['stoch k'].rolling(window=b).mean()
            df['Delta_stoch d'] = df['stoch d'] - df['stoch d'].shift(-1)
            df['slow d'] = df['stoch d'].rolling(window=b).mean()
            return df

        def move(df):
            i, b = 3, 9
            df['Momentum'] = df['Adj Close'] - df['Adj Close'].shift(i)
            df['ROC']=((df['Adj Close']-df['Adj Close'].shift(b))/df['Adj Close'].shift(b))*100
            return df

        def strength(df):
            i = 14
            b = [14, 7]
            df['LW %R'] = ((df['Adj High'].rolling(window=i).max()-df['Adj Close'])/(df['Adj High'].rolling(window=i).max()-df['Adj Low'].rolling(window=i).min()))*-100
            df['Delta_LW %R'] = df['LW %R'] - df['LW %R'].shift(-1)
            for n in b:
                delta = df['Adj Close']-df['Adj Close'].shift(1)
                dUp, dDown = delta.copy(), delta.copy()
                dUp[dUp < 0] = 0
                dDown[dDown > 0] = 0
                RolUp = dUp.rolling(window=n).mean()
                RolDown = dDown.rolling(window=n).mean().abs()
                RS = RolUp / RolDown
                df['RSI %i'%n] = 100-(100/(1+RS))
                df['Delta_RSI %i'%n] = df['RSI %i'%n] - df['RSI %i'%n].shift(-1)
            return df

        def bband(df):
            per = [5, 10, 20]
            for i in per:
                std = df['Adj Close'].rolling(window=i).std()
                df['%i upper band'%i] = df['%i SMA'%i] + std
                df['%i lower band'%i] = df['%i SMA'%i] - std
                df['%i middle band'%i] = df['%i SMA'%i]
            return df
        
        def bias(df):
            per = [5, 10]
            for i in per:
                df['%i BIAS'%i] = df['Adj Close'] - df['%i SMA'%i]
                df['Delta_%i BIAS'%i] = df['%i BIAS'%i] - df['%i BIAS'%i].shift(-1)
        
        df = web.DataReader(ticker, 'yahoo', start, end)
        df = df.reset_index(drop=False)
        #df['ticker']=ticker
        #df['pubDate'] = end
        adjustment(df)
        avg_vol(df)
        ema(df)
        sma(df)
        macd(df)
        stoch(df)
        move(df)
        strength(df)
        bband(df)
        bias(df)
        df = df[np.isfinite(df['macd signal'])]
        df = df.fillna(0)
        return df