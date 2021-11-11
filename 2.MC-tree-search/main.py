import copy
import pisqpipe as pp
from pisqpipe import DEBUG_EVAL, DEBUG
import time
from MCTS import *
from fast_actions import *

pp.infotext = 'name="MCTS", author="", version="1.0", country="China", www=""'

MAX_BOARD = 100
board = [[0 for i in range(MAX_BOARD)] for j in range(MAX_BOARD)]
actions_adj = []
last_point = None
features_my = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
features_op = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


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


def brain_turn():
    try:
        logDebug('actions_adj:  ' + str(actions_adj))
        if pp.terminateAI:
            return
        # at beginning, no stones
        if not last_point:
            action = (int(pp.width / 2), int(pp.height / 2))
            x, y = action
            pp.do_mymove(x, y)
            return

        fea_my = copy.deepcopy(features_my)
        fea_op = copy.deepcopy(features_op)
        action = fast_kill_action(board, 1)
        logDebug('fast_kill:' + str(action))
        if not action:
            board_copy = copy.deepcopy(board)
            actions = copy.deepcopy(actions_adj)
            mcts_player = MCTS(board_copy, 1, actions, fea_my, fea_op)
            action = mcts_player.get_action()
        x, y = action
        pp.do_mymove(x, y)
    except:
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





######################################################################
# A possible way how to debug brains.
# To test it, just "uncomment" it (delete enclosing """)
######################################################################

# define a file for logging ...
DEBUG_LOGFILE = "D:/360Files/My Learning/2021-2022 5/5人工智能/Final Project/pbrain-pyrandom-master/AI-MCTS/MCTS.log"
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
