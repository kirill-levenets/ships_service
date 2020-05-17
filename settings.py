
import os
import dotenv
dotenv.load_dotenv()


# flask app
RANDOM_STRING = os.getenv("RANDOM_STRING", "random string")
APP_NAME = "ships service"
FLASK_HOST = os.getenv("FLASK_HOST", 'localhost')
FLASK_PORT = os.getenv("FLSAK_PORT", 5000)


# params for db
DB_URL = os.environ.get(
    'POSTGRESQL_URL',
    'postgresql://kirl:123456@localhost/postgres?port=5432'
)

# params for rabbit queue
RABITMQ_URL = os.environ.get(
    'RABITMQ_URL',
    "amqp://guest:guest@localhost:5672//"
)

CRAWLER_QUEUE_NAME = "crawl_pages"
CRAWLER_EXCHANGE_NAME = "ex_crawl_pages"
MAX_QUEUE_SIZE = 100


# params for proxy
PROXY_FILE_PATH = "static/proxies.txt"


# configs for crawler
DRIVER_PATH = "bin/chromedriver"  # path to driver binary
IS_HEADLESS = False
NUM_WORKERS = 1
MAX_PAGES = 23_867
PAGE_URL = "https://www.vesselfinder.com/vessels?page={num}"

