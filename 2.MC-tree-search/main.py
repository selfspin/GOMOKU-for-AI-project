import pisqpipe as pp
from pisqpipe import DEBUG_EVAL, DEBUG
import time
import traceback
import regex
from copy import deepcopy
from MCTS import *
# from fast_actions import *

pp.infotext = 'name="a-b-search", author="", version="1.0", country="China", www=""'

MAX_BOARD = 100
MAX_DEPTH = 10
board = [[0 for i in range(MAX_BOARD)] for j in range(MAX_BOARD)]
last_point = None
pattern1 = [['11111'],
            ['011110', '0101110', '0110110', '0111010'],
            ['11110', '11101', '11011', '10111', '01111'],
            ['1111'],
            ['01110', '010110', '011010'],
            ['11100', '11010', '10110', '00111', '01101', '01011'],
            ['111', '1011', '1101'],
            ['0110', '01010'],
            ['110', '011'],
            ['11']
            ]
pattern2 = [['22222'],
            ['022220', '0202220', '0220220', '0222020'],
            ['22220', '22202', '22022', '20222', '02222'],
            ['2222'],
            ['02220', '020220', '022020'],
            ['22200', '22020', '20220', '00222', '02202', '02022'],
            ['222', '2022', '2202'],
            ['0220', '02020'],
            ['220', '022'],
            ['22']
            ]
string_score = {}
score = 0
tick = time.time()
node = None


def brain_init():
    if pp.width < 5 or pp.height < 5:
        pp.pipeOut("ERROR size of the board")
        return
    if pp.width > MAX_BOARD or pp.height > MAX_BOARD:
        pp.pipeOut("ERROR Maximal board size is {}".format(MAX_BOARD))
        return
    pp.pipeOut("OK")


def brain_restart():
    for x in range(pp.width):
        for y in range(pp.height):
            board[x][y] = 0
    global node, last_point
    node = None
    last_point = None
    global score
    score = 0
    pp.pipeOut("OK")


def isFree(x, y):
    return x >= 0 and y >= 0 and x < pp.width and y < pp.height and board[x][y] == 0


def isfree(bd, x, y):
    return x >= 0 and y >= 0 and x < pp.width and y < pp.height and bd[x][y] == 0


def brain_my(x, y):
    logDebug('my move' + str((x, y)))
    if isFree(x, y):
        global node
        if last_point is None:
            node = Node(board, (x, y), [], 1)
        else:
            node = node.towards((x, y))
        board[x][y] = 1
    else:
        # for xi in range(pp.width):
        #     for yi in range(pp.height):
        #         if board[xi][yi]:
        #             logDebug(str([(xi, yi), board[xi][yi]]))
        pp.pipeOut("ERROR my move [{},{}]".format(x, y))


def brain_opponents(x, y):
    if isFree(x, y):
        global last_point, node
        if last_point is None:
            node = Node(board, (x, y), [], 2)
        else:
            node = node.towards((x, y))
        board[x][y] = 2
        last_point = (x, y)
    else:
        pp.pipeOut("ERROR opponents's move [{},{}]".format(x, y))


def brain_block(x, y):
    if isFree(x, y):
        board[x][y] = 3
    else:
        pp.pipeOut("ERROR winning move [{},{}]".format(x, y))


def brain_takeback(x, y):
    if x >= 0 and y >= 0 and x < pp.width and y < pp.height and board[x][y] != 0:
        board[x][y] = 0
        return 0
    return 2


def brain_turn():
    try:
        global tick
        tick = time.time()
        if pp.terminateAI:
            return
        if not last_point:
            action = (int(pp.width / 2), int(pp.height / 2))
            x, y = action
            pp.do_mymove(x, y)
            return

        action = fast_kill_action(board, 1)
        logDebug(str(action))
        if not action:
            solve = MCTS_Algorithm(node)
            action = solve.UCT()
        x, y = action
        pp.do_mymove(x, y)
    except Exception as e:
        logDebug(str(e.args))
        logDebug(str(traceback.format_exc()))
        # pass
        logTraceBack()


def brain_end():
    pass


def brain_about():
    pp.pipeOut(pp.infotext)


