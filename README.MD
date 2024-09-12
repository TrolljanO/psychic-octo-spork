# LIMPAPASTA.COM

LIMPAPASTA.COM é um sistema web para gerenciamento de uploads e processamento de links, com controle de créditos. Usuários podem fazer login, atualizar suas informações de perfil, enviar links para processamento, e visualizar um histórico de suas transações. Administradores têm funcionalidades adicionais, como a capacidade de adicionar créditos aos usuários.

## Funcionalidades

- **Login/Logout**: Autenticação de usuários.
- **Cadastro de Usuário**: Registro de novos usuários.
- **Perfil do Usuário**: Atualização de informações de perfil, incluindo upload de foto de perfil.
- **Gestão de Créditos**: Administradores podem adicionar créditos aos usuários.
- **Histórico de Transações**: Visualização de todas as transações de créditos.
- **Upload de Links**: Envio de links para processamento, consumindo créditos.

## Tecnologias Utilizadas

- **Flask**: Framework web para Python.
- **SQLAlchemy**: ORM para interação com banco de dados.
- **Flask-Login**: Gerenciamento de sessões de usuário.
- **Flask-Migrate**: Migrações de banco de dados.
- **SQLite**: Banco de dados relacional.

## Instalação

1. Clone o repositório do projeto:
    ```bash
    git clone https://github.com/seu-usuario/LIMPAPASTA.COM.git
    cd LIMPAPASTA.COM
    ```

2. Crie e ative um ambiente virtual Python:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4. Configure o banco de dados:
    ```bash
    flask db upgrade
    ```

5. Crie a pasta de uploads:
    ```bash
    mkdir -p instance/uploads
    ```

6. Inicie o servidor Flask:
    ```bash
    flask run
    ```

## Uso do Sistema

### Login

1. Navegue até a página de login.
2. Insira suas credenciais e faça login.

### Cadastro

1. Navegue até a página de cadastro.
2. Insira as informações necessárias e registre-se.

### Atualização de Perfil

1. Faça login no sistema.
2. Navegue até a página de perfil.
3. Atualize suas informações e/ou faça upload de uma foto de perfil.

### Envio de Links

1. Faça login no sistema.
2. Navegue até a página principal.
3. Insira um link e envie para processamento (consumindo créditos).

### Histórico de Transações

1. Navegue até a página de gestão financeira para visualizar seu histórico de transações.

### Funcionalidades de Administrador

1. Faça login como administrador.
2. Navegue até a página de gestão financeira.
3. Use o formulário de adição de créditos para adicionar créditos a outros usuários.

## Administração do Sistema

### Adicionar Créditos

1. Navegue até a página de gestão financeira.
2. Use o formulário de adição de créditos para adicionar créditos aos usuários.

### Gerenciar Usuários

Use as funcionalidades de administrador para gerenciar usuários conforme necessário.

## Manutenção

### Aplicar Migrações

1. Crie uma nova migração, se necessário:
    ```bash
    flask db migrate -m "Descrição da migração"
    ```

2. Aplique as migrações ao banco de dados:
    ```bash
    flask db upgrade
    ```

### Reiniciar o Servidor

1. Use o comando abaixo para reiniciar o servidor Flask:
    ```bash
    flask run
    ```

## Personalização da Interface de Usuário

Se você precisar de ajuda para personalizar a interface do usuário, entre em contato ou consulte a documentação de estilos e templates.

## Licença

Este projeto é de uso particular, mas pode ser hospedado publicamente. Consulte o arquivo de licença para mais detalhes.
