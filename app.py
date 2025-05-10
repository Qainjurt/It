from flask import Flask, request, redirect, session, g, render_template_string
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'secret_key'
DATABASE = 'database.db'

def get_db():
    if not hasattr(g, '_database'):
        g._database = sqlite3.connect(DATABASE)
    return g._database

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db:
        db.close()

def load_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def render_page(title, body_html):
    base = load_file('layout.html')
    return render_template_string(base, title=title, body=body_html)

@app.route('/')
def home():
    content = load_file('home.html')
    return render_page("Басты бет", content)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        db.commit()
        return redirect('/login')
    return render_page("Тіркелу", load_file('register.html'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id, password FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]
            return redirect('/forum')
        else:
            error = "<p style='color:red;'>Қате логин немесе құпиясөз!</p>"
    content = load_file('login.html').replace("{error}", error)
    return render_page("Кіру", content)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    db = get_db()
    cursor = db.cursor()
    if request.method == 'POST' and 'user_id' in session:
        title = request.form['title']
        content = request.form['content']
        cursor.execute("INSERT INTO posts (title, content, user_id) VALUES (?, ?, ?)", (title, content, session['user_id']))
        db.commit()
    cursor.execute("SELECT title, content FROM posts ORDER BY id DESC")
    posts = cursor.fetchall()
    post_html = "".join([f"<div class='post'><h3>{p[0]}</h3><p>{p[1]}</p></div>" for p in posts])
    form = load_file('forum_form.html') if session.get('user_id') else "<p>Форумға жазу үшін тіркеліңіз немесе кіріңіз.</p>"
    full = load_file('forum.html').replace("{form}", form).replace("{posts}", post_html)
    return render_page("Форум", full)

if __name__ == '__main__':
    app.run(debug=True)
