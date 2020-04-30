
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

# params for proxy

# configs for crawler

