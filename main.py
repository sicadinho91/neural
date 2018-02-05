# main.py
from segment import Segment
from scraper import Scraper
from transform import Transform
from profit import Profit
from neuralnetwork import NeuralNetwork
from es import ExponentialSmoothing
import pandas as pd
import datetime

def main():
    out = []
    tickers = pd.read_excel('./tickers.xlsx')
    #tickers = pd.DataFrame({'Ticker': ['GUSH', 'AAPL']})
    print (tickers)
    for tick in tickers['Ticker']:
        print (tick)
        try:
            st = Scraper()
            df = st.scrape(tick)
            #df.to_csv('./output/df.csv')
            ind = df['Date'].iloc[-50:]
            ind = ind.reset_index()
            #ind.to_csv('./output/ind.csv')
            del df['Date']
            points = []
            for record in df['Adj Close']:
                points.append(float(record))
                print (record)
            best_case = 0
            #for w in [0.8, 0.9, 1, 1.1, 1.2, 1.5, 2, 3, 4, 5]:
            for w in [5]:
                segment = Segment(points, 0, len(points), multiplier=w)
                segment.get_turning_points()
                index = sorted(segment.turning_points)
                print(index)
                closes = []
                for i in index:
                    closes.append(points[i])
                profit = Profit.profit(closes)
                #verify logic below
                if profit > best_case:
                    print("weight: ", w)
                    best_case = profit
                    print("profit: ", profit)
                    best_index = index
                    best_closes = closes
            t = Transform()
            transform = t.trend(best_index, best_closes)
            #pd.DataFrame(transform).to_excel('./output/transformed.xlsx')
            df['transformed'] = transform
            sra = t.correlation(df)
            significant_sra = t.significant(sra)
            df_norm = t.normalize(df[significant_sra['Field']])
            #df_norm.to_csv('./output/normalizedinputs.csv')
            n = NeuralNetwork()
            neural, actual = n.network(df_norm, transform)
            pd.DataFrame({'Neural': neural}).to_csv('./output/neural.csv')
            esf = ExponentialSmoothing()
            smoothed = esf.es(neural, actual)
            smoothed['Closes'] = points[-50:]
            smoothed['Date'] = ind['Date']
            smoothed['Ticker'] = tick
            if len(out) == 0:
                out = smoothed
            else:
                out = out.append(smoothed)
        except:
            pass
    today = datetime.date.today()
    pd.DataFrame(out).to_excel('./output/smoothed %s.xlsx'%format(today))
    
if __name__ == "__main__":
    main()