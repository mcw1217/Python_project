import pickle
import numpy as np


def pre_data():
    data2 = [["Male","No","No","No","Yes","Yes","No","Yes","Yes","Yes","Yes","No","Yes","Yes","No"]]
    data = [["Male","No","Yes","No","Yes","No","No","No","Yes","No","Yes","No","Yes","Yes","Yes"]]
    tool = pickle.load(open("tool.t","rb"))
    x = tool.transform(data2).toarray()
    age = [[64]]
    x = np.hstack([age,x])
    print(x)
    return x     


def predict(pre_data):
    model = pickle.load(open("model.t","rb"))
    print(model.predict(pre_data))
    

predict(pre_data())

