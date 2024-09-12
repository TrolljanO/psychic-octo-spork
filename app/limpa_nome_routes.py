from flask import Blueprint, jsonify, request, abort
from .models import db, Vendedor, Cliente, Venda, Comissao

limpa_nome_bp = Blueprint('limpa_nome_bp', __name__)

# Exemplo de uma função auxiliar para gerar respostas padronizadas
def json_response(data=None, message="Success", status=200):
    response = {
        "message": message,
        "data": data
    }
    return jsonify(response), status

# --------------------- ROTAS DOS VENDEDORES -----------------------

@limpa_nome_bp.route('/vendedores', methods=['GET'])
def get_vendedores():
    vendedores = Vendedor.query.all()
    resultado = [
        {
            "id": v.id,
            "nome": v.user.username,  # Assumindo que o modelo User tem a coluna `username`
            "indicacoes": v.indicacoes,
            "vendas_fechadas": v.vendas_fechadas,
            "vendas_concluidas": v.vendas_concluidas,
            "afiliados": v.afiliados,
            "comissao_acumulada": str(v.comissao_acumulada)
        } for v in vendedores
    ]
    return json_response(data=resultado)

@limpa_nome_bp.route('/vendedores/<int:id>', methods=['GET'])
def get_vendedor(id):
    vendedor = Vendedor.query.get(id)
    if not vendedor:
        return json_response(message="Vendedor não encontrado", status=404)

    vendedor_data = {
        "id": vendedor.id,
        "nome": vendedor.user.nome,  # Supondo relacionamento com tabela de usuários
        "indicacoes": vendedor.indicacoes,
        "vendas_fechadas": vendedor.vendas_fechadas,
        "vendas_concluidas": vendedor.vendas_concluidas,
        "afiliados": vendedor.afiliados,
        "comissao_acumulada": str(vendedor.comissao_acumulada)
    }
    return json_response(data=vendedor_data)

@limpa_nome_bp.route('/vendedores', methods=['POST'])
def create_vendedor():
    data = request.json
    if not data.get('user_id'):
        return json_response(message="ID de usuário é obrigatório", status=400)

    # Se o afiliado for indicado por um vendedor existente (afiliado_id)
    afiliado_superior = Vendedor.query.get(data.get('afiliado_id'))

    if afiliado_superior:
        # Buscar todos os afiliados já indicados pelo afiliado superior
        count_afiliados = Vendedor.query.filter_by(afiliado_id=afiliado_superior.id).count()

        # Criar o id_encadeado baseado no id_encadeado do afiliado superior
        novo_id_encadeado = f"{afiliado_superior.id_encadeado}-{count_afiliados + 1}"
    else:
        # Caso seja o primeiro vendedor, o id_encadeado será "1", ou seja, o primeiro na hierarquia
        novo_id_encadeado = f"1-{Vendedor.query.filter_by(afiliado_id=None).count() + 1}"

    # Criar o novo vendedor/afiliado
    novo_vendedor = Vendedor(
        user_id=data['user_id'],
        afiliado_id=data.get('afiliado_id'),  # Se for afiliado de alguém
        id_encadeado=novo_id_encadeado,
        indicacoes=0,
        vendas_fechadas=0,
        vendas_concluidas=0,
        afiliados=0,
        comissao_acumulada=0.00
    )
    db.session.add(novo_vendedor)
    db.session.commit()

    return json_response(data={"id": novo_vendedor.id, "id_encadeado": novo_vendedor.id_encadeado}, message="Vendedor criado com sucesso", status=201)

# --------------------- ROTAS DOS CLIENTES -----------------------

@limpa_nome_bp.route('/clientes', methods=['GET'])
def get_clientes():
    clientes = Cliente.query.all()
    resultado = [
        {
            "id": c.id,
            "nome": c.nome,
            "vendedor_id": c.vendedor_id,
            "valor_divida": str(c.valor_divida),
            "status_pagamento": c.status_pagamento,
            "status_contrato": c.status_contrato
        } for c in clientes
    ]
    return json_response(data=resultado)

@limpa_nome_bp.route('/clientes/<int:id>', methods=['GET'])
def get_cliente(id):
    cliente = Cliente.query.get(id)
    if not cliente:
        return json_response(message="Cliente não encontrado", status=404)

    cliente_data = {
        "id": cliente.id,
        "nome": cliente.nome,
        "vendedor_id": cliente.vendedor_id,
        "valor_divida": str(cliente.valor_divida),
        "status_pagamento": cliente.status_pagamento,
        "status_contrato": cliente.status_contrato
    }
    return json_response(data=cliente_data)

@limpa_nome_bp.route('/clientes', methods=['POST'])
def create_cliente():
    data = request.json
    if not data.get('nome') or not data.get('vendedor_id'):
        return json_response(message="Nome e ID do vendedor são obrigatórios", status=400)

    novo_cliente = Cliente(
        nome=data['nome'],
        vendedor_id=data['vendedor_id'],
        valor_divida=data.get('valor_divida', 0.00),
        status_pagamento="Aguardando pagamento",
        status_contrato="Aberto"
    )
    db.session.add(novo_cliente)
    db.session.commit()
    return json_response(data={"id": novo_cliente.id}, message="Cliente criado com sucesso", status=201)

