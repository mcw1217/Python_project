# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 15:13:38 2022

@author: 김민서
"""

from flask import Flask, request, render_template
import pickle
import numpy as np

def make_model():
    model = pickle.load(open("model.t","rb"))
    print(model)
    return model
    
def do_predict(model, age, , w2, h2):
    tool = pickle.load(open("tool.t","rb"))
    model = make_model()

    x = [[w1,h1,w2,h2]]
    x = tool.transform(x).toarray()
    age = [[age]]
    x = np.hstack([age,x])
    
    y_pre = model.predict(x)
    return y_pre




model = make_model()

#============================================================

webserver = Flask(__name__)

@webserver.route("/")
def index():
    msg="welcome!"
    return msg

@webserver.route("/survey")
def iris():
    msg = render_template("survey.html")
    return msg

@webserver.route("/survey_ans", methods=["POST"])
def iris_ans():
    w1 = float(request.form["w1"])
    h1 = float(request.form["h1"])
    w2 = float(request.form["w2"])
    h2 = float(request.form["h2"])
    
    print(w1, h1, w2, h2)
    
    y_pre = do_predict(model, w1, h1, w2, h2)
    print(y_pre)
    
    msg = f"{w1} {w2} {h1} {h2} => {y_pre[0]}"
    
    return msg


webserver.run(port = 2022)