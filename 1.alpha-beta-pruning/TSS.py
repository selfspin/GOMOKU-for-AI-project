import pisqpipe as pp
from copy import deepcopy

mod = [['011110'],
       ['211110', '11101', '11011', '10111', '01111'],
       ['1111'],
       ['01110', '010110', '011010']]


class TSS:
    def __init__(self, bd, actions):
        self.board = deepcopy(bd)
        self.actions = deepcopy(actions)

    def main(self):
        act = self.threat_space_search(2)
        if act is None:
            return self.threat_space_search(1)
        return act

    def is_free(self, x, y):
        if x >= 0 and y >= 0 and x < pp.width and y < pp.height and self.board[x][y] != 0:
            return True
        return False

    def threat_space_search(self, color):
        for x in range(pp.width):
            for y in range(pp.height):
                if self.board[x][y]:
                    continue

