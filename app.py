from flask import Flask, render_template, request, redirect, url_for, session, g
import sqlite3
import os

from database import init_db, get_db

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # замените на свой секретный ключ

DATABASE = 'database.db'

@app.before_request
def before_request():
    g.db = get_db()

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
        password = request.form['password']
        # Регистрация пользователя
        try:
            g.db.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            g.db.commit()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            error = 'Username already exists'
            return render_template('register.html', error=error)
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = g.db.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password)).fetchone()
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('catalog'))
        else:
            error = 'Invalid credentials'
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/catalog')
def catalog():
    items = g.db.execute('SELECT * FROM objects').fetchall()
    return render_template('catalog.html', items=items)

@app.route('/object/<int:object_id>')
def object_detail(object_id):
    item = g.db.execute('SELECT * FROM objects WHERE id=?', (object_id,)).fetchone()
    if item:
        return render_template('object_detail.html', item=item)
    else:
        return "Object not found", 404

@app.route('/admin')
def admin():
    # Проверка прав администратора (по желанию)
    if 'user_id' not in session or session.get('username') != 'admin':
        return redirect(url_for('login'))
    objects = g.db.execute('SELECT * FROM objects').fetchall()
    return render_template('admin.html', objects=objects)

# Добавьте маршруты для добавления/редактирования/удаления объектов по необходимости

if __name__ == '__main__':
    init_db()
    app.run(debug=True)