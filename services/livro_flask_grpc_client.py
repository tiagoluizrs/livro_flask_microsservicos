# -*- coding: utf-8 -*-
import grpc
import requests

from config import app_config, app_active
from protos import produto_pb2, produto_pb2_grpc
from services import livro_flask_client
from services.livro_flask_client import ProdutoNaoEncontrado, LivroFlaskIndisponivel

config = app_config[app_active]

def request_product(product_id):
    with grpc.insecure_channel(config.LIVRO_FLASK_GRPC_HOST) as channel:
        stub = produto_pb2_grpc.ProdutoServiceStub(channel)
        request = produto_pb2.ProdutoRequest(id=int(product_id))
        metadata = [('access-token', livro_flask_client.access_token)]
        return stub.GetProduto(request, timeout=5, metadata=metadata)

def get_product(product_id):
    try:
        # O login continua sendo feito pela API REST, que é quem gera os tokens
        if livro_flask_client.access_token is None:
            livro_flask_client.login()

        try:
            response = request_product(product_id)
        except grpc.RpcError as e:
            # Se o token expirou, fazemos um novo login e tentamos mais uma vez
            if e.code() != grpc.StatusCode.UNAUTHENTICATED:
                raise
            livro_flask_client.login()
            response = request_product(product_id)
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            raise ProdutoNaoEncontrado(e.details())
        raise LivroFlaskIndisponivel('Não foi possível consultar o livro_flask via gRPC: %s' % e.details())
    except requests.exceptions.RequestException as e:
        raise LivroFlaskIndisponivel('Não foi possível fazer login no livro_flask: %s' % e)

    return {
        'id': response.id,
        'name': response.name,
        'qtd': response.qtd,
        'price': response.price
    }
