from flask import Flask, render_template, request, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy



#db = SQLAlchemy()

def create_app():

    app = Flask(__name__)
    app.secret_key = 'super secret key'
    #db.init_app(app)


    @app.route('/')
    def home():

        if "email" in session:
            session['connected'] = True
        else :
            session['connected'] = False

        return render_template('index.html', active=["homepage", session['connected']])


    @app.route("/login", methods=['POST', 'GET'])
    def login():
        if "email" in session:
            email = session['email']
            return f"<h1>{email}</h1>"
        else :
            if request.method == "POST":
                email=request.form['email']
                session['email'] = email
                #password=request.form['password']
                #session['password']= password
                connected = True
                return redirect(url_for('home'))
            else:
                return render_template("login.html", active=["login", session['connected']])
    
    @app.route('/user')
    def user():
        if "email" in session:
            email = session['email']
            return f"<h1>{email}</h1>"
        else : 
            return redirect(url_for("login"))
        
    @app.route("/logout")
    def logout():
        session.pop('email', None)
        session.pop('password', None)
        session['connected'] = False
        return redirect(url_for("login"))

    return app