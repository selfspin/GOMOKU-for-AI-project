import copy
import pisqpipe as pp
from pisqpipe import DEBUG_EVAL, DEBUG
import regex
import time
from fast_actions import *

pp.infotext = 'name="a-b-search", author="", version="1.0", country="China", www=""'

MAX_BOARD = 100
board = [[0 for i in range(MAX_BOARD)] for j in range(MAX_BOARD)]
actions_adj = []
features_my = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
features_op = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
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
laststate = []
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
tick = time.time()

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
    global actions_adj, features_my, features_op, last_point
    actions_adj = []
    features_my = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    features_op = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    last_point = None
    pp.pipeOut("OK")


def isFree(x, y):
    return x >= 0 and y >= 0 and x < pp.width and y < pp.height and board[x][y] == 0


def brain_my(x, y):
    if isFree(x, y):
        board[x][y] = 1
        global actions_adj, features_my, features_op, last_point
        actions_adj = update_actions(board, actions_adj, x, y)
        features_my, features_op = update_features(board, x, y, features_my, features_op)
    else:
        pp.pipeOut("ERROR my move [{},{}]".format(x, y))


def brain_opponents(x, y):
    if isFree(x, y):
        board[x][y] = 2
        global actions_adj, features_my, features_op, last_point
        actions_adj = update_actions(board, actions_adj, x, y)
        features_my, features_op = update_features(board, x, y, features_my, features_op)
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

'''
def order_actions_adj():
    global actions_adj
    dict_list = []
    for action in actions_adj:
        fea_my, fea_op = update_features(board, action[0], action[1], features_my, features_op)
        v = utility(fea_my, fea_op)
        dict_list.append({'action': action, 'value': v})
    dict_list.sort(key=lambda x: x["value"], reverse=True)
    actions_adj = [x['action'] for x in dict_list]
    return
'''


def brain_turn():
    try:
        global tick
        tick = time.time()
        if pp.terminateAI:
            return
        # logDebug('我的回合')
        # at beginning, no stones
        if not last_point:
            action = (int(pp.width / 2), int(pp.height / 2))
            x, y = action
            pp.do_mymove(x, y)
            return

        action = fast_kill_action(board)
        # logDebug('fast_kill:' + str(action))
        if not action:
            action, v = alpha_beta_search(board, 1)
        x, y = action
        pp.do_mymove(x, y)
    except:
        pass
        # logTraceBack()


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


def update_features_string(s, position, fea_my, fea_op):
    i = 0
    for goal in pattern1:
        num = 0
        for mod in goal:
            num += len(regex.findall(mod, s, overlapped=True))
        fea_my[i] += num
        i += 1
    i = 0
    for goal in pattern2:
        num = 0
        for mod in goal:
            num += len(regex.findall(mod, s, overlapped=True))
        fea_op[i] += num
        i += 1

    s = s[:position] + '0' + s[position+1:]
    i = 0
    for goal in pattern1:
        num = 0
        for mod in goal:
            num += len(regex.findall(mod, s, overlapped=True))
        fea_my[i] -= num
        i += 1
    i = 0
    for goal in pattern2:
        num = 0
        for mod in goal:
            num += len(regex.findall(mod, s, overlapped=True))
        fea_op[i] -= num
        i += 1
    return


def update_features(board, x, y, old_fea_my, old_fea_op):
    k = 5  # 左右四个点
    fea_my = copy.deepcopy(old_fea_my)
    fea_op = copy.deepcopy(old_fea_op)
    # row
    row = ''
    position = 0
    for i in range(x - k, x + k + 1):
        if 0 <= i < pp.width:
            row += str(board[i][y])
            if i == x:
                position = len(row) - 1
    update_features_string(row, position, fea_my, fea_op)
    # col
    col = ''
    for j in range(y - k, y + k + 1):
        if 0 <= j < pp.height:
            col += str(board[x][j])
            if j == y:
                position = len(col) - 1
    update_features_string(col, position, fea_my, fea_op)
    # diag
    diag = ''
    for i in range(-k, k + 1):
        if 0 <= (x + i) < pp.width and 0 <= (y + i) < pp.width:
            diag += str(board[x + i][y + i])
            if i == 0:
                position = len(diag) - 1
    update_features_string(diag, position, fea_my, fea_op)
    # oblique diag
    obdiag = ''
    for i in range(-k, k + 1):
        if 0 <= (x + i) < pp.width and 0 <= (y - i) < pp.width:
            obdiag += str(board[x + i][y - i])
            if i == 0:
                position = len(obdiag) - 1
    update_features_string(obdiag, position, fea_my, fea_op)
    return fea_my, fea_op


def utility(fea_my, fea_op):
    value = 0
    # weight
    coefmy = [1e10, 1e8, 1e8, 0, 1e6, 7e1, 0, 7e1, 5, 0]
    coefop = [1e10, 5e7, 1e4, 0, 1e4, 5e1, 0, 7e1, 5, 0]
    l = len(coefmy)
    for i in range(l):
        value = value + coefmy[i] * fea_my[i] - coefop[i] * fea_op[i]
    return value


