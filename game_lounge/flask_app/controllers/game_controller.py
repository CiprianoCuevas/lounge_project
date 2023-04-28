from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.game_model import Game
from flask_app.models.member_model import Member
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/playing_now")
def playing_now():
    return render_template('add.html')

@app.route("/enter_info", methods = ['POST'])
def game_info():
    if not Game.game_validator(request.form):
        return redirect('/playing_now')
    data = {
        'title' : request.form['title'],
        'description' : request.form['description'],
        'member_id' : session['member_id']
    }
    Game.save(data)
    return redirect('/dashboard')

@app.route('/edit/<int:id>')
def edit(id):
    if 'member_id' not in session:
        return redirect('/')
    game = Game.one_game(id)
    return render_template('view.html', game = game)

@app.route("/edit_info/<int:id>", methods = ['POST'])
def edit_info(id):
    if not Game.game_validator(request.form):
        return redirect(f'/edit/{id}')
    data = {
        'title' : request.form['title'],
        'description' : request.form['description'],
        'id' : id
    }
    Game.edit_info(data)
    return redirect('/dashbord')

@app.route("/one_gamer/<int:id>")
def display_gamer(id):
    if 'member_id' not in session:
        return redirect('/')
    game = Game.one_game(id)
    return render_template('view.html', game = game , member = Member.show_gamer(session['member_id']))

@app.route('/delete_game/<int:id>')
def delete_game(id):
    Game.delete_info(id)
    return redirect('/dashboard')