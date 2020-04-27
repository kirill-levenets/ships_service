
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask

from settings import RANDOM_STRING, FLASK_HOST, FLASK_PORT


app = Flask(__name__)
app.config['SECRET_KEY'] = RANDOM_STRING


def init_app_logger():
    handler = RotatingFileHandler(
        'logs/ships.log', maxBytes=10_000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} '
        '%(levelname)s - %(message)s'
    )
    handler.setFormatter(file_formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)


if __name__ == '__main__':
    init_app_logger()
    with app.app_context():
        import app_routes

    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=True)

