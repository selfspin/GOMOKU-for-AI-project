import pisqpipe as pp
from pisqpipe import DEBUG_EVAL, DEBUG
import time
import traceback
from MCTS import *
from fast_actions import *

pp.infotext = 'name="a-b-search", author="", version="1.0", country="China", www=""'

MAX_BOARD = 100
MAX_DEPTH = 10
board = [[0 for i in range(MAX_BOARD)] for j in range(MAX_BOARD)]
last_point = None
string_score = {}
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
    global board
    for x in range(pp.width):
        for y in range(pp.height):
            board[x][y] = 0
    global node, last_point
    node = None
    last_point = None
    pp.pipeOut("OK")


def isFree(bd, x, y):
    return x >= 0 and y >= 0 and x < pp.width and y < pp.height and bd[x][y] == 0


def brain_my(x, y):
    global board
    if isFree(board, x, y):
        global node
        if last_point is None:
            node = Node(board, (x, y), [], 1)
        else:
            node = node.towards((x, y))
        board[x][y] = 1
    else:
        pp.pipeOut("ERROR my move [{},{}]".format(x, y))


def brain_opponents(x, y):
    global board
    if isFree(board, x, y):
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
    if isFree(board, x, y):
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


def update_actions(bd, actions, x, y, k=1):
    if (x, y) in actions:
        actions.remove((x, y))
    for i in range(x - k, x + k + 1):
        for j in range(y - k, y + k + 1):
            if isFree(bd, i, j) and (i, j) not in actions:
                actions.append((i, j))
    return


######################################################################
# A possible way how to debug brains.
# To test it, just "uncomment" it (delete enclosing """)
######################################################################

# define a file for logging ...
DEBUG_LOGFILE = "D:/Desktop/课程及其他/人工智能/final-pj/Final Project/GOMOKU-for-AI-project/2.MC-tree-search/log.log"
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
