
from libs.db_pg import DbPg
from libs.init_logger import init_logger
from libs.rabbit_wrapper import RabbitQueue
from settings import (CRAWLER_QUEUE_NAME, CRAWLER_EXCHANGE_NAME,
                      PAGE_URL, MAX_PAGES, MAX_QUEUE_SIZE)


class ShipsGenerator:
    def __init__(self, exit_event):
        self.exit_event = exit_event
        self.log = init_logger('ships_url_generator')
        self.was_pages = {}

        self.db = DbPg(self.log)
        self.rqueue = RabbitQueue(CRAWLER_EXCHANGE_NAME, CRAWLER_QUEUE_NAME)

        self.wait_queue()
        self.init_progress_table()
        self.get_ready_tasks()

    def wait_queue(self):
        while self.rqueue.count() > 0:
            self.log.info('Generator waiting ...')
            if self.exit_event.wait(10):
                break

    def get_ready_tasks(self):
        query = '''SELECT * FROM pages'''
        for row in self.db.get_query(query):
            self.was_pages[row[0]] = True
        self.log.debug(f'total ready tasks: {len(self.was_pages)}')

    def run(self):
        for i in range(MAX_PAGES):
            if self.exit_event.is_set():
                break

            if self.was_pages.get(i):
                continue

            msg = {'url': PAGE_URL.format(num=i),
                   'num': i}

            self.log.debug(f'[{i}]: queue size is: {self.rqueue.count()}')
            while self.rqueue.count() > MAX_QUEUE_SIZE:
                self.log.info('Queue too big, wait')
                if self.exit_event.wait(5):
                    return

            self.rqueue.publish(msg)
        self.log.info('all tasks are generated')

    def init_progress_table(self):
        query = '''CREATE TABLE IF NOT EXISTS pages (page_num integer UNIQUE )'''
        self.db.exec_query(query)
