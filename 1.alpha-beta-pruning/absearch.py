import pisqpipe as pp
from pisqpipe import DEBUG_EVAL, DEBUG
import regex
import time
from fast_actions import *

pp.infotext = 'name="a-b-search", author="", version="1.0", country="China", www=""'

MAX_BOARD = 100
MAX_DEPTH = 2
board = [[0 for i in range(MAX_BOARD)] for j in range(MAX_BOARD)]
actions = []
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


def brain_init():
    if pp.width < 5 or pp.height < 5:
        pp.pipeOut("ERROR size of the board")
        return
    if pp.width > MAX_BOARD or pp.height > MAX_BOARD:
        pp.pipeOut("ERROR Maximal board size is {}".format(MAX_BOARD))
        return
    pp.pipeOut("OK")


def brain_restart():
    global board
    for x in range(pp.width):
        for y in range(pp.height):
            board[x][y] = 0
    global actions, last_point
    actions = []
    last_point = None
    global score
    score = 0
    pp.pipeOut("OK")


def isFree(x, y):
    return x >= 0 and y >= 0 and x < pp.width and y < pp.height and board[x][y] == 0


def brain_my(x, y):
    if isFree(x, y):
        board[x][y] = 1
        update_actions(x, y)
        update_score(x, y)
    else:
        pp.pipeOut("ERROR my move [{},{}]".format(x, y))


def brain_opponents(x, y):
    if isFree(x, y):
        board[x][y] = 2
        global last_point
        update_actions(x, y)
        last_point = (x, y)
        update_score(x, y)
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
        logDebug('我的回合')
        if not last_point:
            action = (int(pp.width / 2), int(pp.height / 2))
            x, y = action
            pp.do_mymove(x, y)
            return

        action = fast_kill_action(board)
        if not action:
            action, v = alpha_beta_search(1)
        x, y = action
        pp.do_mymove(x, y)
    except:
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


def update_score_string(s, position, chg=True):
    global score

    if s in string_score.keys():
        if chg:
            score = score + string_score[s]
        return string_score[s]

    score_origin = score

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

    s = s[:position] + '0' + s[position+1:]
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


def utility():
    return score


def terminal_test(depth):
    if depth > MAX_DEPTH or abs(score) > 5e10:
        return True
    return False


def update_actions(x, y, k=1):
    global actions
    add_action = []
    del_action = []
    if (x, y) in actions:
        actions.remove((x, y))
        del_action.append((x, y))
    for i in range(x - k, x + k + 1):
        for j in range(y - k, y + k + 1):
            if isFree(i, j) and (i, j) not in actions:
                actions.append((i, j))
                add_action.append((i, j))
    return add_action, del_action


def restore_actions(add_action, del_action):
    global actions
    j = 0
    for i in range(len(actions)):
        if actions[j] in add_action:
            actions.pop(j)
        else:
            j += 1
    for i in del_action:
        actions.append(i)
    return


def restore_score(chg):
    global score
    score = score - chg
    return


def sort_key(x):
    return update_score(x[0], x[1], chg=False)


def max_value(alpha, beta, depth):
    if terminal_test(depth):
        # logDebug('terminal max ' + str(depth))
        if time.time() - tick > min(pp.info_time_left, pp.info_timeout_turn)/1000 - 0.5:
            return float('-inf'), None
        v = utility()
        return v, None

    v = float("-inf")
    act = None
    if len(actions) != 0:
        action_list = actions.copy()
        action_list.sort(key=sort_key, reverse=True)
        for a in action_list:
            board[a[0]][a[1]] = 1
            add_action, del_action = update_actions(a[0], a[1])
            chg = update_score(a[0], a[1])
            logDebug('max_move:' + str(a))
            move_v, move_action = min_value(alpha, beta, depth + 1)
            logDebug('min_final_move:' + str(move_action) + ' value:' + str(move_v))
            board[a[0]][a[1]] = 0
            restore_actions(add_action, del_action)
            restore_score(chg)

            if not act:
                act = a
            if move_v > v:
                v = move_v
                act = a
            if v >= beta:
                return v, act
            alpha = max(alpha, v)
            if time.time() - tick > min(pp.info_time_left, pp.info_timeout_turn)/1000 - 0.5:
                return v, act
    else:
        v = utility()
        act = None
    return v, act


def min_value(alpha, beta, depth):
    logDebug('min_act_list' + str(actions))
    if terminal_test(depth):
        # logDebug('terminal min ' + str(depth))
        if time.time() - tick > min(pp.info_time_left, pp.info_timeout_turn)/1000 - 0.5:
            return float('inf'), None
        v = utility()
        return v, None

    v = float("inf")
    act = None
    if len(actions) != 0:
        action_list = actions.copy()
        action_list.sort(key=sort_key)
        for a in action_list:
            board[a[0]][a[1]] = 2
            add_action, del_action = update_actions(a[0], a[1])
            chg = update_score(a[0], a[1])
            move_v, move_action = max_value(alpha, beta, depth + 1)
            logDebug('min_move:' + str(a) + ' value:' + str(move_v))
            restore_actions(add_action, del_action)
            restore_score(chg)
            board[a[0]][a[1]] = 0

            if not act:
                act = a
            if move_v < v:
                v = move_v
                act = a
            if v <= alpha:
                return v, act
            beta = min(beta, v)
            if time.time() - tick > min(pp.info_time_left, pp.info_timeout_turn)/1000 - 0.5:
                return v, act
    else:
        v = utility()
        act = None
    return v, act


def alpha_beta_search(color):
    depth = 0
    v, action = max_value(float("-inf"), float("inf"), depth + 1)
    return action, v


######################################################################
# A possible way how to debug brains.
# To test it, just "uncomment" it (delete enclosing """)
######################################################################

# define a file for logging ...
DEBUG_LOGFILE = "D:/Desktop/课程及其他/人工智能/final-pj/Final Project/GOMOKU-for-AI-project/1.alpha-beta-pruning/log.log"
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
