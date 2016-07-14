#!/bin/python3

import curses

from curses import (
    COLOR_BLACK,
    COLOR_WHITE,
    COLOR_RED,
    COLOR_GREEN,
    COLOR_BLUE,
    COLOR_YELLOW
)

from config import *
from title import *
from content import *
from status import *
from menu import *

class Screen:
    def __init__(self):
        self.ch = ""
        self.stdscr = curses.initscr()
        self.init_attributes()
        self.init_colors()
        self.init_windows()

    def destroy(self):
        curses.endwin()
        self.content.vbox.stop_thread()

    def init_attributes(self):
        curses.noecho()
        curses.cbreak()
        curses.curs_set(False)
        self.stdscr.nodelay(True)
        self.stdscr.timeout(1000)
        self.stdscr.keypad(True)
        self.calculate_maxyx()

    def calculate_maxyx(self):
        self.y, self.x = self.stdscr.getmaxyx()

    def init_colors(self):
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, COLOR_BLACK , COLOR_WHITE)
        curses.init_pair(2, COLOR_WHITE , COLOR_BLUE)
        curses.init_pair(3, COLOR_RED   , NO_COLOR)
        curses.init_pair(4, COLOR_GREEN , NO_COLOR)
        curses.init_pair(5, COLOR_YELLOW, NO_COLOR)
        curses.init_pair(6, COLOR_RED   , COLOR_WHITE)
        curses.init_pair(7, COLOR_GREEN , COLOR_WHITE)

    def set_windows_properties(self):
        self.wp = {}
        self.wp['title'] = {'h': 1, 'w': self.x + 1, 'y': 0, 'x': 0}
        self.wp['content'] = {'h': self.y - 3, 'w': self.x + 1, 'y': 1, 'x': 0}
        self.wp['status'] = {'h': 1, 'w': self.x + 1, 'y': self.y - 2, 'x': 0}
        self.wp['menu'] = {'h': 1, 'w': self.x + 1, 'y': self.y - 1, 'x': 0}

    def init_windows(self):
        self.set_windows_properties()
        self.title = Title(APP_NAME, self.wp['title'])
        self.content = Content(self.wp['content'])
        self.status = Status(self.wp['status'])
        self.menu = Menu(self.wp['menu'])

    def draw(self):
        self.title.draw()
        self.content.draw()
        self.status.draw()
        self.menu.draw()
        self.refresh(allow=1)

    def redraw(self):
        if self.was_resized():
            self.title.draw()
            self.status.draw()
            self.menu.draw()
        self.content.draw()
        self.refresh()

    def clear(self):
        if self.was_resized():
            self.title.clear()
            self.status.clear()
            self.menu.clear()
        self.content.clear()

    def refresh(self, allow=0):
        self.stdscr.refresh()
        if allow == 1 or self.was_resized():
            self.title.refresh()
            self.status.refresh()
            self.menu.refresh()
        self.content.refresh()

    def recalculate(self):
        if self.was_resized():
            self.calculate_maxyx()
            self.title.resize(1, self.x + 1)
            self.content.resize(self.y - 3, self.x + 1)
            self.status.resize(1, self.x + 1)
            self.menu.resize(1, self.x + 1)

    def analyze(self):
        if self.ch == curses.KEY_DOWN:
            self.content.index_inc()
        elif self.ch == curses.KEY_UP:
            self.content.index_dec()
        elif self.ch == ord('R'):
            self.content.vbox.run_vm(self.content.index)
        elif self.ch == ord('S'):
            self.content.vbox.stop_vm(self.content.index)

    def was_resized(self):
        if self.ch == curses.KEY_RESIZE:
            return True
        return False

    def getch(self):
        self.ch = self.stdscr.getch()

    def stop_vbox_thread(self):
        self.content.vbox.stop_thread()
