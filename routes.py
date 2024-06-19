from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import User, Kos
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object('config.Config')

User.create_table()
Kos.create_table()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.find_by_username(username)
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['password'] = user['password']
            session['is_admin'] = user['is_admin']
            return redirect(url_for('home'))
        flash('Login failed. Check your username and/or password.')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        User.create(username, password)
        flash('Registration successful. Please login.')
        return redirect(url_for('login'))
    return render_template('register.html')

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
