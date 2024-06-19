from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import User, Kos
from werkzeug.security import generate_password_hash, check_password_hash
import os
import scrypt

app = Flask(__name__)
app.config.from_object('config.Config')
app.secret_key = os.urandom(24)  # Ensure you have a secret key for session management

# Inisialisasi tabel
User.create_table()
Kos.create_table()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            User.create(username, password)
            flash('Registration successful. Please log in.')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Registration failed: {str(e)}', 'error')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.login(username, password)
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['password'] = user['password']
            session['is_admin'] = user['is_admin']
            flash('Login successful.')
            return redirect(url_for('home'))
        else:
            flash('Login failed. Check your username and/or password.', 'error')
    
    return render_template('login.html')

@app.route('/search', methods=['GET'])
def search():
    kos_list = Kos.read_all()
    return render_template('search.html', kos_list=kos_list)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('is_admin'):
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        if 'create' in request.form:
            name = request.form['name']
            address = request.form['address']
            price = request.form['price']
            description = request.form['description']
            Kos.create(name, address, price, description)
        elif 'update' in request.form:
            kos_id = request.form['id']
            name = request.form['name']
            address = request.form['address']
            price = request.form['price']
            description = request.form['description']
            Kos.update(kos_id, name, address, price, description)
        elif 'delete' in request.form:
            kos_id = request.form['id']
            Kos.delete(kos_id)
    
    kos_list = Kos.read_all()
    return render_template('admin.html', kos_list=kos_list)

if __name__ == '__main__':
    app.run(debug=True)
