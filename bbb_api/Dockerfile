FROM python:slim

# Criação do diretório de trabalho
WORKDIR /code

# Copia o arquivos com as dependências
COPY ./requirements.txt /code/requirements.txt

# Instalação das dependências
RUN pip install --no-cache-dir -r /code/requirements.txt

# Copia os arquivos do projeto
#COPY ./app /code/app

# Exposição da porta 8000
EXPOSE 8000

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
#CMD ["python", "app/main.py"]