#!/bin/python3

import curses

class Window:
    def __init__(self, properties):
        self.h = properties['h']
        self.w = properties['w']
        self.y = properties['y']
        self.x = properties['x']
        self.create()

    def create(self):
        self.window = curses.newwin(
            self.h, self.w,
            self.y, self.x
        )

    def blank_line(self, y, x, color_pair=0):
        self.window.move(y, x)

        if color_pair > 0:
            self.window.attron(curses.color_pair(color_pair))
        
        for _ in range(self.w - 1):
            self.window.addstr(" ")
        
        if color_pair > 0:
            self.window.attroff(curses.color_pair(color_pair))

    def resize(self, height, width):
        self.h, self.w = height, width
        self.window.resize(height, width)

    def refresh(self):
        self.window.refresh()

    def clear(self):
        self.window.clear()
