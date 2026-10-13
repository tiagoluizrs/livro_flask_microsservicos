# -*- coding: utf-8 -*-
from flask import Blueprint, request, Response, json

from controller.Pedido import PedidoController
from routes.decorators import auth_token_required

pedidos_bp = Blueprint('pedidos', __name__)

@pedidos_bp.route('/')
def index():
    return 'Serviço de pedidos no ar'

@pedidos_bp.route('/pedidos', methods=['POST'])
@auth_token_required
def create_pedido():
    pedido = PedidoController()
    response = pedido.create_pedido(request.json)
    return Response(json.dumps(response, ensure_ascii=False), mimetype='application/json'), response['status']

@pedidos_bp.route('/pedidos/<int:pedido_id>', methods=['GET'])
@auth_token_required
def get_pedido(pedido_id):
    pedido = PedidoController()
    response = pedido.get_pedido_by_id(pedido_id)
    return Response(json.dumps(response, ensure_ascii=False), mimetype='application/json'), response['status']

@pedidos_bp.route('/pedidos', methods=['GET'])
@auth_token_required
def get_pedidos():
    pedido = PedidoController()
    response = pedido.get_pedidos()
    return Response(json.dumps(response, ensure_ascii=False), mimetype='application/json'), response['status']
