from flask import Blueprint, render_template, request, jsonify, current_app as app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import zipfile
from io import BytesIO
from .models import File, Transaction
from . import db
from config import s3
import os
import uuid
import requests
import boto3

limpa_pasta_bp = Blueprint('limpa_pasta_bp', __name__)

BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
ALLOWED_EXTENSIONS = set(os.getenv('ALLOWED_EXTENSIONS', 'zip,rar').split(','))
instance_id = os.getenv('EC2_INSTANCE_ID')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def start_processing_server():
    try:
        ec2_client = boto3.client(
            'ec2',
            region_name=os.getenv('AWS_DEFAULT_REGION'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )
        instance_id = os.getenv('EC2_INSTANCE_ID')
        response = ec2_client.start_instances(InstanceIds=[instance_id])
        app.logger.info(f"Iniciando a instância: {instance_id}")
        return True
    except Exception as e:
        app.logger.error(f"Erro ao iniciar o servidor de processamento: {e}")
        return False


@limpa_pasta_bp.route('/upload_file', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo foi enviado.'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Nenhum arquivo foi selecionado.'}), 400

    if file and allowed_file(file.filename):
        original_filename = secure_filename(file.filename)
        filename = f"{uuid.uuid4().hex}_{original_filename}"
        try:
            with zipfile.ZipFile(BytesIO(file.read()), 'r') as zip_ref:
                num_folders = sum(1 for z in zip_ref.namelist() if z.endswith('/'))
            cost = num_folders * 100
            user = current_user
            if user.credits >= cost:
                user.credits -= cost
                db.session.commit()

                file.seek(0)
                s3_key = f"{current_user.id}/{filename}"
                s3.upload_fileobj(file, BUCKET_NAME, s3_key, ExtraArgs={"ContentType": file.content_type})

                new_file = File(user_id=current_user.id, filename=filename, s3_key=s3_key,
                                status='Em Processamento', cost=cost, statusPago=True)
                db.session.add(new_file)
                db.session.commit()

                start_processing_server()
                return jsonify({'success': True, 'message': 'Processamento autorizado e iniciado.', 'file_id': new_file.id})
            else:
                new_file = File(user_id=current_user.id, filename=filename, s3_key='', status='Aguardando Pagamento', cost=cost, statusPago=False)
                db.session.add(new_file)
                db.session.commit()
                return jsonify({'success': False, 'message': 'Saldo insuficiente. Por favor, gere um PIX para continuar.', 'file_id': new_file.id, 'custo': cost})

        except Exception as e:
            app.logger.error(f'Ocorreu um erro ao fazer o upload: {str(e)}')
            return jsonify({'error': f'Ocorreu um erro ao fazer o upload: {str(e)}'}), 500

    return jsonify({'error': 'Tipo de arquivo não permitido.'}), 400


@limpa_pasta_bp.route('/finance', methods=['GET', 'POST'])
@login_required
def finance():
    if request.method == 'POST':
        amount = request.form.get('amount')
        user = current_user

        if not amount.isdigit():
            return jsonify({'error': 'Valor inválido. Insira um número inteiro.'}), 400

        api_key = os.getenv('OPENPIX_API_KEY')
        headers = {'Authorization': f'{api_key}', 'Content-Type': 'application/json'}
        payload = {
            "name": f"Recarga para {user.username}",
            "correlationID": str(uuid.uuid4()),
            "value": int(amount),
            "comment": "Recarga de créditos"
        }

        try:
            response = requests.post('https://api.openpix.com.br/api/v1/qrcode-static', json=payload, headers=headers)
            response.raise_for_status()

            charge = response.json()
            if 'pixQrCode' in charge:
                qr_code = charge['pixQrCode']['qrCodeImage']
            else:
                app.logger.error("Campo 'pixQrCode' não encontrado na resposta")
                return jsonify({'error': 'Erro ao gerar cobrança.'}), 500

            new_transaction = Transaction(user_id=user.id, amount=int(amount), description="Recarga via PIX", status='Pendente', correlation_id=payload['correlationID'])
            db.session.add(new_transaction)
            db.session.commit()

            return jsonify({'qr_code': qr_code})

        except requests.exceptions.HTTPError as http_err:
            app.logger.error(f"HTTP error occurred: {http_err}")
            return jsonify({'error': 'Erro ao gerar cobrança.'}), 500
        except Exception as err:
            app.logger.error(f"Other error occurred: {err}")
            return jsonify({'error': 'Erro ao gerar cobrança.'}), 500

    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.timestamp.desc()).all()
    return render_template('finance.html', transactions=transactions)
