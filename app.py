from flask import (
    Flask,
)
from config import secret_key
from routes.api import main as route_api


def configured_app():
    app = Flask(__name__)
    app.secret_key = secret_key
    app.register_blueprint(route_api, url_prefix='/api')
    return app


if __name__ == '__main__':
    app = configured_app()
    config = {
        'debug': False,
        'host': '0.0.0.0',
        'port': 80,
        'threaded': True,
    }
    app.run(**config)
