# BBB API
A BBB API é uma aplicação REST para o sistema de inscrições do Big Brother Brasil, desenvolvida em Python.

## Recursos
- CRUD de candidatos e inscrições

## Como instalar e executar
### Pré-requisitos
- Docker
- Python 3.11 (caso escolha instalação local)

## Instalação com Docker
1. Clone o repositório:
    ```
    git clone https://github.com/samueledson/bbb_api.git
    ```
2. Navegue para o diretório do projeto:
    ```
    cd api
    ```
3. Execute o comando para construir a imagem e criar o container no Docker:
    ```
    docker compose up
    ```
4. Acesse a aplicação front-end em seu navegador
    ```
    http://localhost:4200
    ```
5. Acesse a documentação da API em seu navegador:
    ```
    http://localhost:8000/docs
    ```

### Instalação local
1. Clone o repositório:
    ```
    git clone https://github.com/samueledson/bbb_api.git
    ```
2. Navegue para o diretório do projeto:
    ```
    cd api
    ```
3. Crie e ative um ambiente virtual:
   - Linux:
    ```
    python3 -m venv venv
    source venv/bin/activate
    ```
   - Windows:
    ```
    python -m venv venv
    .\venv\Scripts\activate
    ```
4. Instale as dependências:
    ```
    pip install -r requirements.txt
    ```
5. Inicie a aplicação:
    ```
    python -m uvicorn app.main:app
    ```
6. Acesse a aplicação front-end em seu navegador
    ```
    http://localhost:4200
    ```
7. Acesse a documentação da API em seu navegador
    ```
    http://localhost:8000/docs
    ```

## Como executar os testes

1. Execute o comando para executar os testes unitários e de integração:
    ```
    pytest
    ```
   
## Observações

- A aplicação está configurada para utilizar um banco de dados MySQL, que é criado automaticamente com o Docker Compose.
Caso queira utilizar outro banco de dados, basta alterar a variável de ambiente `DATABASE_URL` no arquivo `.env` para o endereço do banco de dados desejado e executar as querys do arquivo `setup.sql`
- Para encerrar a aplicação em ambas as formas de instalação, utilize o atalho CTRL+C no terminal ou pare o container do Docker.
- Para encerrar o ambiente virtual, utilize o comando `deactivate`.
- Para remover o ambiente virtual, exclua a pasta `venv`.
