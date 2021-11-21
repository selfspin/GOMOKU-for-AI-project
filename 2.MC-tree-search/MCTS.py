import copy
import pisqpipe as pp
import time
from fast_actions import *
from random import choice, random
from main import logDebug


class MCTS(object):

    def __init__(self, board, color, actions, fea_my, fea_op):
        self.board = board
        self.color = color
        self.actions = actions
        self.fea_my = fea_my
        self.fea_op = fea_op
        self.max_simulation_times = 10
        self.max_depth = 20
        self.explorationProb = 0.5
        self.reward = {}

    def get_action(self):
        times = 0
        while times < self.max_simulation_times:
            board_new = copy.deepcopy(self.board)

            # select
            x, y = self.select()
            board_new[x][y] = self.color
            actions_new = update_actions(board_new, self.actions, x, y)
            fea_my_new, fea_op_new = update_features(board_new, x, y, self.fea_my, self.fea_op)

            # expand
            x_op, y_op = self.expand(board_new, actions_new, fea_my_new, fea_op_new)
            board_new[x_op][y_op] = 3 - self.color
            actions_new = update_actions(board_new, actions_new, x_op, y_op)

            # simulation
            r = self.simulation(board_new, self.color, actions_new, self.max_depth)

            # backpropagation
            if (x, y) in self.reward:
                rw = self.reward[(x, y)]
                rw[0] += r
                rw[1] += 1
                self.reward[(x, y)] = rw
            else:
                self.reward[(x, y)] = [r, 1]

            times += 1

        max_mean_reward = -1
        action = None
        for a in self.reward:
            rw = self.reward[a]
            mean_reward = rw[0] / rw[1] + rw[1]/self.max_simulation_times
            if mean_reward > max_mean_reward:
                max_mean_reward = mean_reward
                action = a
        return action

    def select(self):
        actions_value = order_actions(self.board, self.actions, self.fea_my, self.fea_op, self.color)
        actions = [x[0] for x in actions_value]
        if random() < self.explorationProb:
            return choice(actions)
        else:
            return actions[0]

    def expand(self, board, actions, fea_my, fea_op):
        actions_value = order_actions(board, actions, fea_my, fea_op, 3 - self.color)
        actions = [x[0] for x in actions_value]
        if random() < self.explorationProb:
            return choice(actions)
        else:
            return actions[-1]

    def simulation(self, board, color, actions, max_depth):
        for _ in range(max_depth):
            if self.is_win(board, color):
                v = 1.0 if color == 1 else 0.0
                return v
            a = fast_kill_action(board, color)
            if a is not None:
                x, y = a
                board[x][y] = color
                actions = update_actions(board, actions, x, y)
            else:
                x, y = choice(actions)
                board[x][y] = color
                actions = update_actions(board, actions, x, y)
            color = 3 - color

        return 0.5

    def is_win(self, board, color):
        boardLength = pp.width
        # column
        for x in range(boardLength - 4):
            for y in range(boardLength):
                pieces = tuple(board[x + d][y] for d in range(5))
                if pieces.count(color) == 5:
                    return True
        # row
        for x in range(boardLength):
            for y in range(boardLength - 4):
                pieces = tuple(board[x][y + d] for d in range(5))
                if pieces.count(color) == 5:
                    return True
        # positive diagonal
        for x in range(boardLength - 4):
            for y in range(boardLength - 4):
                pieces = tuple(board[x + d][y + d] for d in range(5))
                if pieces.count(color) == 5:
                    return True
        # oblique diagonal
        for x in range(boardLength - 4):
            for y in range(4, boardLength):
                pieces = tuple(board[x + d][y - d] for d in range(5))
                if pieces.count(color) == 5:
                    return True
        return False


def order_actions(board, actions, fea_my, fea_op, color):
    """
    return a list [(action, value)]
    """
    action_value = []
    for action in actions:
        x, y = action
        board[x][y] = color
        fea_my_new, fea_op_new = update_features(board, x, y, fea_my, fea_op)
        v = utility(fea_my_new, fea_op_new)
        action_value.append((action, v))
        board[x][y] = 0
    action_value.sort(key=lambda e: e[1], reverse=True)
    return action_value
