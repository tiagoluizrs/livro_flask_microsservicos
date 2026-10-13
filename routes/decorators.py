# -*- coding: utf-8 -*-
from functools import wraps

import jwt
from flask import request, abort

from config import app_config, app_active

config = app_config[app_active]

def auth_token_required(f):
    @wraps(f)
    def verify_token(*args, **kwargs):
        try:
            access_token = request.headers['access_token']
        except KeyError:
            abort(401, 'Você precisa enviar um token de acesso')

        try:
            jwt.decode(access_token, config.LIVRO_FLASK_SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            abort(401, 'Token expirado, realize um novo login')
        except jwt.InvalidTokenError:
            abort(401, 'Token inválido')

        return f(*args, **kwargs)

    return verify_token
