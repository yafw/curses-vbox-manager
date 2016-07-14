#!/bin/python3

import curses

from window import *

class Title(Window):
    def __init__(self, title, properties):
        super().__init__(properties)
        self.title = title

    def draw(self):
        self.blank_line(0, 0, color_pair=1)
        self.print_title()

    def print_title(self):
        title_length = len(self.title)
        max_length = self.w - 6

        self.window.move(0, 1)
        self.window.attron(curses.color_pair(1))

        for i in range(title_length):
            if i > max_length:
                self.window.addstr("...")
                break
            self.window.addstr(self.title[i])
        
        self.window.attroff(curses.color_pair(1))
