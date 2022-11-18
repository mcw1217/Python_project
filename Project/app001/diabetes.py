import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.model_selection import cross_validate
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import pickle

def pro(data):
    tool = OneHotEncoder()
    key = ['Gender','Polyuria','Polydipsia','sudden weight loss', 'weakness', 'Polyphagia' ,'Genital thrush','visual blurring','Itching','Irritability','delayed healing','partial paresis','muscle stiffness','Alopecia','Obesity']

    x1 = tool.fit_transform(data[key]).toarray()    #onehot인코더를 사용하면 값을 배열로 바꿔주는 과정이 필요함!
    print(x1.shape)
    print(x1[:10])
    pickle.dump(tool, open("tool.t","wb"))
    return x1
    

def data():
    data = pd.read_csv("./dataset/data.csv")
    print(data.info())
    print(data.shape)

    x1 = pro(data)
    x = data.iloc[:,[0]].values
    x = np.hstack([x,x1])
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

    model.fit(train_input, train_target)
    score = model.score(test_input, test_target)
    pickle.dump(model, open("model.t","wb"))
    
    
do_learn()
