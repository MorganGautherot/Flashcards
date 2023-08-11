from flask import Flask, render_template, request, url_for, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import numpy as np
import json

db = SQLAlchemy()

def create_app():

    app = Flask(__name__)
    app.secret_key = 'secret-key'
    app.permanent_session_lifetime= timedelta(days=1)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
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
    
    @app.route('/flash_cards')
    def flash_cards():

        print(models.question.query.with_entities(models.question.answer).all())
        return render_template('flash_cards.html', active=["flash_cards", 
                                                           session['connected'], 
                                                           np.squeeze(models.question.query.with_entities(models.question.question).all()).tolist(),
                                                           np.squeeze(models.question.query.with_entities(models.question.answer).all()).tolist()])
    
    @app.route('/create_cards', methods=['POST', 'GET'])
    def create_cards():
        if request.method == "POST":
            flashcard = models.question(question=request.form['question'],
                               answer=request.form['answer'])

            db.session.add(flashcard)
            db.session.commit()
            flash('The card has been added  !', 'info')
            return render_template("create_cards.html", active=["create_cards", session['connected']])
        else :
            return render_template("create_cards.html", active=["create_cards", session['connected']])

    @app.route('/create_account', methods=['POST', 'GET'])
    def create_account():

        if request.method == "POST":

            found_user = models.users.query.filter_by(email=request.form['email']).first()

            if  found_user:
            
                flash('You already have an account !', 'info')
                flash('Please use the login page !', 'info')
                return redirect(url_for('create_account'))
            
            else :
                usr = models.users(email=request.form['email'],
                                   last_lesson=request.form['last_lesson'])

                db.session.add(usr)

                db.session.commit()

                flash('Your account has been created, please log on now !', 'info')

                return redirect(url_for('home'))
        else :     

            return render_template("create_account.html", active=["create_account", session['connected']])

    @app.route("/login", methods=['POST', 'GET'])
    def login():
        if request.method == "POST":

            found_user = models.users.query.filter_by(email=request.form['email']).first()

            if found_user:
                session['email'] = request.form['email']
                session['last_lesson'] = found_user.last_lesson

                session.permanent = True

                flash('You have been logged in!', 'info')

                return redirect(url_for('home'))
            else :
                flash("You don't have an account, please create one know !", 'info')

                return redirect(url_for('login'))

        else:
            return render_template("login.html", active=["login", session['connected']])
    
    @app.route('/user', methods=['POST', 'GET'])
    def user():

        if request.method == "POST":

            found_user = models.users.query.filter_by(email=session['email']).first()

            found_user.email = request.form['email']
            found_user.last_email = request.form['last_lesson']

            db.session.commit()
            flash("Changes confirm !", 'info')

            session['email'] = request.form['email']
            session['last_lesson'] = request.form['last_lesson']

            return render_template('user.html', active=["user", session['connected'], session['email'], session['last_lesson']])


        else : 
            found_user = models.users.query.filter_by(email=session['email']).first()
            session['email'] = found_user.email
            session['last_lesson'] = found_user.last_lesson

            return render_template('user.html', active=["user", session['connected'], session['email'], session['last_lesson']])
        
    @app.route("/logout")
    def logout():
        session.pop('email', None)
        session['connected'] = False
        flash('You have been logged out!', 'info')
        return redirect(url_for("home"))

    return app