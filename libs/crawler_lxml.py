
import threading
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from lxml import html as lxml_html

from libs.rabbit_wrapper import RabbitQueue
from libs.ship import Ship
from settings import (DRIVER_PATH, IS_HEADLESS, NUM_WORKERS,
    CRAWLER_QUEUE_NAME, CRAWLER_EXCHANGE_NAME
)
from libs.db_pg import DbPg
from libs.init_logger import init_logger
from libs.proxy_manager import ProxyManager


USE_PROXY = False


class VesselCrawlerLxml:
    def __init__(self, ex_ev):
        self.log = init_logger(self.__class__.__name__)
        if USE_PROXY:
            self.proxy_gen = ProxyManager(
                self.log, ok_timeout=30, ban_timeout=1000)
        self.workers = []
        self.exit_event = ex_ev

    def run(self):
        for wnum in range(NUM_WORKERS):
            worker = threading.Thread(
                target=self.work, args=(wnum,), daemon=True
            )
            self.workers.append(worker)

        for w in self.workers:
            w.start()

        while not self.exit_event.is_set():
            count_alive = [int(w.is_alive()) for w in self.workers]

            self.log.debug(f'VesselCrawler is working: {count_alive} of '
                           f'{NUM_WORKERS} is alive')
            if self.exit_event.wait(30):
                break
        for w in self.workers:
            w.join()
        self.log.info('VesselCrawler exit run')

    def init_browser(self):
        prox = None
        driver = None
        while not self.exit_event.is_set():
            if USE_PROXY:
                prox = self.proxy_gen.next_proxy()

                self.log.debug(f'try proxy: {prox}')
                try:
                    status = prox.check_proxy()
                except Exception as e0:
                    self.log.debug(f'bad proxy: {prox}: {e0}')
                    self.proxy_gen.back_proxy(prox, str(e0))
                    continue
                self.log.debug(f'proxy: {prox}: {status}: OK')

            # setup chrome options
            # https://www.andressevilla.com/running-chromedriver-with-python-selenium-on-heroku/
            chrome_options = Options()
            # chrome_options.binary_location = "/path/to/chrome.exe"
            chrome_options.add_argument("--incognito")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")

            # chrome_options.add_argument("--user-data-dir="/path/to/profile")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options = webdriver.ChromeOptions()
            if IS_HEADLESS:
                chrome_options.add_argument('headless')
            chrome_options.add_argument('--no-sandbox')

            if USE_PROXY:
                proxy_str = '--proxy-server=https://{0}:{1}'.format(
                    prox.ip, str(prox.port))
                chrome_options.add_argument(proxy_str)

            driver = webdriver.Chrome(chrome_options=chrome_options,
                                      executable_path=DRIVER_PATH)
            driver.implicitly_wait(10)
            break

        return driver, prox

    def work(self, wnum):
        self.log.debug(f'{wnum} worker started')
        rab_connection = RabbitQueue(CRAWLER_EXCHANGE_NAME, CRAWLER_QUEUE_NAME)
        db_connection = DbPg(self.log)
        driver, prox = self.init_browser()

        for raw_msg in rab_connection.get_generator(self.exit_event):
            if not raw_msg:
                if self.exit_event.wait(2):
                    break
                continue

            msg = raw_msg.json()

            if 'url' not in msg:
                self.log.warning(f'{wnum}: bad task: {msg}')
                raw_msg.ack()
                continue

            if msg['num'] == 0:
                msg['url'] = msg['url'].split('?')[0]

            try:
                driver.get(msg['url'])

                self.log.debug(driver.current_url)
                time.sleep(3)

                html = driver.page_source
                dom = lxml_html.fromstring(html)

                # parse with selenium
                rows = dom.cssselect("tr")
                if not rows:
                    self.log.debug(f'{wnum}: not rows in table')
                    raw_msg.nack(requeue=True)
                    break

                for row in rows:
                    cells = row.cssselect("td")
                    if not cells:
                        continue

                    data = {
                        'img_url': cells[0].cssselect('img')[0].get('src'),
                        'country': cells[1].cssselect('span')[0].get('title'),
                        'vessel_name': cells[1].cssselect('a')[0].text_content().strip(),
                        'vessel_type': cells[1].cssselect('small')[0].text_content().strip(),
                        'year': cells[2].text_content(),
                        'gt': cells[3].text_content(),
                        'dwt': cells[4].text_content(),
                        'sz': cells[5].text_content()
                    }
                    vlength, vwidth = [int(v.strip()) for v in data['sz'].split('/')]
                    self.log.debug(data)
                    ship = Ship(
                        sid=None,
                        name=data['vessel_name'],
                        country_name=data['country'],
                        description=f'{data["vessel_type"]}, {data["img_url"]}',
                        built_year=data['year'],
                        length=vlength,
                        width=vwidth,
                        gt=data['gt'],
                        dwt=data['dwt']
                    )
                    db_connection.insert_ship(ship)
                db_connection.exec_query(f'''
                    INSERT INTO pages (page_num)
                    VALUES({msg['num']})
                ''')
                raw_msg.ack()
            except Exception as e0:
                self.log.error(f'{wnum}: get page error: {e0}')
                raw_msg.nack(requeue=True)
                if USE_PROXY:
                    self.proxy_gen.back_proxy(prox, str(e0))
                try:
                    driver.close()
                except:
                    pass
                if not self.exit_event.is_set():
                    driver, prox = self.init_browser()
            time.sleep(random.randrange(1, 5))

        try:
            rab_connection.close()
            db_connection.close()
            driver.close()
        except:
            pass
        self.log.info(f'{wnum}: worker exit')
