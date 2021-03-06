import numpy as np
from copy import deepcopy
from random import choice
import regex

patterns_my = [
    ['11111'],
    ['011110'],
    ['11011'], ['11101', '10111'], ['11110', '01111'],
    ['001110', '011100'], ['011010', '010110'],
    ['11001', '10011'], ['01110'], ['11010', '01101', '01011', '10110'], ['10101'],
    ['010010'], ['010100', '001010'], ['001100'], ['011000', '000110'],
    ['10001'], ['11000', '00011'], ['10010', '01001'], ['10100', '00101'], ['01010'],
    ['010000', '000010'], ['001000', '000100']
    # ['10000', '01000', '00100', '00010', '00001']
]
patterns_op = [
    ['22222'],
    ['022220'],
    ['22022'], ['22202', '20222'], ['22220', '02222'],
    ['002220', '022200'], ['022020', '020220'],
    ['22002', '20022'], ['02220'], ['22020', '02202', '02022', '20220'], ['20202'],
    ['020020'], ['020200', '002020'], ['002200'], ['022000', '000220'],
    ['20002'], ['22000', '00022'], ['20020', '02002'], ['20200', '00202'], ['02020'],
    ['020000', '000020'], ['002000', '000200']
    # ['20000', '02000', '00200', '00020', '00002']
]


def update_feature_by_str(string, my_f, op_f, sign=1):
    for i in range(len(patterns_my)):
        for mod in patterns_my[i]:
            my_f[i] += sign * len(regex.findall(mod, string, overlapped=False))
    for i in range(len(patterns_op)):
        for mod in patterns_op[i]:
            op_f[i] += sign * len(regex.findall(mod, string, overlapped=False))
    return


