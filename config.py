import os
from dotenv import load_dotenv
import boto3
import logging

# Definir o diretório base do projeto
base_dir = os.path.abspath(os.path.dirname(__file__))

# Carregar as variáveis de ambiente
load_dotenv()

# Configurar o logger para SQLAlchemy (opcional)
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

class Config:
    # Configurações de banco de dados
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')  # Compatível com ambos serviços
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configurações gerais
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')

    # Serviço AWS S3 (configurações específicas do ideal-octo-engine)
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')

    # Configurações adicionais (se necessário)
    S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

# Inicializar o cliente S3 da AWS (mantendo compatibilidade com ideal-octo-engine)
if Config.AWS_ACCESS_KEY_ID and Config.AWS_SECRET_ACCESS_KEY:
    s3 = boto3.client(
        's3',
        aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
        region_name=Config.AWS_REGION
    )
else:
    s3 = None  # Não inicializar se não houver credenciais AWS

