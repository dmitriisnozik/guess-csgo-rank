from flask import Flask, render_template, request, flash, session, redirect
import sqlite3
import random
import re
from DataBase import DataBase


dbase = None
data = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'


def connect_db():
    con = sqlite3.connect('database.db', check_same_thread=False)
    con.row_factory = sqlite3.Row
    return con


@app.before_first_request
def first_of_all():
    db = connect_db()
    global dbase
    dbase = DataBase(db)
    next_video()
    if 'streak' not in session:
        session['streak'] = 0


@app.route('/', methods=['POST', 'GET'])
def index():
    global data
    video, rank = data
    if request.method == 'POST':
        if request.form['submit_button'] == 'Next video':
            session.pop('_flashes', None)
            next_video()
            return redirect('/')
        else:
            guess = 'correct' if request.form['submit_button'] == rank else 'incorrect'
            session['streak'] = 0 if guess == 'incorrect' else session['streak'] + 1
            flash(f'Your guess - {request.form["submit_button"]}, Correct rank - {rank}', category=guess)
            next_video()
            return redirect('/')

    return render_template(
        'index.html',
        title='Guess the rank',
        token=video,
        rank=rank,
    )


def next_video():
    global data
    data = dbase.get_video(random.randint(1, dbase.amount()))


@app.route('/add', methods=['POST', 'GET'])
def add_new():
    if request.method == 'POST':
        if request.form['password'] == '12345':
            url = l[6] if 'watch' in (l := re.findall(r'\w+', request.form['video_url'])) else l[3]
            rank = request.form['rank']
            dbase.add(url, rank)

    return render_template(
        'add.html',
        title='Add new',
    )


if __name__ == '__main__':
    app.run(debug=True)
