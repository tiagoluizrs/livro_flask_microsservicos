# livro_flask_microsservicos

Serviço de pedidos, criado nos capítulos sobre microsserviços do livro Flask de A a Z (part-4).

Esse serviço conversa com o projeto principal (`livro_flask`) de quatro formas diferentes: REST, RabbitMQ, Kafka e gRPC.

## Python

O projeto foi desenvolvido com o Python 3.15 (as versões das `libs` do `requirements.txt` foram congeladas nele) e também foi testado com o Python 3.14, que é o usado nas imagens Docker.

## Rodando com Docker

As pastas `livro_flask` e `livro_flask_microsservicos` precisam estar lado a lado. Crie o `.env` dos dois projetos a partir do `.env.example` de cada um. No `.env` deste projeto, use um usuário dos dados de exemplo do `livro_flask` (por exemplo `LIVRO_FLASK_EMAIL=admin@email.com` e `LIVRO_FLASK_PASSWORD=123456`, veja o `README.md` do `livro_flask`). Nesse mesmo `.env`, preencha a `LIVRO_FLASK_SECRET_KEY` com o mesmo valor da `SECRET_KEY` do `.env` do `livro_flask`, pois é com ela que o serviço de pedidos valida os tokens. Depois, na raiz deste projeto, rode:

```
docker compose up -d --build
```

| Serviço | Endereço |
|---|---|
| livro_flask (admin e API REST) | http://localhost:8000 |
| Serviço de pedidos | http://localhost:8100 |
| Painel do RabbitMQ | http://localhost:15672 (usuário `estoque`, senha `estoque123`) |

## Usando a API

As rotas de pedidos exigem um token. Faça login no `livro_flask` (`POST http://localhost:8000/login_api/`), copie o token do `header` `access_token` da resposta e envie-o no `header` `access-token` das requisições para `http://localhost:8100/pedidos`.

Para saber mais conheça o livro: https://www.casadocodigo.com.br/products/livro-flask-a-z
