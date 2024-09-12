from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from . import db
import re

auth = Blueprint('auth', __name__)

# Rota de login (GET)
@auth.route('/login', methods=['GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))  # Redireciona se o usuário já está logado
    return render_template('login.html')

# Rota de login (POST)
@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    # Validação simples de email
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        flash('Endereço de e-mail inválido.', 'danger')
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(email=email).first()

    if not user:
        flash('E-mail não encontrado. Por favor, cadastre-se primeiro.', 'danger')
        return redirect(url_for('auth.signup'))

    if not check_password_hash(user.password, password):
        flash('Senha incorreta. Por favor, tente novamente.', 'danger')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    flash('Login realizado com sucesso!', 'success')
    return redirect(url_for('main.index'))

# Rota de signup (GET)
@auth.route('/signup', methods=['GET'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    return render_template('signup.html')

# Rota de signup (POST)
@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')  # Novo campo de confirmação de senha

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Este e-mail já está em uso', 'danger')
        return redirect(url_for('auth.signup'))

    if password != confirm_password:
        flash('As senhas não coincidem', 'danger')
        return redirect(url_for('auth.signup'))

    if len(password) < 8:
        flash('A senha deve ter pelo menos 8 caracteres', 'danger')
        return redirect(url_for('auth.signup'))

    if not re.search(r'[A-Za-z]', password) or not re.search(r'[0-9]', password):
        flash('A senha deve conter letras e números', 'danger')
        return redirect(url_for('auth.signup'))

    # Criar novo usuário
    new_user = User(email=email, username=name, password=generate_password_hash(password, method='pbkdf2:sha256'))
    db.session.add(new_user)
    db.session.commit()

    flash('Cadastro realizado com sucesso! Faça o login.', 'success')
    return redirect(url_for('auth.login'))

# Rota de logout
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso!', 'info')
    return redirect(url_for('auth.login'))
