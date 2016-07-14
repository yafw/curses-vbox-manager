#!/bin/python3

from window import *

class Status(Window):
    def __init__(self, properties):
        super().__init__(properties)

    def draw(self):
        self.blank_line(0, 0, color_pair=1)
