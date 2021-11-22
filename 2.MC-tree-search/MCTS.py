import copy
import main as mn
import fast_actions as fa
import random
import pisqpipe as pp
from math import sqrt, log


def have_winner(bd):
    # 返回获胜的颜色，没有就返回0
    boardLength = pp.width
    # column
    for x in range(boardLength - 4):
        for y in range(boardLength):
            pieces = tuple(bd[x + d][y] for d in range(5))
            if pieces.count(1) == 5:
                return 1
            elif pieces.count(2) == 5:
                return 2
    # row
    for x in range(boardLength):
        for y in range(boardLength - 4):
            pieces = tuple(bd[x][y + d] for d in range(5))
            if pieces.count(1) == 5:
                return 1
            elif pieces.count(2) == 5:
                return 2
    # positive diagonal
    for x in range(boardLength - 4):
        for y in range(boardLength - 4):
            pieces = tuple(bd[x + d][y + d] for d in range(5))
            if pieces.count(1) == 5:
                return 1
            elif pieces.count(2) == 5:
                return 2
    # oblique diagonal
    for x in range(boardLength - 4):
        for y in range(4, boardLength):
            pieces = tuple(bd[x + d][y - d] for d in range(5))
            if pieces.count(1) == 5:
                return 1
            elif pieces.count(2) == 5:
                return 2
    return 0


class Node:
    def __init__(self, bd, from_action, action, color, fa=None, score=0):  # 从board开始，下了from_action一步
        self.state = copy.deepcopy(bd)
        self.a = from_action
        self.reward = 0
        self.visit_count = 1
        self.A = copy.deepcopy(action)
        self.color = color
        self.fa = fa
        self.son = {}
        self.score = score

        x, y = self.a
        self.state[x][y] = self.color
        mn.update_actions(self.state, self.A, x, y)
        self.score += mn.update_score(self.state, x, y)

    def towards(self, action):
        if action in self.son.keys():
            self.son[action].fa = None
            return self.son[action]
        return Node(self.state, action, self.A, 3 - self.color, score=self.score)

    def is_terminal(self, depth):
        if depth > mn.MAX_DEPTH or have_winner(self.state):
            return True
        return False

    def expand(self):
        act = random.choice(self.A)
        son = Node(self.state, act, self.A, 3 - self.color, fa=self, score=self.score)
        self.son[act] = son
        self.A.remove(act)
        return son

    def best_son(self):
        if self.color == 1:
            maxv = float('-inf')
            a = None
            for v in self.son.values():
                q = v.reward / v.visit_count + sqrt(log(self.visit_count) / v.visit_count) \
                    + v.score / log(v.visit_count + 1)
                if q > maxv:
                    maxv = q
                    a = v
            return a
            # return max([(v.reward / v.visit_count + sqrt(log(self.visit_count) / v.visit_count), v)
            #            for v in self.son.values()])[1]
        else:
            minv = float('inf')
            a = None
            for v in self.son.values():
                q = v.reward / v.visit_count + sqrt(log(self.visit_count) / v.visit_count) \
                    + v.score / log(v.visit_count + 1)
                if q < minv:
                    minv = q
                    a = v
            return a
            # return min([(v.reward / v.visit_count + sqrt(log(self.visit_count) / v.visit_count), v)
            #             for v in self.son.values()])[1]


class MCTS_Algorithm:
    def __init__(self, node, max_actions=30):
        self.root = node
        self.max_actions = max_actions

    def UCT(self):
        for i in range(self.max_actions):
            mn.logDebug(str(i))
            node = self.Tree_Policy(self.root)
            mn.logDebug(str(self.root.A))
            r = self.policy(node)
            self.back(node, r)
        rt = self.root
        mn.logDebug(str(rt.son))
        return max([(v.reward/v.visit_count + sqrt(log(rt.visit_count)/v.visit_count), v.a)
                    for v in rt.son.values()])[1]

    def Tree_Policy(self, node):
        depth = 1
        while not node.is_terminal(depth):
            node.visit_count += 1
            if node.A:
                return node.expand()
            else:
                node = node.best_son()
            depth += 1
        return node

    def policy(self, node):
        bd = copy.deepcopy(node.state)
        now_color = node.color
        act_list = copy.deepcopy(node.A)
        depth = 0
        while not have_winner(bd) and depth < 10:
            act = fa.fast_kill_action(bd, now_color)
            if act is None:
                # logDebug(str(act_list))
                act = random.choice(act_list)
            x, y = act
            bd[x][y] = now_color
            mn.update_actions(bd, act_list, x, y)
            depth += 1
            now_color = 3 - now_color
        x = have_winner(bd)
        if x == 1:
            return 1
        elif x == 2:
            return 0
        else:
            return 0.1

    def back(self, node, r):
        while node is not None:
            node.visit_count += 1
            node.reward += r
            node = node.fa
        return
