# Usar uma imagem base do Python 3.9 slim

FROM python:3.9-slim


# Definir o diretório de trabalho no container

WORKDIR /app


# Copiar o arquivo de dependências para o container

COPY requirements.txt .


# Instalar as dependências

RUN pip install --no-cache-dir -r requirements.txt


# Copiar o restante do código para o container

COPY . .


# Definir a variável de ambiente para desabilitar o buffering de saída

ENV PYTHONUNBUFFERED=1


# Expor a porta que o Flask vai rodar

EXPOSE 3775


# Comando para rodar o aplicativo

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:3775", "run:app"]
