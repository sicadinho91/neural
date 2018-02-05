from sklearn.neural_network import MLPRegressor

class NeuralNetwork():
    
    def error_check(self, predict, actual):
        total_error = 0
        for x_val, y_val in zip(predict, actual):
            error = (x_val - y_val) ** 2
            total_error = total_error + error
            return total_error
    
    def network(self, input, output):
        # create Trainig Dataset
        model = False
        input = input.as_matrix(columns=None)
        trainx = input[:-50]
        trainy = output[:-50]         
        #create neural net
        #parameter optimization
        for a in [20000]:
            for b in ['relu']:
                for c in ['adam']:
                    for d in ['adaptive']:
                        for e in [150000]:           
                            clf = MLPRegressor(
                                hidden_layer_sizes = a,
                                activation = b,
                                solver = c,
                                learning_rate = d,
                                max_iter = e)
                            clf.fit(trainx,trainy)
                             
                            #test prediction
                            testx = input[-50:]
                            testy = output[-50:]
                             
                            predict = clf.predict(testx)
                            print('prediction: ', predict)
                            print('train score: ', clf.score(trainx, trainy))
                            #print('test score: ', clf.score(testx, testy))
                            model_error = self.error_check(predict, testy)
                            if model == False:
                                choice = [a,b,c,d,e]
                                best = predict
                                total_error = model_error
                            elif model_error < total_error:
                                choice = [a,b,c,d,e]
                                best = predict
                                total_error = model_error                               
        #print("_Input_\t_output_")
        prediction = []
        print('best model: ')
        print('     hidden layer sizes: ', a)
        print('     activation: ', b)
        print('     solver: ', c)
        print('     learning rate: ', d)
        print('     max iterations: ', e)
        for i in range(len(testx)):
            #print("  ",testx.iloc[i],"---->",predict[i])
            prediction.append(best[i])
        return prediction, testy