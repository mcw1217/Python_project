from flask import Flask, request, render_template
import pickle
import numpy as np

def make_model():
    model = pickle.load(open("model.t","rb"))
    print(model)
    return model

webserver = Flask(__name__)

@webserver.route("/")
def index():
    msg= render_template("main.html")
    return msg

@webserver.route("/survey.html")
def survey():
    msg = render_template("survey.html")
    return msg

@webserver.route("/survey_ans", methods=["POST"])
def survey_ans():
    model = make_model()   
    tool = pickle.load(open("tool.t","rb"))

    gender= request.form["gender"]
    age= request.form["age"]
    a = request.form["a"]
    b = request.form["b"]
    c = request.form["c"]
    d = request.form["d"]
    e = request.form["e"]
    f = request.form["f"]
    g = request.form["g"]
    h = request.form["h"]
    i = request.form["i"]
    j = request.form["j"]
    k = request.form["k"]
    l = request.form["l"]
    m = request.form["m"]
    n = request.form["n"]

    print(gender,a,b,c,d,e,f,g,h,i,j,k,l,m,n)
    x = [[gender,a,b,c,d,e,f,g,h,i,j,k,l,m,n]]
    x = tool.transform(x).toarray()
    age = [[age]]
    x = np.hstack([age,x])

    y_pre = model.predict(x)

    if y_pre[0] == "Positive":
        msg = "[당뇨병 초기 검진 결과] =====> 당신은 '당뇨병' 초기 증상이 의심됩니다! 빠른 시일내에 병원에서 검사해보시기바랍니다."
    else:
        msg = "[당뇨병 초기 검진 결과] =====> 당신은 '당뇨병' 초기 증상이 의심되지 않습니다! 오늘도 건강한 하루되시길 바랍니다!"
    
    return msg

    


webserver.run(port = 2022)