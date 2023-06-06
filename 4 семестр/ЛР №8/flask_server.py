import json
from flask import Flask, render_template, request
from datetime import datetime
import hashlib
import os

app = Flask(__name__)

users = []

def load_users():
    global users
    if os.path.exists('users.json'):
        with open('users.json', 'r') as file:
            users = json.load(file)

def save_users():
    with open('users.json', 'w') as file:
        json.dump(users, file, indent=4)

@app.route('/user/reg', methods=['GET', 'POST'])
def user_registration():
    if request.method == 'GET':
        return render_template('registration.html')
    elif request.method == 'POST':
        data = request.form

        login = data.get('login')
        password = data.get('password')
        registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not login or not password:
            return "Missing required fields", 400

        for user in users:
            if user['login'] == login:
                return "Login already exists", 400

        # Хеширование пароля с солью
        salt = os.urandom(16)
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        ).hex()

        new_user = {
            'login': login,
            'password_hash': password_hash,
            'salt': salt.hex(),
            'registration_date': registration_date
        }
        users.append(new_user)
        save_users()

        return "User registered successfully", 201

if __name__ == '__main__':
    load_users()
    app.run(debug=True)
