# -*- coding: utf-8 -*-
import requests

from config import app_config, app_active

config = app_config[app_active]

# Guardamos o token em memória para não precisar fazer login a cada requisição
access_token = None

class ProdutoNaoEncontrado(Exception):
    pass

class LivroFlaskIndisponivel(Exception):
    pass

def login():
    global access_token

    url = '%s/login_api/' % config.LIVRO_FLASK_URL.rstrip('/')
    data = {
        'email': config.LIVRO_FLASK_EMAIL,
        'password': config.LIVRO_FLASK_PASSWORD
    }

    response = requests.post(url, json=data, timeout=5)
    response.raise_for_status()

    access_token = response.headers['access_token']

def request_product(product_id):
    url = '%s/product/%s' % (config.LIVRO_FLASK_URL.rstrip('/'), product_id)
    headers = {'access-token': access_token}

    return requests.get(url, headers=headers, timeout=5)

def get_product(product_id):
    try:
        if access_token is None:
            login()

        response = request_product(product_id)

        # O token do livro_flask expira, então fazemos um novo login e tentamos mais uma vez
        if response.status_code == 401:
            login()
            response = request_product(product_id)

        data = response.json()
        if response.status_code == 400 and not data.get('result'):
            raise ProdutoNaoEncontrado('Produto %s não encontrado no livro_flask' % product_id)

        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise LivroFlaskIndisponivel('Não foi possível consultar o livro_flask: %s' % e)

    return data['result']
