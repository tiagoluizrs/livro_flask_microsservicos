import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    SECRET = os.getenv('SECRET_KEY', 'troque-essa-chave-em-producao')
    APP = None

    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '123')
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_PORT = os.getenv('MYSQL_PORT', '3306')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'livro_flask_microsservicos')
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://%s:%s@%s:%s/%s' % (
        MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE
    )

    # Endereço onde a API do livro_flask (o projeto principal) está rodando
    LIVRO_FLASK_URL = os.getenv('LIVRO_FLASK_URL', 'http://localhost:8000')
    LIVRO_FLASK_EMAIL = os.getenv('LIVRO_FLASK_EMAIL', '')
    LIVRO_FLASK_PASSWORD = os.getenv('LIVRO_FLASK_PASSWORD', '')

    # Mesma SECRET_KEY do livro_flask, usada para validar os tokens que ele gera
    LIVRO_FLASK_SECRET_KEY = os.getenv('LIVRO_FLASK_SECRET_KEY', '')

    # Endereço do servidor gRPC do livro_flask e qual forma de comunicação usar na consulta de produtos (rest ou grpc)
    LIVRO_FLASK_GRPC_HOST = os.getenv('LIVRO_FLASK_GRPC_HOST', 'localhost:50051')
    LIVRO_FLASK_CLIENT = os.getenv('LIVRO_FLASK_CLIENT', 'rest')

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    IP_HOST = os.getenv('IP_HOST', 'localhost')
    PORT_HOST = 8100
    URL_MAIN = 'http://%s:%s/' % (IP_HOST, PORT_HOST)

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    IP_HOST = os.getenv('IP_HOST', 'localhost')
    PORT_HOST = 5100
    URL_MAIN = 'http://%s:%s/' % (IP_HOST, PORT_HOST)

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    IP_HOST = os.getenv('IP_HOST', 'localhost')
    PORT_HOST = 8180
    URL_MAIN = 'http://%s:%s/' % (IP_HOST, PORT_HOST)

app_config = {
    'development': DevelopmentConfig(),
    'testing': TestingConfig(),
    'production': ProductionConfig()
}

app_active = os.getenv('FLASK_ENV')