if DEBUG_EVAL:
    import win32gui


    def brain_eval(x, y):
        # check if it works as expected
        wnd = win32gui.GetForegroundWindow()
        dc = win32gui.GetDC(wnd)
        rc = win32gui.GetClientRect(wnd)
        c = str(board[x][y])
        win32gui.ExtTextOut(dc, rc[2] - 15, 3, 0, None, c, ())
        win32gui.ReleaseDC(wnd, dc)

# weight
coefmy = [1e11, 1e8, 1e8, 0, 1e6, 7e1, 0, 7e1, 5, 0]
coefop = [1e11, 5e7, 1e4, 0, 1e4, 5e1, 0, 7e1, 5, 0]


def update_score_string(s, position, chg=False):
    global score

    if s in string_score.keys():
        if chg:
            score = score + string_score[s]
        return string_score[s]

    score_origin = deepcopy(score)

    i = 0
    for goal in pattern1:
        num = 0
        for mod in goal:
            num += len(regex.findall(mod, s, overlapped=True))
        score += num * coefmy[i]
        i += 1
    i = 0
    for goal in pattern2:
        num = 0
        for mod in goal:
            num += len(regex.findall(mod, s, overlapped=True))
        score -= num * coefop[i]
        i += 1

    s = s[:position] + '0' + s[position + 1:]
    i = 0
    for goal in pattern1:
        num = 0
        for mod in goal:
            num += len(regex.findall(mod, s, overlapped=True))
        score -= num * coefmy[i]
        i += 1
    i = 0
    for goal in pattern2:
        num = 0
        for mod in goal:
            num += len(regex.findall(mod, s, overlapped=True))
        score += num * coefop[i]
        i += 1

    string_score[s] = score - score_origin
    s = ''.join(reversed(s))
    string_score[s] = score - score_origin

    ans = score - score_origin
    if not chg:
        score = score_origin

    return ans


def update_score(x, y, chg=True):
    k = 5  # 左右5个点
    change = 0
    # row
    row = ''
    position = 0
    for i in range(x - k, x + k + 1):
        if 0 <= i < pp.width:
            row += str(board[i][y])
            if i == x:
                position = len(row) - 1
        else:
            row += '#'
    change += update_score_string(row, position, chg)
    # col
    col = ''
    for j in range(y - k, y + k + 1):
        if 0 <= j < pp.height:
            col += str(board[x][j])
            if j == y:
                position = len(col) - 1
        else:
            col += '#'
    change += update_score_string(col, position, chg)
    # diag
    diag = ''
    for i in range(-k, k + 1):
        if 0 <= (x + i) < pp.width and 0 <= (y + i) < pp.width:
            diag += str(board[x + i][y + i])
            if i == 0:
                position = len(diag) - 1
        else:
            diag += '#'
    change += update_score_string(diag, position, chg)
    # oblique diag
    obdiag = ''
    for i in range(-k, k + 1):
        if 0 <= (x + i) < pp.width and 0 <= (y - i) < pp.width:
            obdiag += str(board[x + i][y - i])
            if i == 0:
                position = len(obdiag) - 1
        else:
            obdiag += '#'
    change += update_score_string(obdiag, position, chg)
    return change


def update_actions(bd, actions, x, y, k=1):
    if (x, y) in actions:
        actions.remove((x, y))
    for i in range(x - k, x + k + 1):
        for j in range(y - k, y + k + 1):
            if isfree(bd, i, j) and (i, j) not in actions:
                actions.append((i, j))
    return


def fast_kill_action(bd, color):
    action = search_five(bd, color)
    if action is not None:
        return action
    action = search_five(bd, 3 - color)
    if action is not None:
        return action
    action = search_four(bd, color)
    if action is not None:
        return action
    action = search_four_op(bd, 3 - color)
    if action is not None:
        return action
    action = search_double(bd, color)
    if action is not None:
        return action
    return None


