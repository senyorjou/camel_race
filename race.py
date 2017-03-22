# Race
import time
import random
from curses import A_BOLD, A_REVERSE

from models import Player, Bactrian, Domestic, Dromedary
from helpers import generate_keys, get_curr_time


letter_a = ord('a')
letter_z = ord('z')
command_letters = [chr(x) for x in range(letter_a, letter_z + 1)]
turbo_letters = ['u', 'i']
ESC = 27


class Turn(object):
    def __init__(self, start_time, players, lapse_time, adv):
        self.start_time = start_time
        self.players = {p.id: p for p in players}
        self.shooters = self.movers = []
        self.lapse_time = lapse_time
        self.adv = adv
        self.cmd_keys = generate_keys(command_letters, turbo_letters)

    def add_key(self, player, curr_time, key):
        player = self.players[player.id]
        if key in self.cmd_keys and key != player.last_key:
            player.last_key = key
            player.plays.append({'ts': curr_time, 'key': key})

    def check_movement(self, curr_time, terrain):
        for player in self.players.values():
            keys = [x['key'] for x in player.plays]
            tss = [x['ts'] for x in player.plays]

            # check shoot
            if player.id not in self.shooters:
                if keys[-6:] == self.cmd_keys + self.cmd_keys[::-1]:
                    player.shoot()
                    self.shooters.append(player)

            # Check movement
            if player.id not in self.movers:
                if keys[-3:] == self.cmd_keys:
                    turbo = any(x in self.cmd_keys for x in turbo_letters)
                    time_bonus = 1 if tss[-1] < self.lapse_time / 2 else 0.5
                    player.advance(adv=self.adv * time_bonus, turbo=turbo,
                                   terrain=terrain)
                    self.movers.append(player.id)

    def show_keys(self):
        return ' '.join(self.cmd_keys).upper()

    def show_player_keys(self, player):
        return ' '.join([x['key'] for x in self.players[player.id].plays][-3:])


class Race(object):
    def __init__(self, win, turn_time=3000, adv=1, num_players=4):
        self.win = win
        self.win.timeout(30)  # Lower timeout speedier cpu
        self.turn_time = turn_time
        self.adv = adv
        self.meter_length = 50
        self.track_length = 40
        self.max_players = 4
        self.num_players = num_players
        self.players = self.create_players()
        self.turns = []
        self.terrain = self.pick_terrain()

    def create_players(self):
        draft = [Bactrian, Domestic, Dromedary]

        def pick_camel():
            return draft[random.randint(0, len(draft) - 1)]()

        human = [Player(pick_camel(), human=True)]
        cpus = [Player(pick_camel()) for _ in range(self.num_players)]

        return human + cpus

    def draw_frame(self):
        self.win.border(0)
        self.win.addstr(0, 24, ' CAMEL RACE ')
        self.win.addstr(0, 45, ' ESC to Quit ')
        self.win.addstr(2, 2, 'Terrain: {}. Lapse Time: {}'
                              .format(self.terrain, self.turn_time))

    def draw_command(self, turn):
        self.win.addstr(17, 2, 'Type :' + turn.show_keys())

    def draw_meter(self, curr_time):
        progress = int(curr_time * self.meter_length / self.turn_time)

        bar = '█' * progress
        bar_bg = '░' * (self.meter_length - progress)
        self.win.addstr(18, 2, bar + bar_bg)

    def draw_players(self, turn):
        sep = '─' * 51
        lane = '─' * 30

        self.win.addstr(3, 2, sep)
        self.win.addstr(4, 2, 'Camel')
        self.win.addstr(4, 16, 'Keys')
        self.win.addstr(4, 23, 'Progress')
        self.win.addstr(5, 2, sep)

        for i, (player_id, player) in enumerate(turn.players.items()):
            row = i * 2 + 6
            style = A_REVERSE if player.human else A_BOLD
            self.win.addstr(row, 2, player_id, style)
            self.win.addstr(row, 16, turn.show_player_keys(player))
            self.win.addstr(row, 23, player.progress(self.track_length))
            self.win.addstr(row + 1, 23, lane)

    def pick_terrain(self):
        terrains = ['grass', 'neutral', 'mud', 'sand']

        return terrains[random.randint(0, len(terrains) - 1)]

    def run(self):
        key = 0
        winner = False
        zero_time = time.time()
        turn = Turn(zero_time, self.players, self.turn_time, self.adv)

        self.draw_frame()
        self.draw_command(turn)

        while key != ESC and not winner:
            curr_time = get_curr_time(zero_time)
            self.draw_meter(curr_time)
            self.draw_players(turn)

            # End turn
            if curr_time > self.turn_time:
                self.turns.append(turn)
                zero_time = time.time()
                turn = Turn(zero_time, self.players, self.turn_time, self.adv)
                self.draw_command(turn)
                key = 0

            #  If no key pressed... go on
            event = self.win.getch()
            key = key if event == -1 else event

            # Add key to players
            for player in self.players:
                if player.x >= self.track_length:
                    winner = True
                if player.human:
                    turn.add_key(player, curr_time, chr(key))
                else:
                    rnd_key = random.randint(letter_a, letter_z + 1)
                    turn.add_key(player, curr_time, chr(rnd_key))

            turn.check_movement(curr_time, self.terrain)

        self.winner()

    def winner(self):
        # clear screen
        for row in range(4, 19):
            self.win.addstr(row, 2, ' ' * 52)

        self.win.addstr(5, 2, '#  Camel name')
        self.win.addstr(5, 17, 'Distance')
        self.win.addstr(6, 2, '─' * 51)

        # draw winners
        arrival_list = sorted(self.players, key=lambda p: p.x, reverse=True)
        for row, player in enumerate(arrival_list):
            self.win.addstr(row + 7, 2, str(row + 1))
            self.win.addstr(row + 7, 4, str(player.id))
            self.win.addstr(row + 7, 17, str(player.x))

        key = 0
        while key != ESC:
            key = self.win.getch()
            continue
