from db import init_db, fetch_question
from dotenv import load_dotenv
from os import getenv
from flask import Flask, session, url_for, redirect, jsonify, request, render_template
from authlib.integrations.flask_client import OAuth


load_dotenv()

app = Flask(__name__)
app.secret_key = getenv("AUTH_SECRET")

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id= getenv("GOOGLE_ID"),
    client_secret= getenv("GOOGLE_SECRET"),
    access_token_params=None,
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
        userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'email profile'},
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration'
)
init_db()

@app.route('/')
def index():
    if 'profile' in session:
        print(session['profile'])
        return render_template("home.html", profile=session['profile'])
    return redirect("/login")

@app.route('/login')
def login():
    google = oauth.create_client("google")
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    token = google.authorize_access_token()
    userinfo = google.get('userinfo', token=token)
    userinfo.raise_for_status()
    profile = userinfo.json()
    session['profile'] = profile
    session.permanent = True
    return redirect('/')

@app.route("/logout")
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')

@app.route('/next')
def next():
    diff = request.args.get("diff")
    diff = diff if diff != None else "easy"
    no = request.args.get("no")
    no = 1 if no == None else int(no) + 1
    q = fetch_question(diff)
    return render_template('next.html', profile=session["profile"], no=no, diff=diff, question=q)

@app.route('/result')
def result():
    cnt = int(request.args.get("cnt"))
    cr = int(request.args.get("cr"))
    return render_template('result.html', profile=session['profile'], cnt=cnt, cr=cr)
