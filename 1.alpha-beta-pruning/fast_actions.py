import pisqpipe as pp
import absearch as ab
import copy


def fast_kill_action(board):
    action = search_five(board, 1)
    if action is not None:
        return action
    action = search_five(board, 2)
    if action is not None:
        return action
    action = search_four(board, 1)
    if action is not None:
        return action
    action = search_four_op(board, 2)
    if action is not None:
       return action
    action = search_double(board, 1)
    if action is not None:
        return action
    action = search_double(board, 2)
    if action is not None:
        return action
    return None


def search_five(board, color):
    boardLength = pp.width
    # column
    for x in range(boardLength-4):
        for y in range(boardLength):
            pieces = tuple(board[x+d][y] for d in range(5))
            if pieces.count(color) == 4 and 0 in pieces:
                d = pieces.index(0)
                return x + d, y
    # row
    for x in range(boardLength):
        for y in range(boardLength-4):
            pieces = tuple(board[x][y+d] for d in range(5))
            if pieces.count(color) == 4 and 0 in pieces:
                d = pieces.index(0)
                return x, y + d
    # positive diagonal
    for x in range(boardLength-4):
        for y in range(boardLength-4):
            pieces = tuple(board[x+d][y+d] for d in range(5))
            if pieces.count(color) == 4 and 0 in pieces:
                d = pieces.index(0)
                return x + d, y + d
    # oblique diagonal
    for x in range(boardLength-4):
        for y in range(4, boardLength):
            pieces = tuple(board[x+d][y-d] for d in range(5))
            if pieces.count(color) == 4 and 0 in pieces:
                d = pieces.index(0)
                return x + d, y - d
    return None


def search_four(board, color):
    boardLength = pp.width
    # column
    for x in range(boardLength-5):
        for y in range(boardLength):
            pieces = tuple(board[x+d][y] for d in range(6))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(color) == 3 and 0 in pieces[1:5]:
                d = pieces.index(0, 1, -1)
                return x + d, y
    # row
    for x in range(boardLength):
        for y in range(boardLength-5):
            pieces = tuple(board[x][y+d] for d in range(6))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(color) == 3 and 0 in pieces[1:5]:
                d = pieces.index(0, 1, -1)
                return x, y + d
    # positive diagonal
    for x in range(boardLength-5):
        for y in range(boardLength-5):
            pieces = tuple(board[x+d][y+d] for d in range(6))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(color) == 3 and 0 in pieces[1:5]:
                d = pieces.index(0, 1, -1)
                return x + d, y + d
    # oblique diagonal
    for x in range(boardLength-5):
        for y in range(5, boardLength):
            pieces = tuple(board[x+d][y-d] for d in range(6))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(color) == 3 and 0 in pieces[1:5]:
                d = pieces.index(0, 1, -1)
                return x + d, y - d
    return None


def search_four_op(board, color):
    boardLength = pp.width
    # column
    for x in range(boardLength-5):
        for y in range(boardLength):
            pieces = tuple(board[x+d][y] for d in range(6))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(color) == 3 and 0 in pieces[1:5]:
                d = pieces.index(0, 1, -1)
                actions = [(x, y), (x + 4, y)] if d == 4 else [(x + 1, y), (x + 5, y)] if d == 1 \
                           else [(x, y), (x + d, y), (x + 5, y)]
                max_utility = float("-inf")
                action = None
                for a in actions:
                    x, y = a
                    board_new = copy.deepcopy(board)
                    board_new[x][y] = 3 - color
                    fea = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                    fea_my_new, fea_op_new = ab.update_features(board_new, x, y, fea, fea)
                    value = ab.utility(fea_my_new, fea_op_new)
                    if value > max_utility:
                        action = a
                        max_utility = value
                return action
    # row
    for x in range(boardLength):
        for y in range(boardLength-5):
            pieces = tuple(board[x][y+d] for d in range(6))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(color) == 3 and 0 in pieces[1:5]:
                d = pieces.index(0, 1, -1)
                actions = [(x, y), (x, y + 4)] if d == 4 else [(x, y + 1), (x, y + 5)] if d == 1 \
                    else [(x, y), (x, y + d), (x, y + 5)]
                max_utility = float("-inf")
                action = None
                for a in actions:
                    x, y = a
                    board_new = copy.deepcopy(board)
                    board_new[x][y] = 3 - color
                    fea = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                    fea_my_new, fea_op_new = ab.update_features(board_new, x, y, fea, fea)
                    value = ab.utility(fea_my_new, fea_op_new)
                    if value > max_utility:
                        action = a
                        max_utility = value
                return action
    # positive diagonal
    for x in range(boardLength-5):
        for y in range(boardLength-5):
            pieces = tuple(board[x+d][y+d] for d in range(6))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(color) == 3 and 0 in pieces[1:5]:
                d = pieces.index(0, 1, -1)
                actions = [(x, y), (x + 4, y + 4)] if d == 4 else [(x + 1, y + 1), (x + 5, y + 5)] if d == 1 \
                    else [(x, y), (x + d, y + d), (x + 5, y + 5)]
                max_utility = float("-inf")
                action = None
                for a in actions:
                    x, y = a
                    board_new = copy.deepcopy(board)
                    board_new[x][y] = 3 - color
                    fea = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                    fea_my_new, fea_op_new = ab.update_features(board_new, x, y, fea, fea)
                    value = ab.utility(fea_my_new, fea_op_new)
                    if value > max_utility:
                        action = a
                        max_utility = value
                return action
    # oblique diagonal
    for x in range(boardLength-5):
        for y in range(5, boardLength):
            pieces = tuple(board[x+d][y-d] for d in range(6))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(color) == 3 and 0 in pieces[1:5]:
                d = pieces.index(0, 1, -1)
                actions = [(x, y), (x + 4, y - 4)] if d == 4 else [(x + 1, y - 1), (x + 5, y - 5)] if d == 1 \
                    else [(x, y), (x + d, y - d), (x + 5, y - 5)]
                max_utility = float("-inf")
                action = None
                for a in actions:
                    x, y = a
                    board_new = copy.deepcopy(board)
                    board_new[x][y] = 3 - color
                    fea = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                    fea_my_new, fea_op_new = ab.update_features(board_new, x, y, fea, fea)
                    value = ab.utility(fea_my_new, fea_op_new)
                    if value > max_utility:
                        action = a
                        max_utility = value
                return action
    return None