def search_five(bd, color):
    boardLength = pp.width
    # column
    for x in range(boardLength - 4):
        for y in range(boardLength):
            pieces = tuple(bd[x + d][y] for d in range(5))
            if pieces.count(color) == 4 and 0 in pieces:
                d = pieces.index(0)
                return x + d, y
    # row
    for x in range(boardLength):
        for y in range(boardLength - 4):
            pieces = tuple(bd[x][y + d] for d in range(5))
            if pieces.count(color) == 4 and 0 in pieces:
                d = pieces.index(0)
                return x, y + d
    # positive diagonal
    for x in range(boardLength - 4):
        for y in range(boardLength - 4):
            pieces = tuple(bd[x + d][y + d] for d in range(5))
            if pieces.count(color) == 4 and 0 in pieces:
                d = pieces.index(0)
                return x + d, y + d
    # oblique diagonal
    for x in range(boardLength - 4):
        for y in range(4, boardLength):
            pieces = tuple(bd[x + d][y - d] for d in range(5))
            if pieces.count(color) == 4 and 0 in pieces:
                d = pieces.index(0)
                return x + d, y - d
    return None


def search_four(bd, color):
    boardLength = pp.width
    # column
    for x in range(boardLength - 5):
        for y in range(boardLength):
            pieces = tuple(bd[x + d][y] for d in range(6))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(color) == 3 and 0 in pieces[1:5]:
                d = pieces.index(0, 1, -1)
                return x + d, y
    # row
    for x in range(boardLength):
        for y in range(boardLength - 5):
            pieces = tuple(bd[x][y + d] for d in range(6))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(color) == 3 and 0 in pieces[1:5]:
                d = pieces.index(0, 1, -1)
                return x, y + d
    # positive diagonal
    for x in range(boardLength - 5):
        for y in range(boardLength - 5):
            pieces = tuple(bd[x + d][y + d] for d in range(6))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(color) == 3 and 0 in pieces[1:5]:
                d = pieces.index(0, 1, -1)
                return x + d, y + d
    # oblique diagonal
    for x in range(boardLength - 5):
        for y in range(5, boardLength):
            pieces = tuple(bd[x + d][y - d] for d in range(6))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(color) == 3 and 0 in pieces[1:5]:
                d = pieces.index(0, 1, -1)
                return x + d, y - d
    return None


def search_four_op(bd, color):
    boardLength = pp.width
    # column
    for x in range(boardLength - 5):
        for y in range(boardLength):
            pieces = tuple(bd[x + d][y] for d in range(6))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(color) == 3 and 0 in pieces[1:5]:
                d = pieces.index(0, 1, -1)
                actions = [(x, y), (x + 4, y)] if d == 4 else [(x + 1, y), (x + 5, y)] if d == 1 \
                    else [(x, y), (x + d, y), (x + 5, y)]
                max_utility = float("-inf")
                action = None
                for a in actions:
                    x, y = a
                    bd[x][y] = 3 - color
                    value = update_score(x, y, False)
                    bd[x][y] = 0
                    logDebug(str(a) + ' ' + str(value))
                    if value > max_utility:
                        action = a
                        max_utility = value
                return action
    # row
    for x in range(boardLength):
        for y in range(boardLength - 5):
            pieces = tuple(bd[x][y + d] for d in range(6))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(color) == 3 and 0 in pieces[1:5]:
                d = pieces.index(0, 1, -1)
                actions = [(x, y), (x, y + 4)] if d == 4 else [(x, y + 1), (x, y + 5)] if d == 1 \
                    else [(x, y), (x, y + d), (x, y + 5)]
                max_utility = float("-inf")
                action = None
                for a in actions:
                    x, y = a
                    bd[x][y] = 3 - color
                    value = update_score(x, y, False)
                    bd[x][y] = 0
                    ab.logDebug(str(a) + ' ' + str(value))
                    if value > max_utility:
                        action = a
                        max_utility = value
                return action
    # positive diagonal
    for x in range(boardLength - 5):
        for y in range(boardLength - 5):
            pieces = tuple(bd[x + d][y + d] for d in range(6))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(color) == 3 and 0 in pieces[1:5]:
                d = pieces.index(0, 1, -1)
                actions = [(x, y), (x + 4, y + 4)] if d == 4 else [(x + 1, y + 1), (x + 5, y + 5)] if d == 1 \
                    else [(x, y), (x + d, y + d), (x + 5, y + 5)]
                max_utility = float("-inf")
                action = None
                for a in actions:
                    x, y = a
                    bd[x][y] = 3 - color
                    value = update_score(x, y, False)
                    bd[x][y] = 0
                    logDebug(str(a) + ' ' + str(value))
                    if value > max_utility:
                        action = a
                        max_utility = value
                return action
    # oblique diagonal
    for x in range(boardLength - 5):
        for y in range(5, boardLength):
            pieces = tuple(bd[x + d][y - d] for d in range(6))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(color) == 3 and 0 in pieces[1:5]:
                d = pieces.index(0, 1, -1)
                actions = [(x, y), (x + 4, y - 4)] if d == 4 else [(x + 1, y - 1), (x + 5, y - 5)] if d == 1 \
                    else [(x, y), (x + d, y - d), (x + 5, y - 5)]
                max_utility = float("-inf")
                action = None
                for a in actions:
                    x, y = a
                    bd[x][y] = 3 - color
                    value = update_score(x, y, False)
                    bd[x][y] = 0
                    logDebug(str(a) + ' ' + str(value))
                    if value > max_utility:
                        action = a
                        max_utility = value
                return action
    return None


