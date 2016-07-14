#!/bin/python3

import curses

from window import *
from config import *
from vbox import *

class Content(Window):
    def __init__(self, properties):
        super().__init__(properties)
        self.vbox = VBox()
        self.vbox.start()
        self.index = 0

    def draw(self):
        self.blank_line(0, 0, color_pair=2)
        self.init_table_head()
        self.table_head()
        self.table_content()

    def init_table_head(self):
        self.th = (
            {'name': 'ID'     , 'size': 5},
            {'name': 'NAME'   , 'size': self.w - 51},
            {'name': 'OS_TYPE', 'size': 20},
            {'name': 'MEMORY' , 'size': 12},
            {'name': 'STATUS' , 'size': 12}
        )

    def table_head(self):
        y, x = 0, 1
        self.window.move(y, x)
        self.window.attron(curses.color_pair(2))
        for item in self.th:
            self.window.addstr(item['name'])
            x += item['size']
            self.window.move(y, x)
        self.window.attroff(curses.color_pair(2))

    def table_content(self):
        y, x = 1, 1
        for i, vm in enumerate(self.vbox.vms):
            self.window.move(y, x)
            if i == self.index:
                self.blank_line(y, 0, color_pair=1)
                self.print_line(vm, y, active=True)
            else:
                self.print_line(vm, y)
            y += 1

    def print_line(self, vm, y, active=False):
        x = 1
        names = ['id', 'name', 'os_type', 'memory', 'status']

        self.window.move(y, x)

        if active == True:
            self.window.attron(curses.color_pair(1))

        for i, key in enumerate(names):
            if key == 'status':
                self.print_vm_status(vm['status'], active)
                continue
            self.window.addstr(str(vm[key]))
            x += self.th[i]['size']
            self.window.move(y, x)
        
        if active == True:
            self.window.attroff(curses.color_pair(1))

    def print_vm_status(self, status, active):
        color_pair = 3
        if active == True and status == 'RUNNING':
            color_pair = 1
        elif active == False and status == 'RUNNING':
            color_pair = 4
        elif active == True and status == 'OFF':
            color_pair = 1
        elif active == False and status == 'OFF':
            color_pair = 3

        self.window.attron(curses.color_pair(color_pair))
        self.window.addstr(status)
        self.window.attroff(curses.color_pair(color_pair))

    def index_inc(self):
        if self.index < len(self.vbox.vms) - 1:
            self.index += 1

    def index_dec(self):
        if self.index > 0:
            self.index -= 1
