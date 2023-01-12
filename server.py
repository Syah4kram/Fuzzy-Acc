from flask import Flask, render_template, request, session, redirect
from flask_restful import Api, Resource
from flask_session import Session
from waitress import serve
import os
import pandas as pd

app = Flask(__name__, static_url_path="", static_folder='static')
api =   Api(app)
app.secret_key = "adminofacc"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
CSV_FOLDER = "static/csv/"

@app.route('/viewdata', methods=['GET', 'POST'])
def viewdata():
    if not session.get("email"):
        return redirect('/login')
    site = request.args.get('site')
    lt = request.args.get('lt')
    return render_template('view.html', site=site, lt=lt)

@app.route('/', methods=['GET', 'POST'])
def index():
    if not session.get("email"):
        return redirect('/login')
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('home.html')

@app.route('/log', methods=['GET', 'POST'])
def log():
    if request.method == "POST":
        email = request.form.get('email')
        if email == "admin@bmkg.go.id":
            session['email'] = email
            return redirect('/')
        else:
            return "<h1>Data salah</h1><br><a href = '/login'>" + "click here to log in</a>"
    else:
        return redirect('/login')

@app.route("/logout")
def logout():
    session["email"] = None
    return redirect("/")

@app.route('/warning-system', methods=['GET', 'POST'])
def wd():
    if not session.get("email"):
        return redirect('/login')
    return render_template('wd.html')

@app.route('/about', methods=['GET', 'POST'])
def about():
    if not session.get("email"):
        return redirect('/login')
    return render_template('about.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if not session.get("email"):
        return redirect('/login')
    return render_template('profile.html')

class view(Resource):
    def get(self):
        dt = []
        x = []
        y = []
        z = []

        name = request.args.get('site')
        st = os.path.join(CSV_FOLDER, name)
        st = st + ".csv"
        df = pd.read_csv(st, delimiter=',')
        
        for i, row in df.iterrows():
            dt.append(row['dt'])
            x.append(row['x'])
            y.append(row['y'])
            z.append(row['z'])

        data={
            "dt": dt, 
            "x": x,
            "y": y,
            "z": z
        }
        return data

class add(Resource):
    def post(self):
        dt = []
        x = []
        y = []
        z = []

        name = request.args.get('site')
        dtadd = request.args.get('dt')
        xadd = request.args.get('x')
        yadd = request.args.get('y')
        zadd = request.args.get('z')

        st = os.path.join(CSV_FOLDER, name)
        st = st + ".csv"
        df = pd.read_csv(st, delimiter=',')
        
        for i, row in df.iterrows():
            dt.append(row['dt'])
            x.append(row['x'])
            y.append(row['y'])
            z.append(row['z'])

        dt.append(dtadd)
        x.append(xadd)
        y.append(yadd)
        z.append(zadd)

        data={
            "dt": dt, 
            "x": x,
            "y": y,
            "z": z
        }

        toexport = pd.DataFrame(data)
        toexport.to_csv(st)
        return data

api.add_resource(view,'/view')
api.add_resource(add,'/add')

if __name__ == '__main__':
    app.run(debug=True)
    #serve(app, host="0.0.0.0", port=5000)