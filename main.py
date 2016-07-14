#!/bin/python3

from screen import *

screen = Screen()               # most important class, it contains windows, curses settings, etc.
screen.draw()                   # draw title, content, status and menu (all windows)

while screen.ch != ord('Q'):
    screen.getch()              # capture pressed character
    screen.analyze()            # analyze pressed character and do something
    screen.recalculate()        # recalculate windows sizes if it is necessery
    screen.clear()              # clear windows screens if it is necessery
    screen.redraw()             # redraw content (other windows too if terminal was resized)

screen.destroy()                # destroy curses window, and vbox thread
