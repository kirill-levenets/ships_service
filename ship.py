
class Ship:
    def __init__(
        self, name, country, ship_description, built_year, length=100,
            width=200, gt=None, dwt=None):
        self.ship_id = None
        self.country_id = None

        self.name = name
        self.country_name = country
        self.ship_description = ship_description
        self.length = length
        self.width = width
        self.gt = gt
        self.dwt = dwt
        self.built_year = built_year

    def __str__(self):
        return f'{self.name} [{self.country_name} - {self.built_year}]'

    def __repr__(self):
        return f'{self.name} [{self.country_name} - {self.built_year}]'