def terminal_test(depth, fea_my, fea_op):
    if depth > 1 | fea_my[0] | fea_op[0]:
        return True
    return False


def update_actions(board, old_actions, x, y, k = 1):
    actions = copy.deepcopy(old_actions)
    if (x, y) in actions:
        actions.remove((x, y))
    for i in range(x - k, x + k + 1):
        for j in range(y - k, y + k + 1):
            if i >= 0 and j >= 0 and i < pp.width and j < pp.height and board[i][j] == 0 and (i, j) not in actions:
                actions.append((i, j))
    return actions

'''
def sort_key(x, ref):
    if x[0] == ref[0] or x[1] == ref[1] or abs(x[0]-ref[0]) == abs(x[1]-ref[1]):
        return 0
    else:
        return min(abs(x[0]-ref[0]), abs(x[1]-ref[1]))
'''

def max_value(board, color, alpha, beta, depth, action_list, fea_my, fea_op, last_po):
    if terminal_test(depth, fea_my, fea_op):
        # logDebug('terminal max ' + str(depth))
        if time.time() - tick > min(pp.info_time_left, pp.info_timeout_turn)/1000 - 0.5:
            return float('-inf'), None
        v = utility(fea_my, fea_op)
        return v, None

    v = float("-inf")
    action = None
    if len(action_list) != 0:
        action_list.sort(key=lambda x: abs(x[0]-last_po[0])+abs(x[1]-last_po[1]))
        # action_list.sort(key=lambda x: sort_key(x, last_po))
        for a in action_list:
            board_new = copy.deepcopy(board)
            board_new[a[0]][a[1]] = 1
            nxt_last_po = tuple(a)
            action_list_new = update_actions(board_new, action_list, a[0], a[1])
            # logDebug('action_list_new' + str(action_list_new))
            fea_my_new, fea_op_new = update_features(board_new, a[0], a[1], fea_my, fea_op)
            # logDebug('max_move:' + str(a))
            move_v, move_action = min_value(board_new, color, alpha, beta, depth + 1,
                                            action_list_new, fea_my_new, fea_op_new, nxt_last_po)
            # logDebug('min_final_move:' + str(move_action) + ' value:' + str(move_v))
            if not action:
                action = a
            if move_v > v:
                v = move_v
                action = a
            if v >= beta:
                # logDebug('prune return' + str(v) + str(action))
                return v, action
            alpha = max(alpha, v)
            if time.time() - tick > min(pp.info_time_left, pp.info_timeout_turn)/1000 - 0.5:
                return v, action
    else:
        v = utility(fea_my, fea_op)
        action = None
    return v, action


def min_value(board, color, alpha, beta, depth, action_list, fea_my, fea_op, last_po):
    # logDebug('min_act_list' + str(action_list))
    if terminal_test(depth, fea_my, fea_op):
        # logDebug('terminal min ' + str(depth))
        if time.time() - tick > min(pp.info_time_left, pp.info_timeout_turn)/1000 - 0.5:
            return float('inf'), None
        v = utility(fea_my, fea_op)
        return v, None

    v = float("inf")
    action = None
    if len(action_list) != 0:
        # 负优化: 改一下排序函数，先优先同一行、列、斜上的元素
        action_list.sort(key=lambda x: abs(x[0] - last_po[0]) + abs(x[1] - last_po[1]))
        # action_list.sort(key=lambda x: sort_key(x, last_po))
        for a in action_list:
            board_new = copy.deepcopy(board)
            board_new[a[0]][a[1]] = 2
            nxt_last_po = tuple(a)
            action_list_new = update_actions(board_new, action_list, a[0], a[1])
            # logDebug('action_list_new ' + str(action_list_new))
            fea_my_new, fea_op_new = update_features(board_new, a[0], a[1], fea_my, fea_op)
            move_v, move_action = max_value(board_new, color, alpha, beta, depth + 1,
                                            action_list_new, fea_my_new, fea_op_new, nxt_last_po)
            # logDebug('min_move:' + str(a) + ' value:' + str(move_v))
            if not action:
                action = a
            if move_v < v:
                v = move_v
                action = a
            if v <= alpha:
                # logDebug('prune return' + str(v) + str(action))
                return v, action
            beta = min(beta, v)
            if time.time() - tick > min(pp.info_time_left, pp.info_timeout_turn)/1000 - 0.5:
                return v, action
    else:
        v = utility(fea_my, fea_op)
        action = None
    # logDebug('return' + str(v) + str(action))
    return v, action


def alpha_beta_search(board, color):
    depth = 0
    v, action = max_value(board, color, float("-inf"), float("inf"), depth,
                          actions_adj, features_my, features_op, last_point)
    return action, v


######################################################################
# A possible way how to debug brains.
# To test it, just "uncomment" it (delete enclosing """)
######################################################################
"""
# define a file for logging ...
DEBUG_LOGFILE = "D:/Desktop/课程及其他/人工智能/final-pj/Final Project/pbrain-pyrandom-master/log.log"
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
        traceback.print_exc(file = f)
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
"""
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
