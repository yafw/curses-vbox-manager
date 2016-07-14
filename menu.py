#!/bin/python3

import curses

from window import *

MENU = (
    {'scut': 'R', 'desc': 'Run'},
    {'scut': 'S', 'desc': 'Stop'},
    {'scut': 'Q', 'desc': 'Quit'}
)

class Menu(Window):
    def __init__(self, properties):
        super().__init__(properties)

    def draw(self):
        for i, item in enumerate(MENU):
            self.print_shortcut(item['scut'])
            self.print_description(item['desc'])

    def print_shortcut(self, shortcut):
        self.window.attron(curses.A_BOLD)
        self.window.addstr("%s " % shortcut)
        self.window.attroff(curses.A_BOLD)

    def print_description(self, description):
        self.window.addstr("%s  " % description)
