from flask import Flask, render_template, request, url_for, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
import etc.secrets.secret_file as secret
from flashcards_app.raw_data import fill_db
from datetime import timedelta, datetime
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

        # If the question database is empty fill it with questions and answers
        if models.question.query.count()==0:
            fill_db(db, models)

    @app.route('/')
    def home():

        if "email" in session:
            session['connected'] = True
        else :
            session['connected'] = False

        return render_template('index.html', active=["homepage", session['connected']])
    
    @app.route('/flash_cards', methods=['POST', 'GET'])
    def flash_cards():
        if request.method == "POST":
            # retrieves information from the buttons
            action, id_action = request.form['submit'].split('-')

            # extracts only the number
            id_action = id_action.replace('{', '').replace('}', '').replace(' ', '')

            # Find the user's question in the database
            found_learning = models.learning.query.filter_by(user_id=session['user_id']).filter_by(question_id=id_action).first()

            # Update the next time the user will see the flashcard
            if action == 'hour':
                # User sees the flashcard again in one hour
                found_learning.next_show = datetime.now()+ timedelta(hours=1)
            elif action == "day":
                # User sees the flashcard again in one day
                found_learning.next_show = datetime.now()+ timedelta(days=1)
            elif action == "week":
                # User sees the flashcard again in one week
                found_learning.next_show = datetime.now()+ timedelta(days=7)
            elif action == "delete":
                # User never sees the flashcard again
                found_learning.next_show = datetime.now()+timedelta(days=36500)

            # update the database with the changes
            db.session.commit()

            # inform the user that the changes are effective
            flash("Changes confirm !", 'info')

            # retrieve the question id from database 
            id_question = models.learning.query.filter_by(user_id=session['user_id']).filter(models.learning.next_show<datetime.now()).with_entities(models.learning.question_id).all()
            
            # get id_question in list shape
            id_question_flatten = list(map(lambda x : int(np.squeeze(x)), id_question))

            # retrieve questions from id_question
            list_question = np.squeeze(models.question.query.filter(models.question._id.in_(id_question_flatten)).filter(models.question.lesson<=session['last_lesson']).with_entities(models.question.question).all()).tolist()
            
            # retrieve answers from id_question
            list_answer = np.squeeze(models.question.query.filter(models.question._id.in_(id_question_flatten)).filter(models.question.lesson<=session['last_lesson']).with_entities(models.question.answer).all()).tolist()
           
            return render_template('flash_cards.html', active=["flash_cards", 
                                                            session['connected'], 
                                                            list_question,
                                                            list_answer, 
                                                            id_question_flatten])
        else :
            # retrieve the question id from database 
            id_question = models.learning.query.filter_by(user_id=session['user_id']).filter(models.learning.next_show<datetime.now()).with_entities(models.learning.question_id).all()
            
            # get id_question in list shape
            id_question_flatten = list(map(lambda x : int(np.squeeze(x)), id_question))

            # retrieve questions from id_question
            list_question = np.squeeze(models.question.query.filter(models.question._id.in_(id_question_flatten)).filter(models.question.lesson<=session['last_lesson']).with_entities(models.question.question).all()).tolist()
            
            # retrieve answers from id_question
            list_answer = np.squeeze(models.question.query.filter(models.question._id.in_(id_question_flatten)).filter(models.question.lesson<=session['last_lesson']).with_entities(models.question.answer).all()).tolist()

            return render_template('flash_cards.html', active=["flash_cards", 
                                                            session['connected'], 
                                                            list_question,
                                                            list_answer, 
                                                            id_question_flatten])
    
    @app.route('/admin', methods=['POST', 'GET'])
    def admin():
        if request.method == "POST":

            if request.form['id']==secret.admin_id and request.form['password']==secret.admin_password :

                flash('You have been logged in!', 'info')
                session['admin'] = True

                return redirect(url_for('create_cards'))
            else :
                flash("id or password incorect, please try again !", 'info')

                return redirect(url_for('admin'))

        else:
            return render_template("admin.html", active=["admin", session['connected']])

    @app.route('/create_cards', methods=['POST', 'GET'])
    def create_cards():
        if 'admin' in session and session['admin']:
            if request.method == "POST":
                flashcard = models.question(question=request.form['question'],
                                            answer=request.form['answer'],
                                            lesson=request.form['lesson'])

                db.session.add(flashcard)
                db.session.commit()
                flash('The card has been added  !', 'info')
                return render_template("create_cards.html", active=["create_cards", session['connected']])
            else :
                return render_template("create_cards.html", active=["create_cards", session['connected']])
        else : 
            flash("Please loging first !", 'info')
            return redirect(url_for('admin'))

    @app.route('/create_account', methods=['POST', 'GET'])
    def create_account():

        if request.method == "POST":

            found_user = models.users.query.filter_by(email=request.form['email']).first()

            if  found_user:
            
                flash('You already have an account !', 'info')
                flash('Please use the login page !', 'info')
                return redirect(url_for('create_account'))
            
            else :

                # add new user
                usr = models.users(email=request.form['email'],
                                   last_lesson=request.form['last_lesson'])
                db.session.add(usr)
                db.session.commit()

                # Search for the id of the new user
                found_user = models.users.query.filter_by(email=request.form['email']).first()

                # Search for the id of the question in db
                found_question = models.question.query.with_entities(models.question._id).all()

                # Fill the table learning for the user_id with the id of every question in the db
                for quest in found_question:
                    user_question = models.learning(user_id=int(np.squeeze(found_user._id)),
                                                    question_id=int(np.squeeze(quest)))
                    db.session.add(user_question)
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
                session['user_id'] = found_user._id

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
            found_user.last_lesson = request.form['last_lesson']

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