# --------------------- ROTAS DAS VENDAS -----------------------

@limpa_nome_bp.route('/vendas', methods=['GET'])
def get_vendas():
    vendas = Venda.query.all()
    resultado = [
        {
            "id": v.id,
            "vendedor_id": v.vendedor_id,
            "cliente_id": v.cliente_id,
            "valor_venda": str(v.valor_venda),
            "status": v.status,
            "data_venda": v.data_venda.strftime("%Y-%m-%d") if v.data_venda else None,
            "data_conclusao": v.data_conclusao.strftime("%Y-%m-%d") if v.data_conclusao else None
        } for v in vendas
    ]
    return json_response(data=resultado)

@limpa_nome_bp.route('/vendas/<int:id>', methods=['GET'])
def get_venda(id):
    venda = Venda.query.get(id)
    if not venda:
        return json_response(message="Venda não encontrada", status=404)

    venda_data = {
        "id": venda.id,
        "vendedor_id": venda.vendedor_id,
        "cliente_id": venda.cliente_id,
        "valor_venda": str(venda.valor_venda),
        "status": venda.status,
        "data_venda": venda.data_venda.strftime("%Y-%m-%d") if venda.data_venda else None,
        "data_conclusao": venda.data_conclusao.strftime("%Y-%m-%d") if venda.data_conclusao else None
    }
    return json_response(data=venda_data)

@limpa_nome_bp.route('/vendas', methods=['POST'])
def create_venda():
    data = request.json
    if not data.get('vendedor_id') or not data.get('cliente_id'):
        return json_response(message="ID do vendedor e cliente são obrigatórios", status=400)

    nova_venda = Venda(
        vendedor_id=data['vendedor_id'],
        cliente_id=data['cliente_id'],
        valor_venda=data.get('valor_venda', 1500.00),
        status="Aguardando Fechamento"
    )
    db.session.add(nova_venda)
    db.session.commit()

    # Após a criação da venda, distribuir comissões
    distribuir_comissao(nova_venda.id)

    return json_response(data={"id": nova_venda.id}, message="Venda criada com sucesso", status=201)

# --------------------- ROTAS DE COMISSÕES -----------------------

@limpa_nome_bp.route('/comissoes', methods=['POST'])
def create_comissao():
    data = request.json
    if not data.get('vendedor_id') or not data.get('afiliado_id') or not data.get('valor_comissao'):
        return json_response(message="Dados insuficientes para registrar a comissão", status=400)

    nova_comissao = Comissao(
        vendedor_id=data['vendedor_id'],
        afiliado_id=data['afiliado_id'],
        valor_comissao=data['valor_comissao'],
        nivel=data['nivel'],
        status="Pendente"
    )
    db.session.add(nova_comissao)
    db.session.commit()
    return json_response(data={"id": nova_comissao.id}, message="Comissão criada com sucesso", status=201)

@limpa_nome_bp.route('/comissoes/<int:vendedor_id>', methods=['GET'])
def get_comissoes(vendedor_id):
    comissoes = Comissao.query.filter_by(vendedor_id=vendedor_id).all()
    resultado = [
        {
            "id": c.id,
            "vendedor_id": c.vendedor_id,
            "afiliado_id": c.afiliado_id,
            "valor_comissao": str(c.valor_comissao),
            "nivel": c.nivel,
            "data_comissao": c.data_comissao.strftime("%Y-%m-%d"),
            "status": c.status
        } for c in comissoes
    ]
    return json_response(data=resultado)

# Função auxiliar para distribuir comissões
def obter_vendedor_superior(vendedor, nivel_atual):
    afiliado_superior = Vendedor.query.filter_by(id=vendedor.afiliado_id).first()
    return afiliado_superior if afiliado_superior and afiliado_superior.nivel == nivel_atual else None

def distribuir_comissao(venda_id):
    venda = Venda.query.get(venda_id)
    vendedor = Vendedor.query.get(venda.vendedor_id)

    comissao = 500
    nova_comissao = Comissao(
        vendedor_id=venda.vendedor_id,
        afiliado_id=venda.cliente_id,
        valor_comissao=comissao,
        nivel=1,
        status="Pendente"
    )
    db.session.add(nova_comissao)

    # Distribuir comissões para os níveis superiores
    for nivel in range(2, 6):
        vendedor_superior = obter_vendedor_superior(vendedor, nivel)
        if vendedor_superior:
            comissao_nivel = 500 - (nivel - 1) * 50  # A comissão diminui 50 por nível
            nova_comissao = Comissao(
                vendedor_id=vendedor_superior.id,
                afiliado_id=venda.cliente_id,
                valor_comissao=comissao_nivel,
                nivel=nivel,
                status="Pendente"
            )
            db.session.add(nova_comissao)

    db.session.commit()
