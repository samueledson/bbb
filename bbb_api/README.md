# BBB

API REST para o sistema de inscrições do BBB feita em Python.

## Recursos

- CRUD de usuários e inscrições

## Como instalar

1. Certifique-se de ter o Python 3.11 instalado em sua máquina.
2. Clone o repositório:
    ```
    git clone https://github.com/samueledson/bbb_api.git
    ```
3. Navegue para o diretório do projeto:
    ```
    cd bbb_api
    ```
4. Crie um ambiente virtual:
   - Linux:
    ```
    python3 -m venv venv
    ```
   - Windows:
    ```
    python -m venv venv
    ```
5. Ative o ambiente virtual:
   - Linux:
    ```
    source venv/bin/activate
    ```
   - Windows:
    ```
    .\venv\bin\activate
    ```
6. Instale as dependências:
    ```
    pip install -r requirements.txt
    ```
7. Após a instalação, execute o comando para iniciar a aplicação:
    ```
    python app/main.py
    ```
8. Acesse a aplicação
    ```
    http://localhost:8000
    ```
9. Acesse a documentação da API
    ```
    http://localhost:8000/docs
    ```

## Instalação com Docker

1. Certifique-se de ter o Docker instalado em sua máquina.
2. Clone o repositório:
    ```
    git clone
   ```
3. Navegue para o diretório do projeto:
    ```
    cd bbb_api
    ```
4. Execute o comando para iniciar a aplicação:
    ```
    docker build -t bbbimage .
    ```
5. Inicie o container:
    ```
    docker run -d --name bbbcontainer -p 8000:8000 bbbimage
    ```
6. Acesse a aplicação
    ```
    http://localhost:8000
    ```
7. Acesse a documentação da API
    ```
    http://localhost:8000/docs
    ```