def search_double(bd, color):
    # 'double four', 'four-three' and 'double three'
    boardLength = pp.width

    # possible actions to achieve four
    # column
    col4_my = set()
    col4_op = set()
    for x in range(boardLength - 4):
        for y in range(boardLength):
            pieces = tuple(bd[x + d][y] for d in range(5))
            if pieces.count(0) == 2 and pieces.count(color) == 3:
                for d in range(5):
                    if pieces[d] == 0:
                        col4_my.add((x + d, y))
            if pieces.count(0) == 2 and pieces.count(3 - color) == 3:
                for d in range(5):
                    if pieces[d] == 0:
                        col4_op.add((x + d, y))
    # row
    row4_my = set()
    row4_op = set()
    for x in range(boardLength):
        for y in range(boardLength - 4):
            pieces = tuple(bd[x][y + d] for d in range(5))
            if pieces.count(0) == 2 and pieces.count(color) == 3:
                for d in range(5):
                    if pieces[d] == 0:
                        row4_my.add((x, y + d))
            if pieces.count(0) == 2 and pieces.count(3 - color) == 3:
                for d in range(5):
                    if pieces[d] == 0:
                        row4_op.add((x, y + d))
    # positive diagonal
    pos4_my = set()
    pos4_op = set()
    for x in range(boardLength - 4):
        for y in range(boardLength - 4):
            pieces = tuple(bd[x + d][y + d] for d in range(5))
            if pieces.count(0) == 2 and pieces.count(color) == 3:
                for d in range(5):
                    if pieces[d] == 0:
                        pos4_my.add((x + d, y + d))
            if pieces.count(0) == 2 and pieces.count(3 - color) == 3:
                for d in range(5):
                    if pieces[d] == 0:
                        pos4_op.add((x + d, y + d))
    # oblique diagonal
    ob4_my = set()
    ob4_op = set()
    for x in range(boardLength - 4):
        for y in range(4, boardLength):
            pieces = tuple(bd[x + d][y - d] for d in range(5))
            if pieces.count(0) == 2 and pieces.count(color) == 3:
                for d in range(5):
                    if pieces[d] == 0:
                        ob4_my.add((x + d, y - d))
            if pieces.count(0) == 2 and pieces.count(3 - color) == 3:
                for d in range(5):
                    if pieces[d] == 0:
                        ob4_op.add((x + d, y - d))

    # possible actions to achieve three
    # column
    col3_my = set()
    col3_op = set()
    for x in range(boardLength - 5):
        for y in range(boardLength):
            pieces = tuple(bd[x + d][y] for d in range(6))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(color) == 2 and pieces[1:5].count(0) == 2:
                for d in range(1, 5):
                    if pieces[d] == 0:
                        col3_my.add((x + d, y))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(3 - color) == 2 and pieces[1:5].count(0) == 2:
                for d in range(1, 5):
                    if pieces[d] == 0:
                        col3_op.add((x + d, y))
    # row
    row3_my = set()
    row3_op = set()
    for x in range(boardLength):
        for y in range(boardLength - 5):
            pieces = tuple(bd[x][y + d] for d in range(6))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(color) == 2 and pieces[1:5].count(0) == 2:
                for d in range(1, 5):
                    if pieces[d] == 0:
                        row3_my.add((x, y + d))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(3 - color) == 2 and pieces[1:5].count(0) == 2:
                for d in range(1, 5):
                    if pieces[d] == 0:
                        row3_op.add((x, y + d))
    # positive diagonal
    pos3_my = set()
    pos3_op = set()
    for x in range(boardLength - 5):
        for y in range(boardLength - 5):
            pieces = tuple(bd[x + d][y + d] for d in range(6))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(color) == 2 and pieces[1:5].count(0) == 2:
                for d in range(1, 5):
                    if pieces[d] == 0:
                        pos3_my.add((x + d, y + d))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(3 - color) == 2 and pieces[1:5].count(0) == 2:
                for d in range(1, 5):
                    if pieces[d] == 0:
                        pos3_op.add((x + d, y + d))
    # oblique diagonal
    ob3_my = set()
    ob3_op = set()
    for x in range(boardLength - 5):
        for y in range(5, boardLength):
            pieces = tuple(bd[x + d][y - d] for d in range(6))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(color) == 2 and pieces[1:5].count(0) == 2:
                for d in range(1, 5):
                    if pieces[d] == 0:
                        ob3_my.add((x + d, y - d))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(3 - color) == 2 and pieces[1:5].count(0) == 2:
                for d in range(1, 5):
                    if pieces[d] == 0:
                        ob3_op.add((x + d, y - d))

    sets_my = [col4_my, row4_my, pos4_my, ob4_my, col3_my, row3_my, pos3_my, ob3_my]
    sets_op = [col4_op, row4_op, pos4_op, ob4_op, col3_op, row3_op, pos3_op, ob3_op]
    # my double four and three-four
    for i in range(4):
        for j in range(i + 1, 4):
            intersect = sets_my[i] & sets_my[j]
            if len(intersect) != 0:
                return list(intersect)[0]
    for i in range(4):
        for j in range(4, 8):
            if j != i + 4:
                intersect = sets_my[i] & sets_my[j]
                if len(intersect) != 0:
                    return list(intersect)[0]
    # op double four and three-four
    for i in range(4):
        for j in range(i + 1, 4):
            intersect = sets_op[i] & sets_op[j]
            if len(intersect) != 0:
                return list(intersect)[0]
    for i in range(4):
        for j in range(4, 8):
            if j != i + 4:
                intersect = sets_op[i] & sets_op[j]
                if len(intersect) != 0:
                    return list(intersect)[0]
    # my double three
    for i in range(4, 8):
        for j in range(i + 1, 8):
            intersect = sets_my[i] & sets_my[j]
            if len(intersect) != 0:
                return list(intersect)[0]
    # op double three
    for i in range(4, 8):
        for j in range(i + 1, 8):
            intersect = sets_op[i] & sets_op[j]
            if len(intersect) != 0:
                return list(intersect)[0]
