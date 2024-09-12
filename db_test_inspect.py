from sqlalchemy import create_engine, inspect
import os

# URL do banco de dados diretamente do .env
DATABASE_URI = os.getenv('DATABASE_URI', 'mysql+pymysql://trajano_site:nascimento%40123@3.132.30.92:3306/site')

# Conectar ao banco de dados
engine = create_engine(DATABASE_URI)
connection = engine.connect()

# Verificar as tabelas existentes no banco de dados
inspector = inspect(engine)
schemas = inspector.get_schema_names()

for schema in schemas:
    print(f"Schema: {schema}")
    tables = inspector.get_table_names(schema=schema)
    for table in tables:
        print(f"  Table: {table}")

connection.close()
