from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.sql import func

db = SQLAlchemy()

# Tabela 'user' no schema 'site'
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    __table_args__ = {'schema': 'site'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    credits = db.Column(db.Integer, default=0)
    is_admin = db.Column(db.Boolean, default=False)
    profile_pic = db.Column(db.String(255), nullable=True)
    transactions = db.relationship('Transaction', backref='user', lazy=True)
    files = db.relationship('File', backref='user', lazy=True)
    services = db.relationship('Service', backref='user', lazy=True)

# Tabela 'services' no schema 'site' para controlar quais serviços estão habilitados
class Service(db.Model):
    __tablename__ = 'services'
    __table_args__ = {'schema': 'site'}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('site.user.id'), nullable=False)  # FK para User
    limpa_nome = db.Column(db.Boolean, default=False)
    limpa_pasta = db.Column(db.Boolean, default=False)
    servico_3 = db.Column(db.Boolean, default=False)
    servico_4 = db.Column(db.Boolean, default=False)

# Tabelas do serviço 'limpa_pasta' no schema 'limpa_pasta'

# Tabela 'job_limpa_pasta'
class JobLimpaPasta(db.Model):
    __tablename__ = 'job_limpa_pasta'
    __table_args__ = {'schema': 'limpa_pasta'}

    id_job = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('site.user.id'), nullable=False)  # FK para User
    link_arquivo = db.Column(db.String(255), nullable=False)
    novo_link = db.Column(db.String(255), nullable=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    job_feito = db.Column(db.Boolean, default=False)

# Tabela 'file' do serviço 'limpa_pasta'
class File(db.Model):
    __tablename__ = 'file'
    __table_args__ = {'schema': 'limpa_pasta'}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('site.user.id'), nullable=False)  # FK para User
    filename = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Iniciando')
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    s3_key = db.Column(db.String(255), nullable=False)
    download_link = db.Column(db.String(255), nullable=True)
    cost = db.Column(db.Float, nullable=True)
    qr_code = db.Column(db.Text, nullable=True)
    statusPago = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<File {self.filename}>'

# Tabela 'transaction' do serviço 'limpa_pasta'
class Transaction(db.Model):
    __tablename__ = 'transaction'
    __table_args__ = {'schema': 'limpa_pasta'}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('site.user.id'), nullable=False)  # FK para User
    file_id = db.Column(db.Integer, db.ForeignKey('limpa_pasta.file.id'), nullable=True)  # FK para File
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    payment_type = db.Column(db.String(50), nullable=True)
    reference = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(50), nullable=False, default='Pendente')
    correlation_id = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=func.now())

    def formatted_amount(self):
        return f"R$ {self.amount:.2f}"

# Tabelas do serviço 'limpa_nome' no schema 'limpa_nome'

class Vendedor(db.Model):
    __tablename__ = 'vendedores'
    __table_args__ = {'schema': 'limpa_nome'}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('site.user.id'), nullable=False)  # FK para User
    afiliado_id = db.Column(db.Integer, db.ForeignKey('limpa_nome.vendedores.id'), nullable=True)  # FK para Vendedor (self-referencing)
    id_encadeado = db.Column(db.String(255), nullable=False)
    indicacoes = db.Column(db.Integer, default=0)
    vendas_fechadas = db.Column(db.Integer, default=0)
    vendas_concluidas = db.Column(db.Integer, default=0)
    afiliados = db.Column(db.Integer, default=0)
    comissao_acumulada = db.Column(db.Numeric(10, 2), default=0.00)
    data_ultima_venda = db.Column(db.Date)
    status = db.Column(db.String(50), default='Ativo')
    data_criacao = db.Column(db.Date, default=db.func.current_date())
    telefone = db.Column(db.String(20))
    tipo_vendedor = db.Column(db.String(50), default='Afiliado')

class Cliente(db.Model):
    __tablename__ = 'clientes'
    __table_args__ = {'schema': 'limpa_nome'}

    id = db.Column(db.Integer, primary_key=True)
    vendedor_id = db.Column(db.Integer, db.ForeignKey('limpa_nome.vendedores.id'), nullable=False)  # FK para Vendedor
    nome = db.Column(db.String(255), nullable=False)
    valor_divida = db.Column(db.Numeric(10, 2))
    status_pagamento = db.Column(db.String(50), default='Aguardando pagamento')
    status_contrato = db.Column(db.String(50), default='Aberto')
    afiliado_potencial = db.Column(db.Boolean, default=False)
    afiliado_id = db.Column(db.String(255))
    forma_pagamento = db.Column(db.String(50), default='Não Informado')
    data_pagamento = db.Column(db.Date)
    email = db.Column(db.String(255))
    telefone = db.Column(db.String(20))
    data_contrato = db.Column(db.Date)
    origem_lead = db.Column(db.String(100), default='Afiliado')
    documentos_recebidos = db.Column(db.Boolean, default=False)

class Venda(db.Model):
    __tablename__ = 'vendas'
    __table_args__ = {'schema': 'limpa_nome'}

    id = db.Column(db.Integer, primary_key=True)
    vendedor_id = db.Column(db.Integer, db.ForeignKey('limpa_nome.vendedores.id'), nullable=False)  # FK para Vendedor
    cliente_id = db.Column(db.Integer, db.ForeignKey('limpa_nome.clientes.id'), nullable=False)  # FK para Cliente
    valor_venda = db.Column(db.Numeric(10, 2), default=1500.00)
    status = db.Column(db.String(50), default='Aguardando Fechamento')
    data_venda = db.Column(db.Date)
    data_conclusao = db.Column(db.Date)
    forma_pagamento = db.Column(db.String(50), default='Não Informado')
    data_pagamento = db.Column(db.Date)
    numero_parcelas = db.Column(db.Integer, default=1)
    valor_pago = db.Column(db.Numeric(10, 2))
    data_cancelamento = db.Column(db.Date)
    motivo_cancelamento = db.Column(db.String(255))
    status_pagamento = db.Column(db.String(50), default='Pendente')
    tipo_venda = db.Column(db.String(50), default='Não Informado')

class Comissao(db.Model):
    __tablename__ = 'comissao'
    __table_args__ = {'schema': 'limpa_nome'}

    id = db.Column(db.Integer, primary_key=True)
    vendedor_id = db.Column(db.Integer, db.ForeignKey('limpa_nome.vendedores.id'), nullable=False)  # FK para Vendedor
    afiliado_id = db.Column(db.Integer, nullable=False)
    valor_comissao = db.Column(db.Numeric(10, 2), nullable=False)
    nivel = db.Column(db.Integer, nullable=False)
    data_comissao = db.Column(db.Date, default=db.func.current_date())
    status = db.Column(db.String(50), default='Pendente')
