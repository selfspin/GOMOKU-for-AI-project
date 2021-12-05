import pisqpipe as pp
from pisqpipe import DEBUG_EVAL, DEBUG
from fast_actions import *
from board import *
from TSS import *
import nn
import numpy as np

pp.infotext = 'name="RL", author="", version="1.0", country="China", www=""'

MAX_BOARD = 100
board = [[0 for i in range(MAX_BOARD)] for j in range(MAX_BOARD)]
last_point = None
k = 0  # num of steps


def replay():
    feature_file = "D:/360Files/My Learning/2021-2022 5/5人工智能/Final Project/pbrain/RL/replay_feature_yx.npy"
    target_file = "D:/360Files/My Learning/2021-2022 5/5人工智能/Final Project/pbrain/RL/replay_target_yx.npy"
    winner = my_board.is_win()
    feature = my_board.extract_feature()
    replay_f = np.load(feature_file)
    replay_f = np.concatenate((replay_f, feature), axis=1)
    np.save(feature_file, replay_f)
    if winner == 1:
        replay_y = np.load(target_file)
        replay_y = np.concatenate((replay_y, np.ones((1, k))), axis=1)
        np.save(target_file, replay_y)
    elif winner == 2:
        replay_y = np.load(target_file)
        replay_y = np.concatenate((replay_y, np.zeros((1, k))), axis=1)
        np.save(target_file, replay_y)
    return


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
    global last_point, my_board, k
    last_point = None
    replay()
    my_board = Board(np.zeros((20, 20)), network=network, explore_prob=0)
    k = 0
    pp.pipeOut("OK")


def isFree(x, y):
    return x >= 0 and y >= 0 and x < pp.width and y < pp.height and board[x][y] == 0


def brain_my(x, y):
    if isFree(x, y):
        global k
        k += 1
        board[x][y] = 1
        my_board.update_board(x, y)
        replay()

        a = search_five(my_board, my_board.turn)
        if a is not None:
            k += 1
            my_board.update_board(a[0], a[1])
            replay()
    else:
        pp.pipeOut("ERROR my move [{},{}]".format(x, y))


def brain_opponents(x, y):
    if isFree(x, y):
        global last_point, k
        last_point = (x, y)
        k += 1
        board[x][y] = 2
        my_board.update_board(x, y)
        replay()
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
        if pp.terminateAI:
            return
        # at beginning, no stones
        if not last_point:
            x, y = (int(pp.width / 2), int(pp.height / 2))
            my_board.update_board(x, y)
            pp.do_mymove(x, y)
            return

        B = TSS(my_board)
        action = B.solve()
        logDebug('this is TSS:' + str(action))
        if not action:
            logDebug('this is fast action' + str(action))
            action = fast_kill_action(my_board)
        if not action:
            action = my_board.minimax()
            logDebug('this is foolish network' + str(action))
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
DEBUG_LOGFILE = "D:/360Files/My Learning/2021-2022 5/5人工智能/Final Project/pbrain/RL/RL.log"
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


try:
    par = np.load('D:/360Files/My Learning/2021-2022 5/5人工智能/Final Project/pbrain/RL/para_replay_yx.npy',
                  allow_pickle=True)
    par = par.reshape(1)[0]
    network = nn.NN(params=par)
    my_board = Board(np.zeros((20, 20)), network=network, explore_prob=0)
except:
    logTraceBack()
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
