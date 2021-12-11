from board import *
import regex

live_3_my = ['011100', '011010']
rest_4_my = ['01111', '10111', '11011']
live_4_my = ['011110']
win_my = ['11111']

dict_block = {'011100': [1, 5], '011010': [1, 4, 6],
              '01111': [1], '10111': [2], '11011': [3],
              '022200': [1, 5], '022020': [1, 4, 6],
              '02222': [1], '20222': [2], '22022': [3]
              }

live_3_op = ['022200', '022020']
rest_4_op = ['02222', '20222', '22022']
live_4_op = ['022220']
win_op = ['22222']

direction = [(1, 1), (1, 0), (0, 1), (1, -1)]


def pattern_exchange():
    global live_3_my, live_3_op
    mid = live_3_my
    live_3_my = live_3_op
    live_3_op = mid
    global live_4_my, live_4_op
    mid = live_4_my
    live_4_my = live_4_op
    live_4_op = mid
    global rest_4_my, rest_4_op
    mid = rest_4_my
    rest_4_my = rest_4_op
    rest_4_op = mid
    global win_my, win_op
    mid = win_my
    win_my = win_op
    win_op = mid
    return


def op_turn(x):
    return int(3 - x)


class TSS:
    def __init__(self, bd: Board):
        self.board = bd.board.copy()
        self.acts = bd.adjacent_actions(2)
        self.turn = bd.turn
        self.width = bd.width
        self.height = bd.height

    def is_free(self, x, y):
        if self.is_legal(x, y) and self.board[x][y] == 0:
            return True
        return False

    def is_legal(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return True
        return False

    @staticmethod
    def num2str(x):
        return str(int(x))

    @staticmethod
    def reverse(s):
        return s[::-1]

    def check_five(self, x, y, turn):
        for (dx, dy) in direction:
            num = 1
            for i in range(1, 5):
                if self.is_legal(x + i * dx, y + i * dy) and \
                        self.board[x + i * dx, y + i * dy] == turn:
                    num += 1
                else:
                    break
            for i in range(1, 5):
                if self.is_legal(x - i * dx, y - i * dy) and \
                        self.board[x - i * dx, y - i * dy] == turn:
                    num += 1
                else:
                    break
            if num >= 5:
                return True
        return False

    def check_four(self, x, y, turn):
        flag = 0
        turn = int(turn)
        if turn != int(live_3_my[0][1]):
            pattern_exchange()

        pos = None
        for (dx, dy) in direction:
            s = str(turn)
            for i in range(1, 5):
                if self.is_legal(x + i * dx, y + i * dy):
                    s = self.num2str(self.board[x + i * dx][y + i * dy]) + s
                else:
                    break
            xypos = len(s) - 1
            for i in range(1, 5):
                if self.is_legal(x - i * dx, y - i * dy):
                    s += self.num2str(self.board[x - i * dx][y - i * dy])
                else:
                    break

            for mod in live_4_my:
                if len(regex.findall(mod, s)) > 0:
                    return 'win', None

            for mod in rest_4_my:
                if s.find(mod) >= 0:
                    flag += 1
                    k = s.find(mod) + dict_block[mod][0] - 1 - xypos
                    pos = (x - k * dx, y - k * dy)
                    if flag >= 2:
                        return 'win', None
                    break
                elif s.find(self.reverse(mod)) >= 0:
                    flag += 1
                    k = s.find(self.reverse(mod)) + (len(mod) - dict_block[mod][0] + 1) - 1 - xypos
                    pos = (x - k * dx, y - k * dy)
                    if flag >= 2:
                        return 'win', None
                    break

        if flag:
            return 'rest', pos

        return False, None

    def block_four(self, x, y, turn):
        # 封堵
        op_result, _ = self.check_four(x, y, op_turn(turn))
        # 对手堵的时候形成冲4
        if op_result:
            return False
        return True

    # Victory of Continuous Four
    def VCF(self, x, y, turn):
        if self.check_five(x, y, turn):
            return True
        result, pos = self.check_four(x, y, turn)
        if result == 'win':
            return True
        elif result == 'rest':
            self.board[x][y] = turn
            bx, by = pos
            if not self.block_four(bx, by, turn):  # 对手封堵过程形成冲4
                self.board[x][y] = 0
                return False
            self.board[bx][by] = op_turn(turn)

            ans = False
            for dx, dy in direction:
                for i in range(-4, 5):
                    nx = x + i * dx
                    ny = y + i * dy
                    if not self.is_free(nx, ny):
                        continue
                    ans = ans or self.VCF(nx, ny, turn)
                    if ans:
                        self.board[bx][by] = 0
                        self.board[x][y] = 0
                        return True

            self.board[bx][by] = 0
            self.board[x][y] = 0
            return False
        else:
            return False

    def check_three(self, x, y, turn):
        flag = 0
        turn = int(turn)
        if turn != int(live_3_my[0][1]):
            pattern_exchange()

        pos = []
        for (dx, dy) in direction:
            s = str(turn)
            for i in range(1, 5):
                if self.is_legal(x + i * dx, y + i * dy):
                    s = self.num2str(self.board[x + i * dx][y + i * dy]) + s
                else:
                    break
            xypos = len(s) - 1
            for i in range(1, 5):
                if self.is_legal(x - i * dx, y - i * dy):
                    s += self.num2str(self.board[x - i * dx][y - i * dy])
                else:
                    break

            for mod in live_3_my:
                if s.find(mod) >= 0:
                    flag += 1
                    for p in dict_block[mod]:
                        k = s.find(mod) + p - 1 - xypos
                        pos.append((x - k * dx, y - k * dy))
                    if flag >= 2:
                        return 'win', None
                    break
                elif s.find(self.reverse(mod)) >= 0:
                    flag += 1
                    for p in dict_block[mod]:
                        k = s.find(self.reverse(mod)) + (len(mod) - p + 1) - 1 - xypos
                        pos.append((x - k * dx, y - k * dy))
                    if flag >= 2:
                        return 'win', None
                    break

        if flag:
            return 'live', pos

        return False, None

    def block_three(self, myx, myy, pos, turn):
        for x, y in pos:
            # 封堵
            op_result, _ = self.check_four(x, y, op_turn(turn))
            if op_result:  # 遇到冲4必凉
                return False
            op_result, _ = self.check_three(x, y, op_turn(turn))
            if op_result == 'win':  # 遇到双3也凉
                return False
            elif op_result == 'live' and not self.VCF(myx, myy, turn):  # 遇到单3但是没法VCF，也冀了
                return False
        return True

    # Victory of Continuous Three
    def VCT(self, x, y, turn):
        if self.VCF(x, y, turn):
            return True
        result3, pos3 = self.check_three(x, y, turn)
        result4, pos4 = self.check_four(x, y, turn)
        if result3 == 'win' or result4 == 'win' \
                or (result3 == 'live' and result4 == 'rest' and pos4 not in pos3):
            return True
        elif result4 == 'rest':
            self.board[x][y] = turn
            bx, by = pos4
            if not self.block_four(bx, by, turn):  # 对手封堵过程形成冲4
                self.board[x][y] = 0
                return False
            self.board[bx][by] = op_turn(turn)

            ans = False
            for dx, dy in direction:
                for i in range(-4, 5):
                    nx = x + i * dx
                    ny = y + i * dy
                    if not self.is_free(nx, ny):
                        continue
                    ans = ans or self.VCT(nx, ny, turn)
                    if ans:
                        self.board[bx][by] = 0
                        self.board[x][y] = 0
                        return True

            self.board[bx][by] = 0
            self.board[x][y] = 0
            return False
        elif result3 == 'live':
            self.board[x][y] = turn
            # 所有可能的堵法都堵上，使得下一个攻击手段与堵法无关
            for bx, by in pos3:
                self.board[bx][by] = op_turn(turn)

            if not self.block_three(x, y, pos3, turn):  # 对手封堵过程形成威胁
                self.board[x][y] = 0
                for bx, by in pos3:
                    self.board[bx][by] = 0
                return False

            ans = False
            for dx, dy in direction:
                for i in range(-4, 5):
                    nx = x + i * dx
                    ny = y + i * dy
                    if not self.is_free(nx, ny):
                        continue
                    ans = ans or self.VCT(nx, ny, turn)
                    if ans:
                        for bx, by in pos3:
                            self.board[bx][by] = 0
                        self.board[x][y] = 0
                        return True

            for bx, by in pos3:
                self.board[bx][by] = 0
            self.board[x][y] = 0
            return False
        else:
            return False

    def solve(self):
        # 确定pattern
        if self.turn != int(live_3_my[0][1]):
            pattern_exchange()

        # 自己成5
        for (x, y) in self.acts:
            if self.check_five(x, y, self.turn):
                return [(x, y)]

        # 检查对手已有冲4
        for (x, y) in self.acts:
            if self.check_five(x, y, op_turn(self.turn)):
                return [(x, y)]

        # 自己VCF
        for (x, y) in self.acts:
            if self.VCF(x, y, self.turn):
                return [(x, y)]

        # 对手VCF
        kill = []
        for (x, y) in self.acts:
            if self.VCF(x, y, op_turn(self.turn)):
                kill.append((x, y))
        num = len(kill)
        if num == 1:
            return kill
        elif num >= 2:
            rnt = []
            for (x, y) in kill:
                flag = True
                self.board[x][y] = self.turn
                for kx, ky in kill:
                    if kx == x and ky == y:
                        continue
                    if self.VCF(kx, ky, op_turn(self.turn)):
                        flag = False
                        break
                self.board[x][y] = 0
                if flag:
                    rnt.append((x, y))
            return rnt

        # 自己VCT
        for (x, y) in self.acts:
            if self.VCT(x, y, self.turn):
                return [(x, y)]

        # 对手VCT
        kill = []
        for (x, y) in self.acts:
            if self.VCT(x, y, op_turn(self.turn)):
                kill.append((x, y))
        num = len(kill)
        if num == 1:
            return kill
        elif num >= 2:
            rnt = []
            for (x, y) in kill:
                flag = True
                self.board[x][y] = self.turn
                for (kx, ky) in kill:
                    if kx == x and ky == y:
                        continue
                    if self.VCT(kx, ky, op_turn(self.turn)):
                        flag = False
                        break
                self.board[x][y] = 0
                if flag:
                    rnt.append((x, y))
            return rnt

        return []

'''
bd0 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 1, 2, 2, 0, 0, 2, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
       ]

bd1 = [[1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 2, 0],
       [0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0],
       [0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
       [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
       ]

bd2 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
       [0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0],
       [0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
       ]

bd3 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 2, 1, 1, 2, 0, 0, 0, 0],
       [0, 0, 0, 2, 1, 0, 1, 2, 0, 0, 0, 0],
       [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
       ]

B = TSS(Board(bd0, None))
print(B.solve())
'''
