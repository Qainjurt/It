from flask import Flask, render_template, request, redirect, session, url_for, g
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        db.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id, password FROM users WHERE username=?", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]
            return redirect(url_for('forum'))
        return "Қате логин немесе құпиясөз!"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    db = get_db()
    cursor = db.cursor()
    if request.method == 'POST':
        if 'user_id' in session:
            title = request.form['title']
            content = request.form['content']
            cursor.execute("INSERT INTO posts (title, content, user_id) VALUES (?, ?, ?)",
                           (title, content, session['user_id']))
            db.commit()
    cursor.execute("SELECT title, content FROM posts ORDER BY id DESC")
    posts = cursor.fetchall()
    return render_template('forum.html', posts=posts)

if __name__ == '__main__':
    app.run(debug=True)
