# Game.py

import curses

from race import Race


def quit_game():
    curses.endwin()


def draw_frame(win):
    win.border(0)
    win.addstr(0, 24, ' CAMEL RACE ')
    win.addstr(0, 45, ' ESC to Quit ')


def init_window():
    curses.initscr()
    curses.noecho()
    curses.curs_set(0)

    win = curses.newwin(20, 60, 0, 0)
    win.keypad(1)
    win.border(0)
    win.nodelay(1)

    draw_frame(win)

    return win


def game():
    window = init_window()
    race = Race(window)
    race.run()
    quit_game()


if __name__ == '__main__':
    game()
