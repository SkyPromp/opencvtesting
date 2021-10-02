import random


class Point:
    def __init__(self, direction, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.direction = direction
        self.edges = ""

    def checkEdges(self):
        self.edges = ""
        if self.x - 1 >= 0:
            self.edges += "L"
        elif self.x + 1 < self.w:
            self.edges += "R"
        elif self.y - 1 >= 0:
            self.edges += "U"
        elif self.y + 1 < self.h:
            self.edges += "D"

        return self.edges

    def next(self):
        operations = {"L": {0: ("D"), 1: (-1, 0, "L"), 2: ("U")},
                      "R": {0: ("U"), 1: (1, 0, "R"), 2: ("D")},
                      "U": {0: ("L"), 1: (0, -1, "U"), 2: ("R")},
                      "D": {0: ("R"), 1: (0, 1, "D"), 2: ("L")}}

        x_adder, y_adder, self.direction = operations[self.direction][random.randint(0, 3)]

        self.x += x_adder
        self.y += y_adder
