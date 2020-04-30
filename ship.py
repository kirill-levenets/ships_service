
class Ship:
    __slots__ = (
        'id', 'name', 'country_name',
        'description', 'built_year', 'length', 'width', 'gt', 'dwt'
    )

    def __init__(
        self, sid, name, country_name, description, built_year, length=100,
            width=200, gt=None, dwt=None):
        self.id = sid
        self.name = name
        self.country_name = country_name
        self.description = description
        self.length = length
        self.width = width
        self.gt = gt
        self.dwt = dwt
        self.built_year = built_year

    def __str__(self):
        return f'{self.name} [{self.country_name} - {self.built_year}]'

    def __repr__(self):
        return f'{self.name} [{self.country_name} - {self.built_year}]'

    def make_dict(self):
        # TODO: prepare dict from this object
        pass


if __name__ == '__main__':
    s = Ship(1, 2, 3, 4, 5, 6, 7, 8, 9)
    print(s.make_dict())


