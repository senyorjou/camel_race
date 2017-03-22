import random


class Camel(object):
    def advance(self, adv, turbo, terrain):
        extra_adv = self.extra_adv(terrain) if turbo else 1
        return adv * extra_adv

    def extra_adv(self, terrain):
        if terrain == self.fav_terrain:
            return self.turbo_plus
        return self.turbo_boost

    @property
    def id(self):
        return '{}-{}'.format(self.name, str(random.randint(10, 99)))


class Bactrian(Camel):
    name = 'Bactrian'
    turbo_boost = 1.15
    turbo_plus = 1.30
    fav_terrain = 'mud'


class Domestic(Camel):
    name = 'Domestic'
    turbo_boost = 1.20
    turbo_plus = 1.30
    fav_terrain = 'grass'


class Dromedary(Camel):
    name = 'Dromedary'
    turbo_boost = 1.25
    turbo_plus = 1.35
    fav_terrain = 'sand'


class Player(object):
    def __init__(self, camel, human=False):
        self.camel = camel
        self.id = camel.id
        self.plays = []
        self.last_key = ''
        self.x = 0.0
        self.human = human

    def advance(self, **kwargs):
        adv = self.camel.advance(**kwargs)
        self.x += adv if adv else 0

    def progress(self, track_length):
        return '▖' * int(self.x)

    def shoot(self):
        pass
