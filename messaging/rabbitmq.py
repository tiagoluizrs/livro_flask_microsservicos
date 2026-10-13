# -*- coding: utf-8 -*-
import os
import json
import pika

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'guest')
QUEUE_PEDIDO_CRIADO = 'pedido_criado'

def publish_pedido_criado(pedido):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    ))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_PEDIDO_CRIADO, durable=True)

    body = json.dumps({
        'pedido_id': pedido.id,
        'product_id': pedido.product_id,
        'qtd': pedido.qtd
    })

    channel.basic_publish(
        exchange='',
        routing_key=QUEUE_PEDIDO_CRIADO,
        body=body,
        properties=pika.BasicProperties(delivery_mode=2)
    )
    connection.close()
