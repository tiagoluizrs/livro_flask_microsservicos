# -*- coding: utf-8 -*-
from decimal import Decimal

from model.Pedido import Pedido
from messaging.rabbitmq import publish_pedido_criado
from messaging.kafka_producer import publish_pedido_evento
from services.livro_flask_client import ProdutoNaoEncontrado, LivroFlaskIndisponivel
from config import app_config, app_active

if app_config[app_active].LIVRO_FLASK_CLIENT == 'grpc':
    from services.livro_flask_grpc_client import get_product
else:
    from services.livro_flask_client import get_product

class EstoqueInsuficiente(Exception):
    pass

class PedidoController():
    def __init__(self):
        self.pedido_model = Pedido()

    def create_pedido(self, obj):
        result = {}
        try:
            qtd = int(obj['qtd'])
            product = get_product(obj['product_id'])

            if int(product['qtd']) < qtd:
                raise EstoqueInsuficiente('Estoque insuficiente para esse produto')

            preco_unitario = Decimal(product['price'])

            pedido = Pedido()
            pedido.product_id = product['id']
            pedido.product_name = product['name']
            pedido.qtd = qtd
            pedido.preco_unitario = preco_unitario
            pedido.preco_total = preco_unitario * qtd
            pedido.status = 'pendente'

            if pedido.save():
                try:
                    publish_pedido_criado(pedido)
                except Exception as e:
                    # Não deixamos a falha no envio da mensagem derrubar a criação do pedido
                    print('Erro ao publicar mensagem no RabbitMQ:', e)

                try:
                    publish_pedido_evento(pedido)
                except Exception as e:
                    print('Erro ao publicar evento no Kafka:', e)

                result = {
                    'id': pedido.id,
                    'product_id': pedido.product_id,
                    'product_name': pedido.product_name,
                    'qtd': pedido.qtd,
                    'preco_unitario': str(pedido.preco_unitario),
                    'preco_total': str(pedido.preco_total),
                    'status': pedido.status
                }
                status = 201
            else:
                result = {'message': 'Erro ao salvar o pedido'}
                status = 400
        except ProdutoNaoEncontrado as e:
            result = {'message': str(e)}
            status = 404
        except EstoqueInsuficiente as e:
            result = {'message': str(e)}
            status = 400
        except LivroFlaskIndisponivel as e:
            print(e)
            result = {'message': 'Não foi possível consultar o produto, tente novamente mais tarde'}
            status = 503
        except Exception as e:
            print(e)
            result = {'message': 'Dados inválidos para criação do pedido'}
            status = 400
        return {
            'result': result,
            'status': status
        }

    def get_pedido_by_id(self, pedido_id):
        result = {}
        try:
            self.pedido_model.id = pedido_id
            res = self.pedido_model.get_by_id()

            if res is None:
                result = {'message': 'Pedido não encontrado'}
                status = 404
            else:
                result = {
                    'id': res.id,
                    'product_id': res.product_id,
                    'product_name': res.product_name,
                    'qtd': res.qtd,
                    'preco_unitario': str(res.preco_unitario),
                    'preco_total': str(res.preco_total),
                    'status': res.status,
                    'date_created': res.date_created
                }
                status = 200
        except Exception as e:
            print(e)
            result = {'message': 'Erro ao buscar o pedido'}
            status = 400
        return {
            'result': result,
            'status': status
        }

    def get_pedidos(self):
        result = []
        try:
            res = self.pedido_model.get_all()
            for r in res:
                result.append({
                    'id': r.id,
                    'product_id': r.product_id,
                    'product_name': r.product_name,
                    'qtd': r.qtd,
                    'preco_unitario': str(r.preco_unitario),
                    'preco_total': str(r.preco_total),
                    'status': r.status,
                    'date_created': r.date_created
                })
            status = 200
        except Exception as e:
            print(e)
            result = []
            status = 400
        return {
            'result': result,
            'status': status
        }
