
import os
import dotenv
dotenv.load_dotenv()


# flask app
RANDOM_STRING = os.getenv("RANDOM_STRING", "random string")
APP_NAME = "Suggestions Crawler"
FLASK_HOST = os.getenv("FLASK_HOST", 'localhost')
FLASK_PORT = os.getenv("FLSAK_PORT", 5000)

# params for db
DB_URL = os.environ.get('POSTGRESQL_URL')

# params for rabbit queue
RABITMQ_URL = os.environ.get(
    'RABITMQ_URL', "amqp://guest:guest@localhost:5672//")

# RABITMQ_URL=amqp://vzfrhuaa:27Jr-CXjNQ6wuoMgo3XuW_PJAbdrREaK@whale.rmq.cloudamqp.com/vzfrhuaa

# params for proxy

# configs for crawler