######################################################################
# A possible way how to debug brains.
# To test it, just "uncomment" it (delete enclosing """)
######################################################################

# define a file for logging ...
DEBUG_LOGFILE = "D:/360Files/My Learning/2021-2022 5/5人工智能/Final Project/MC-tree-search/log.log"
# ...and clear it initially
with open(DEBUG_LOGFILE, "w") as f:
    pass


# define a function for writing messages to the file
def logDebug(msg):
    with open(DEBUG_LOGFILE, "a") as f:
        f.write(msg + "\n")
        f.flush()


# define a function to get exception traceback
def logTraceBack():
    import traceback
    with open(DEBUG_LOGFILE, "a") as f:
        traceback.print_exc(file=f)
        f.flush()
    raise


'''
# use logDebug wherever
# use try-except (with logTraceBack in except branch) to get exception info
# an example of problematic function
def brain_turn():
    logDebug("some message 1")
    try:
        logDebug("some message 2")
        1. / 0.  # some code raising an exception
        logDebug("some message 3")  # not logged, as it is after error
    except:
        logTraceBack()
'''

######################################################################

# "overwrites" functions in pisqpipe module
pp.brain_init = brain_init
pp.brain_restart = brain_restart
pp.brain_my = brain_my
pp.brain_opponents = brain_opponents
pp.brain_block = brain_block
pp.brain_takeback = brain_takeback
pp.brain_turn = brain_turn
pp.brain_end = brain_end
pp.brain_about = brain_about
if DEBUG_EVAL:
    pp.brain_eval = brain_eval


def main():
    pp.main()


if __name__ == "__main__":
    main()
