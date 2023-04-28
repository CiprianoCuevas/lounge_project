from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models.member_model import Member
from flask_app.models.game_model import Game
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def homepage():
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/dashboard")
def dashboard():
    # if not 'member_id' not in session:
    #     return redirect('/login')
    return render_template('mainpage.html', games = Game.playing(), member = Member.show_gamer(session['member_id']))

@app.route("/log_in", methods = ['POST'])
def sign_in():
    data = {'email' :  request.form['email'],
            'password' : request.form['password']
            }
    member_db = Member.show_member(data)
    if not member_db:
        flash('Please Re-Enter Your Email/Password')
        return redirect('/login')
    if not bcrypt.check_password_hash(member_db.password,request.form['password']):
        flash('Please Re-Enter Your Information')
        return redirect('/login')
    session['member_id'] = member_db.id
    return redirect('/dashboard')

@app.route("/member_registration", methods = ['POST'])
def create_member():
    if not Member.validator(request.form):
        return redirect('/login')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'f_name' : request.form['f_name'],
        'l_name' : request.form['l_name'],
        'email' : request.form['email'],
        'password' : pw_hash
    }
    member_id = Member.save(data)
    session['member_id'] = member_id
    return redirect('/dashboard')

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')