def search_double(board, color):
    # 'double four', 'one four one three' and 'double three'
    boardLength = pp.width
    # possible placement to achieve four
    # column
    col4 = set()
    for x in range(boardLength - 4):
        for y in range(boardLength):
            pieces = tuple(board[x + d][y] for d in range(5))
            if pieces.count(0) == 2 and pieces.count(color) == 3:
                for d in range(5):
                    if pieces[d] == 0:
                        col4.add((x + d, y))
    # row
    row4 = set()
    for x in range(boardLength):
        for y in range(boardLength - 4):
            pieces = tuple(board[x][y + d] for d in range(5))
            if pieces.count(0) == 2 and pieces.count(color) == 3:
                for d in range(5):
                    if pieces[d] == 0:
                        row4.add((x, y + d))
    # positive diagonal
    pos4 = set()
    for x in range(boardLength - 4):
        for y in range(boardLength - 4):
            pieces = tuple(board[x + d][y + d] for d in range(5))
            if pieces.count(0) == 2 and pieces.count(color) == 3:
                for d in range(5):
                    if pieces[d] == 0:
                        pos4.add((x + d, y + d))
    # oblique diagonal
    ob4 = set()
    for x in range(boardLength - 4):
        for y in range(4, boardLength):
            pieces = tuple(board[x + d][y - d] for d in range(5))
            if pieces.count(0) == 2 and pieces.count(color) == 3:
                for d in range(5):
                    if pieces[d] == 0:
                        ob4.add((x + d, y - d))

    # possible placement to achieve three
    # column
    col3 = set()
    for x in range(boardLength - 5):
        for y in range(boardLength):
            pieces = tuple(board[x + d][y] for d in range(6))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(color) == 2 and pieces[1:5].count(0) == 2:
                for d in range(1, 5):
                    if pieces[d] == 0:
                        col3.add((x + d, y))
    # row
    row3 = set()
    for x in range(boardLength):
        for y in range(boardLength - 5):
            pieces = tuple(board[x][y + d] for d in range(6))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(color) == 2 and pieces[1:5].count(0) == 2:
                for d in range(1, 5):
                    if pieces[d] == 0:
                        row3.add((x, y + d))
    # positive diagonal
    pos3 = set()
    for x in range(boardLength - 5):
        for y in range(boardLength - 5):
            pieces = tuple(board[x + d][y + d] for d in range(6))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(color) == 2 and pieces[1:5].count(0) == 2:
                for d in range(1, 5):
                    if pieces[d] == 0:
                        pos3.add((x + d, y + d))
    # oblique diagonal
    ob3 = set()
    for x in range(boardLength - 5):
        for y in range(5, boardLength):
            pieces = tuple(board[x + d][y - d] for d in range(6))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(color) == 2 and pieces[1:5].count(0) == 2:
                for d in range(1, 5):
                    if pieces[d] == 0:
                        ob3.add((x + d, y - d))

    sets = [col4, row4, pos4, ob4, col3, row3, pos3, ob3]
    for i in range(8):
        for j in range(i+1, 8):
            if j != i+4:
                intersect = sets[i] & sets[j]
                if len(intersect) != 0:
                    return list(intersect)[0]
