#  helpers
import time
from random import randint

letter_a = ord('a')
letter_z = ord('z')


def get_curr_time(zero_time):
    return int(round((time.time() - zero_time) * 1000))


def generate_keys(command_letters, turbo_letters):
    commands = set()
    turbo_boost = False

    while len(commands) < 3:
        next_command = command_letters[randint(0, letter_z - letter_a)]
        if next_command in turbo_letters:
            if not turbo_boost:
                turbo_boost = True
            else:
                continue

        commands.add(next_command)

    return list(commands)
