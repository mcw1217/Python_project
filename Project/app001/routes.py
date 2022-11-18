from flask import render_template, request, redirect, url_for, session
import re
from app001 import app
from app001.models import User
import pickle
import numpy as np

app.secret_key = 'your secret key'


@app.route('/login/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    # username과 password에 입력값이 있을 경우
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # 쉬운 checking을 위해 변수에 값 넣기
        username = request.form['username']
        password = request.form['password']
        # MySQL DB에 해당 계정 정보가 있는지 확인
        account,check_password = User.login_check(username,password)
        if check_password:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            fromip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
            User.update_fromip(fromip, account['id'])
            # return 'Logged in successfully!'
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password!'
    if 'loggedin' in session:
      return redirect(url_for('home'))
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)

@app.route('/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
  
  
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))
 
 
@app.route('/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        account = User.get_information([session['id']])
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
  
@app.route('/ip', methods=['GET'])
def client_ip():
    return request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
  
  
  
@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = 'Creating User Page'
    # If already loggedin, redirect to home
    if 'loggedin' in session:
        return redirect(url_for('home'))
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        username_already_exist = User.check_username_exist(username)
        email_already_exist = User.check_email_exist(email)
        if username_already_exist:
            msg = 'That username is already exist'
        elif email_already_exist:
            msg = 'That email is already exist'
        else:
            User.useradd(username, password, email)
            msg = 'Create User Success!'
            return redirect(url_for('login'))
    return render_template('register.html', msg=msg)

@app.route('/survey', methods=['GET', 'POST'])
def survey():
    msg = render_template("survey.html")
    return msg

@app.route('/survey_ans', methods=['GET','POST'])
def survey_ans():
    model = pickle.load(open("./app001/model/model.t","rb"))
    tool = pickle.load(open("./app001/model/tool.t","rb"))

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