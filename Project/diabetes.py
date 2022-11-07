import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.model_selection import cross_validate
from sklearn.ensemble import RandomForestClassifier

def data():
    data = pd.read_csv("./dataset/data.csv")
    # print(data.info())
    # print(data.shape)

    x = data.iloc[:,0:16].values
    y = data.iloc[:,16].values
    
    train_input, test_input, train_target, test_target = train_test_split(x,y,test_size=0.2)
    return train_input, test_input, train_target, test_target
def make_model():
    model = RandomForestClassifier(n_jobs=-1)
    return model
def do_learn():
    train_input, test_input, train_target, test_target = data()
    model = make_model()
    scores = cross_validate(model, train_input, train_target, return_train_score=True, n_jobs=-1)
    print(np.mean(scores['train_score']), np.mean(scores['test_score']))



    


    
do_learn()