class Board:
    def __init__(self, board, network, turn=1, offend=1, actions=None, explore_prob=0.2):
        if actions is None:
            actions = []
        self.board = np.array(board)
        self.network = network
        self.turn = turn
        self.offend = offend
        self.actions = actions
        self.explore_prob = explore_prob
        self.width = self.board.shape[0]
        self.height = self.board.shape[1]
        self._init_feature()
        self.feature = self.extract_feature()

    def _init_feature(self):
        self.feature_my = np.zeros(len(patterns_my) + 1)
        self.feature_op = np.zeros(len(patterns_op) + 1)
        self.feature_my[-1] = int(self.turn == 1)
        self.feature_op[-1] = int(self.turn == 2)
        # row
        for j in range(self.height):
            string = ''.join(str(int(self.board[i][j])) for i in range(self.width))
            update_feature_by_str(string, self.feature_my, self.feature_op)
        # col
        for i in range(self.width):
            string = ''.join(str(int(self.board[i][j])) for j in range(self.height))
            update_feature_by_str(string, self.feature_my, self.feature_op)
        # diag ????????????
        for center in range(self.height):
            string = ''
            for expand in range(self.height):
                if expand == 0:
                    string += str(int(self.board[center][center]))
                else:
                    if 0 <= center + expand < self.height \
                            and 0 <= center - expand < self.height:
                        string = str(int(self.board[center + expand][center - expand])) \
                                 + string \
                                 + str(int(self.board[center - expand][center + expand]))
                    else:
                        break
            update_feature_by_str(string, self.feature_my, self.feature_op)
        # oblique diag
        for center in range(self.height):
            string = ''
            for expand in range(self.height):
                if expand == 0:
                    string += str(int(self.board[self.height - 1 - center][center]))
                else:
                    if 0 <= center + expand < self.height \
                            and 0 <= center - expand < self.height:
                        string = str(int(self.board[self.height - 1 - center - expand][center - expand])) \
                                 + string \
                                 + str(int(self.board[self.height - 1 - center + expand][center + expand]))
                    else:
                        break
            update_feature_by_str(string, self.feature_my, self.feature_op)

    def _update_feature(self, x, y):
        self.feature_my[-1] = int(self.turn == 1)
        self.feature_op[-1] = int(self.turn == 2)
        # row
        string = ''.join(str(int(self.board[i][y])) for i in range(self.width))
        update_feature_by_str(string, self.feature_my, self.feature_op)
        string = string[0:x] + '0' + string[(x + 1):self.width]
        update_feature_by_str(string, self.feature_my, self.feature_op, -1)
        # col
        string = ''.join(str(int(self.board[x][j])) for j in range(self.height))
        update_feature_by_str(string, self.feature_my, self.feature_op)
        string = string[0:y] + '0' + string[(y + 1):self.height]
        update_feature_by_str(string, self.feature_my, self.feature_op, -1)
        # diag
        string = str(int(self.board[x][y]))
        string2 = '0'
        for expand in range(1, self.height):
            if 0 <= x + expand < self.width \
                    and 0 <= y - expand < self.height:
                string = str(int(self.board[x + expand][y - expand])) + string
                string2 = str(int(self.board[x + expand][y - expand])) + string2
            if 0 <= x - expand < self.width \
                    and 0 <= y + expand < self.height:
                string = string + str(int(self.board[x - expand][y + expand]))
                string2 = string2 + str(int(self.board[x - expand][y + expand]))
        update_feature_by_str(string, self.feature_my, self.feature_op)
        update_feature_by_str(string2, self.feature_my, self.feature_op, -1)
        # oblique diag
        string = str(int(self.board[x][y]))
        string2 = '0'
        for expand in range(1, self.height):
            if 0 <= x + expand < self.width \
                    and 0 <= y + expand < self.height:
                string = str(int(self.board[x + expand][y + expand])) + string
                string2 = str(int(self.board[x + expand][y + expand])) + string2
            if 0 <= x - expand < self.width \
                    and 0 <= y - expand < self.height:
                string = string + str(int(self.board[x - expand][y - expand]))
                string2 = string2 + str(int(self.board[x - expand][y - expand]))
        update_feature_by_str(string, self.feature_my, self.feature_op)
        update_feature_by_str(string2, self.feature_my, self.feature_op, -1)

    def update_board(self, x, y):
        self.board[x, y] = self.turn
        self.turn = 3 - self.turn
        self.update_actions(self.actions, x, y)
        self._update_feature(x, y)

    def update_actions(self, actions, x, y, k=1):
        if (x, y) in actions:
            actions.remove((x, y))
        for i in range(x - k, x + k + 1):
            for j in range(y - k, y + k + 1):
                if 0 <= i < self.width and 0 <= j < self.height \
                        and self.board[i][j] == 0 and (i, j) not in actions:
                    actions.append((i, j))
        return

    def adjacent_actions(self, k=1):
        actions = []
        for x in np.arange(self.width):
            for y in np.arange(self.height):
                if self.board[x, y] > 0:
                    self.update_actions(actions, x, y, k)
        return actions

    def extract_feature(self):
        lst = []
        # my
        for i in range(len(self.feature_my)):
            num = self.feature_my[i]
            if i == len(self.feature_my) - 1:  # turn
                lst.append(num)
            else:
                if num >= 1:
                    lst.append(int(self.turn == 1))
                    lst.append(int(self.turn == 2))
                else:
                    lst.append(0)
                    lst.append(0)
                if i == 0:  # ???5
                    continue
                for j in range(4):
                    if num >= 1:
                        lst.append(1)
                        num -= 1
                    else:
                        lst.append(0)
                lst.append(num / 2)
        # op
        for i in range(len(self.feature_op)):
            num = self.feature_op[i]
            if i == len(self.feature_op) - 1:
                lst.append(num)
            else:
                if num >= 1:
                    lst.append(int(self.turn == 1))
                    lst.append(int(self.turn == 2))
                else:
                    lst.append(0)
                    lst.append(0)
                if i == 0:  # ???5
                    continue
                for j in range(4):
                    if num >= 1:
                        lst.append(1)
                        num -= 1
                    else:
                        lst.append(0)
                lst.append(num / 2)
        # offend
        lst.append(int(self.offend == 1))
        lst.append(int(self.offend == 2))
        f = np.array(lst).reshape(len(lst), 1)
        return f

    def evaluation(self, feature=None):
        if feature is None:
            feature = self.extract_feature()
        params_values = self.network.params
        value, _ = self.network.full_forward_propagation(feature, params_values)
        return value

    def Q_value(self, legal_actions=None):
        if legal_actions is None:
            legal_actions = self.actions
        besta = None
        if self.turn == 1:
            bestq = float('-inf')
            for a in legal_actions:
                newBoard = deepcopy(self)
                newBoard.update_board(a[0], a[1])
                q = newBoard.evaluation() + np.random.rand() / 10000
                if q > bestq:
                    bestq = q
                    besta = a
        else:
            bestq = float('inf')
            for a in legal_actions:
                newBoard = deepcopy(self)
                newBoard.update_board(a[0], a[1])
                q = newBoard.evaluation() + np.random.rand() / 10000
                if q < bestq:
                    bestq = q
                    besta = a

        return bestq, besta

    def e_greedy(self, e=None):
        if self.actions is None:
            self.actions = self.adjacent_actions
        if e is None:
            e = self.explore_prob

        if np.random.rand() > e:
            _, action = self.Q_value(self.actions)
        else:
            action = choice(self.actions)

        return action

    def is_win(self):
        length = self.width
        color = 1
        op = 3 - color
        # column
        for x in range(length - 4):
            for y in range(length):
                pieces = tuple(self.board[x + d][y] for d in range(5))
                if pieces.count(color) == 5:
                    return color
                if pieces.count(op) == 5:
                    return op
        # row
        for x in range(length):
            for y in range(length - 4):
                pieces = tuple(self.board[x][y + d] for d in range(5))
                if pieces.count(color) == 5:
                    return color
                if pieces.count(op) == 5:
                    return op
        # positive diagonal
        for x in range(length - 4):
            for y in range(length - 4):
                pieces = tuple(self.board[x + d][y + d] for d in range(5))
                if pieces.count(color) == 5:
                    return color
                if pieces.count(op) == 5:
                    return op
        # oblique diagonal
        for x in range(length - 4):
            for y in range(4, length):
                pieces = tuple(self.board[x + d][y - d] for d in range(5))
                if pieces.count(color) == 5:
                    return color
                if pieces.count(op) == 5:
                    return op
        return False

    def get_candidate(self, n=5):
        if len(self.actions) <= n:
            return self.actions

        a_q = []
        for a in self.actions:
            newBoard = deepcopy(self)
            newBoard.update_board(a[0], a[1])
            a_q.append((a, newBoard.evaluation()))

        if self.turn == 1:
            a_q.sort(key=lambda x: x[1], reverse=True)
        else:
            a_q.sort(key=lambda x: x[1])
        actions = [x[0] for x in a_q[:n]]
        return actions

    def minimax_3l(self, legal_actions=None):
        if legal_actions is None:
            legal_actions = self.get_candidate()

        a_q = []
        for a1 in legal_actions:
            newBoard1 = deepcopy(self)
            newBoard1.update_board(a1[0], a1[1])
            q2 = []
            for a2 in newBoard1.get_candidate():
                newBoard2 = deepcopy(newBoard1)
                newBoard2.update_board(a2[0], a2[1])
                q, _ = newBoard2.Q_value()
                q2.append(q)
            q1 = max(q2) if newBoard1.turn == 1 else min(q2)
            a_q.append((a1, q1))

        a_q.sort(key=lambda x: x[1])
        if self.turn == 1:
            return a_q[-1][0]
        else:
            return a_q[0][0]

    def minimax(self, legal_actions=None):
        if legal_actions is None:
            legal_actions = self.get_candidate()

        a_q = []
        for a in legal_actions:
            newBoard = deepcopy(self)
            newBoard.update_board(a[0], a[1])
            q, _ = newBoard.Q_value()
            a_q.append((a, q))

        a_q.sort(key=lambda x: x[1])
        if self.turn == 1:
            return a_q[-1][0]
        else:
            return a_q[0][0]
