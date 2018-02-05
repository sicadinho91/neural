#imports
import pandas as pd
import numpy as np

class Profit():
    
    def profit(closes):
        df = pd.DataFrame({'Adj Close':closes})
        df['Hi'] = np.where((df['Adj Close']>df['Adj Close'].shift(1)) & (df['Adj Close']>df['Adj Close'].shift(-1)), df['Adj Close'], 0)
        df['Lo'] = np.where((df['Adj Close']<df['Adj Close'].shift(1)) & (df['Adj Close']<df['Adj Close'].shift(-1)), df['Adj Close'], 0)
        if df['Adj Close'].iloc[1] > df['Adj Close'].iloc[0]:
            df['Lo'].iloc[0] = df['Adj Close'].iloc[0]
        if df['Adj Close'].iloc[-1] > df['Adj Close'].iloc[-2]:
            df['Hi'].iloc[-1] = df['Adj Close'].iloc[-1]
        endpoints = df['Hi'] + df['Lo']
        endpoints = pd.DataFrame({'Endpoints':endpoints})
        endpoints = endpoints.loc[(endpoints!=0).any(axis=1)]
        profit_values = []
        profit_pctg = []
        investment = 2000
        for i in range(1, len(endpoints)):
            if ((endpoints.iloc[i]['Endpoints'] - endpoints.iloc[i-1]['Endpoints']) > 0):
                profit_values.append(float(endpoints.iloc[i]['Endpoints'] - endpoints.iloc[i-1]['Endpoints']))
                profit_pctg.append(float(endpoints.iloc[i]['Endpoints'] / endpoints.iloc[i-1]['Endpoints']))
                investment = (investment - 16) * (float(endpoints.iloc[i]['Endpoints'] / endpoints.iloc[i-1]['Endpoints']))
        started = False
        for i in profit_pctg:
            if started == False:
                total_pctg = i
                started = True
            else:
                total_pctg = total_pctg * i
        total_pctg = float(total_pctg - 1.00000)
        #print('values: ', profit_values)
        #print('pctg: ', profit_pctg)
        #print('total_pctg: ', total_pctg)
        #df.to_csv('./output/profit.csv')
        #print('investment: ', investment)
        return investment