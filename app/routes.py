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

@base_bp.route('/service_selection')
@login_required
def service_selection():
    user_services = current_user.services  # Tabela Services com os serviços habilitados para o usuário
    return render_template('service_selection.html', services=user_services)
