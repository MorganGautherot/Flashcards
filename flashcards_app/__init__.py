from flask import Flask, render_template, request, url_for, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

db = SQLAlchemy()

def create_app():

    app = Flask(__name__)
    app.secret_key = 'secret-key'
    app.permanent_session_lifetime= timedelta(days=1)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite2"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from . import models

    with app.app_context():
        db.create_all()


    @app.route('/')
    def home():

        if "email" in session:
            session['connected'] = True
        else :
            session['connected'] = False

        return render_template('index.html', active=["homepage", session['connected']])


    @app.route("/login", methods=['POST', 'GET'])
    def login():
        if request.method == "POST":

            email=request.form['email']
            session['email'] = email

            password=request.form['password']
            session['password']= password

            session.permanent = True

            flash('You have been logged in!', 'info')

            return redirect(url_for('home'))
        else:
            return render_template("login.html", active=["login", session['connected']])
    
    @app.route('/user', methods=["POST", "GET"])
    def user():
        return render_template('user.html', active=["user", session['connected']])
        
    @app.route("/logout")
    def logout():
        session.pop('email', None)
        session.pop('password', None)
        session['connected'] = False
        flash('You have been logged out!', 'info')
        return redirect(url_for("home"))

    return app