from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
import pymysql
import logging
from logging.handlers import RotatingFileHandler
from flask_cors import CORS  # Importação do CORS
from dotenv import load_dotenv
import os
from .models import db

# Carregar variáveis de ambiente
load_dotenv()

# Inicialização das extensões do Flask
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'

def create_app():
    # Criar a aplicação Flask
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    print(db)

    # Configuração do banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    app.config["SQLALCHEMY_RECORD_QUERIES"] = True

    # Configuração de CORS para permitir requisições de http://localhost:3001
    CORS(app, resources={r"/*": {"origins": "http://localhost:3001"}}, methods=["GET", "POST", "OPTIONS"])

    # Inicializar as extensões
    migrate.init_app(app, db)
    login.init_app(app)

    with app.app_context():
        # Registro dos Blueprints para diferentes serviços
        from .routes import base_bp
        from .limpa_nome_routes import limpa_nome_bp
        from .limpa_pasta_routes import limpa_pasta_bp
        from .auth import auth
        from .models import User  # Certifique-se de importar User aqui

        app.register_blueprint(base_bp, url_prefix='/')
        app.register_blueprint(limpa_pasta_bp, url_prefix='/limpa_pasta')
        app.register_blueprint(limpa_nome_bp, url_prefix='/limpa_nome')
        app.register_blueprint(auth, url_prefix='/auth')

        # Função user_loader para carregar o usuário a partir do ID
        @login.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

    # Configurações de logs
    if not app.debug:
        # Log de erros
        error_handler = RotatingFileHandler('error.log', maxBytes=1024 * 1024 * 100, backupCount=10)
        error_handler.setLevel(logging.ERROR)
        error_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
        error_handler.setFormatter(error_formatter)
        app.logger.addHandler(error_handler)

        # Log de informações
        info_handler = RotatingFileHandler('app.log', maxBytes=10240, backupCount=10)
        info_handler.setLevel(logging.INFO)
        info_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
        info_handler.setFormatter(info_formatter)
        app.logger.addHandler(info_handler)

    return app
