# auth.py
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from . import db
import re

auth = Blueprint('auth', __name__)

# Rota de login (POST e OPTIONS)
@auth.route('/login', methods=['POST', 'OPTIONS'])
def login_post():
    if request.method == 'OPTIONS':
        return '', 200  # Responder ao preflight com sucesso

    email = request.json.get('email')
    password = request.json.get('password')
    remember = True if request.json.get('remember') else False

    # Validação e autenticação
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return {'message': 'Invalid credentials'}, 401

    login_user(user, remember=remember)
    return {'message': 'Login successful'}, 200


@auth.route('/signup', methods=['POST', 'OPTIONS'])
def signup_post():
    if request.method == 'OPTIONS':
        return '', 200  # Resposta ao preflight CORS

    data = request.json
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    confirm_password = data.get('confirmPassword')

    # Validação e inserção no banco de dados
    user = User.query.filter_by(email=email).first()
    if user:
        return {'message': 'Este e-mail já está em uso'}, 400
    if password != confirm_password:
        return {'message': 'As senhas não coincidem'}, 400

    new_user = User(email=email, username=username, password=generate_password_hash(password, method='pbkdf2:sha256'))
    db.session.add(new_user)
    db.session.commit()

    return {'message': 'Cadastro realizado com sucesso!'}, 200

# Rota de logout
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso!', 'info')
    return redirect(url_for('auth.login'))
