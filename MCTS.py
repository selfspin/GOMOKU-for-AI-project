import copy
import pisqpipe as pp
from fast_actions import *
from random import choice
from main import logDebug


class MCTS(object):

    def __init__(self, board, color, actions, fea_my, fea_op):
        self.board = board
        self.color = color
        self.actions = actions
        self.fea_my = fea_my
        self.fea_op = fea_op
        self.max_simulation_times = 3
        self.max_depth = 20

    def get_action(self):
        action_reward = []

        # expand
        actions_value = order_actions_adj(self.board, self.actions, self.fea_my, self.fea_op)[0:3]
        s = sum([x[1] for x in actions_value]) + 0.1
        prior = [x[1]/s for x in actions_value]
        actions = [x[0] for x in actions_value]

        # simulation
        i = 0
        for a in actions:
            reward = 0
            times = 0
            x, y = a
            board_new = copy.deepcopy(self.board)
            board_new[x][y] = self.color
            actions_new = update_actions(self.board, actions, x, y, 2)
            while times < self.max_simulation_times:
                r = self.simulation(self.board, 3 - self.color, actions_new, self.max_depth)
                reward += r
                times += 1
                logDebug('times ' + str(times))
            # bayes adjust
            reward = reward * prior[i]
            action_reward.append((a, reward))
            i += 1

        action_reward.sort(key = lambda x: x[1], reverse = True)
        logDebug('action choice ' + str(action_reward))
        return action_reward[0][0]

    def simulation(self, board_init, color, actions, max_depth):
        board = copy.deepcopy(board_init)
        for d in range(max_depth):
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


def order_actions_adj(board, actions, fea_my, fea_op):
    action_value = []
    actions_adj = copy.deepcopy(actions)
    for action in actions_adj:
        x, y = action
        board_new = copy.deepcopy(board)
        board_new[x][y] = 1
        fea_my_new, fea_op_new = update_features(board_new, x, y, fea_my, fea_op)
        v = utility(fea_my_new, fea_op_new)
        action_value.append((action, v))
    action_value.sort(key=lambda x: x[1], reverse=True)
    return action_value
