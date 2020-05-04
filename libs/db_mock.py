
from flask import g


def get_db():
    if 'db' not in g:
        g.db = Db()
    return g.db


class Db:
    ships = {}

    def __init__(self):
        pass

    @classmethod
    def get_ships(cls,):
        for key in Db.ships:
            yield Db.ships[key]

    @classmethod
    def upsert_ship(cls, ship):
        cls.ships[ship.name] = ship

    @classmethod
    def del_ship(cls, ship_name):
        if ship_name in cls.ships:
            cls.ships.pop(ship_name)

    def close(self):
        pass