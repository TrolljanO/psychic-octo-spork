from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import User

base_bp = Blueprint('base_bp', __name__)

@base_bp.route('/')
@login_required
def index():
    # Redireciona para a página de seleção de serviço
    return redirect(url_for('base_bp.service_selection'))

@base_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@base_bp.route('/user/services')
@login_required
def get_user_services():
    user_services = current_user.services  # Obtenção dos serviços vinculados ao usuário
    return jsonify({
        'limpa_pasta': user_services.limpa_pasta,
        'limpa_nome': user_services.limpa_nome
    })