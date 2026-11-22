# -*- coding: utf-8 -*-
import os
import json
from kafka import KafkaProducer

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
TOPIC_PEDIDOS = 'pedidos'

_producer = None

def _get_producer():
    global _producer
    if _producer is None:
        _producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
    return _producer

def publish_pedido_evento(pedido):
    producer = _get_producer()
    producer.send(TOPIC_PEDIDOS, {
        'pedido_id': pedido.id,
        'product_id': pedido.product_id,
        'product_name': pedido.product_name,
        'qtd': pedido.qtd,
        'preco_total': str(pedido.preco_total)
    })
    producer.flush()
