
from flask import g, current_app
import psycopg2

from settings import DB_URL
from ship import Ship


def get_db():
    if 'db' not in g:
        g.db = DbPg()
    return g.db


FIELDS = 'ships.id as sid, ships.name as name, countries.name as country_name, ' \
         'ship_description, ' \
         'built_year, length, width, gt, dwt'


class DbPg:
    def __init__(self, db_url=DB_URL):
        """
        create db connection and cursor
        :param db_url:
        """
        self.con = psycopg2.connect(db_url)
        self.cur = self.con.cursor()

    def get_ships(self, num=10):
        query = f"SELECT {FIELDS} FROM ships " \
                f"INNER JOIN countries ON countries.id = ships.country_id " \
                f"ORDER BY ships.id ASC " \
                f"LIMIT {num}"
        self.cur.execute(query)
        for params in self.cur:
            yield Ship(*params)

    def get_ship_by_name(self, ship_name):
        query = f"SELECT {FIELDS} FROM ships " \
                f"INNER JOIN countries ON countries.id = ships.country_id " \
                f"WHERE ships.name = %s"
        self.cur.execute(query, (ship_name,))
        params = self.cur.fetchone()
        current_app.logger.info(f'get_ship_by_name [{ship_name}]: {params}')
        return Ship(*params)

    def update_ship(self, ship):
        ret_message = 'Ship updated'
        query = """
            UPDATE ships 
            SET 
                name = %(name)s, 
                country_id = (
                    SELECT id from countries WHERE name=%(country_name)s), 
                ship_description = %(description)s, 
                built_year = %(built_year)s
            WHERE id = %(id)s
        """
        try:
            self.cur.execute(query, ship.make_dict())
            self.con.commit()
        except Exception as e0:
            ret_message = f'Error on update: {e0}'
            current_app.logger.error(ret_message)
        return ret_message

    def insert_ship(self, ship):
        ret_message = 'Ship inserted'
        query = """
            INSERT INTO ships (name, country_id, ship_description, built_year) 
            VALUES (
                %(name)s,
                (SELECT id from countries WHERE name=%(country_name)s), 
                %(description)s, %(built_year)s)
        """
        try:
            self.cur.execute(query, ship.make_dict())
            self.con.commit()
        except Exception as e0:
            ret_message = f'Error on insert: {e0}'
            current_app.logger.error(ret_message)
        return ret_message


    def del_ship(self, ship_name):
        if not ship_name:
            return

        query = """
            DELETE FROM ships 
            WHERE name = %s
        """

        self.cur.execute(query, (ship_name,))
        self.con.commit()

    def get_countries(self):
        # TODO: implement
        query = f"SELECT name FROM countries"
        self.cur.execute(query)
        for params in self.cur:
            yield params[0]

    def close(self):
        self.cur.close()
        self.con.close()
