import pandas as pd
import numpy as np

class ExponentialSmoothing():

    def es(self, predicted, actual):
        esl = []
        es = []
        alpha = [0.3]
        for i in alpha:
            for val in range(0,len(predicted)):
                if val == 0:
                    esl.append(predicted[val])
                else:
                    esl.append(predicted[val-1]+(i*(actual[val-1] - predicted[val-1])))
            if len(es) == 0:
                es = pd.DataFrame({('Smoothed %s' %i):esl})
            else:
                es['Smoothed %s' %i] = esl
            es['Upper %s' %i] = es['Smoothed %s' %i]*(1 + i)
            es['Lower %s' %i] = es['Smoothed %s' %i]*(1 - i)
            esl = []
        es['Predicted'] = predicted
        es['Actuals'] = actual
        es['Buy'] = np.where((es['Predicted'] < es['Lower 0.3']) & (es['Predicted'].shift(1) > es['Lower 0.3'].shift(1)), "B", np.where((es['Predicted'] > es['Upper 0.3']) & (es['Predicted'].shift(1) < es['Upper 0.3'].shift(1)),"S", ""))
        return es