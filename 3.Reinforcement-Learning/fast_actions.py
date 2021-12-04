import pisqpipe as pp


def fast_kill_action(Board):
    color = Board.turn
    action = search_five(Board, color)
    if action is not None:
        return action
    action = search_five(Board, 3 - color)
    if action is not None:
        return action
    action = search_four(Board, color)
    if action is not None:
        return action
    action = search_four_op(Board, 3 - color)
    if action is not None:
       return action
    action = search_double(Board, color)
    if action is not None:
        return action
    return None


def search_five(Board, color):
    boardLength = pp.width
    board = Board.board
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


def search_four(Board, color):
    boardLength = pp.width
    board = Board.board
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


def search_four_op(Board, color):
    boardLength = pp.width
    board = Board.board
    # column
    for x in range(boardLength-5):
        for y in range(boardLength):
            pieces = tuple(board[x+d][y] for d in range(6))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(color) == 3 and 0 in pieces[1:5]:
                d = pieces.index(0, 1, -1)
                actions = [(x, y), (x + 4, y)] if d == 4 else [(x + 1, y), (x + 5, y)] if d == 1 \
                           else [(x, y), (x + d, y), (x + 5, y)]

                _, action = Board.Q_value(legal_actions=actions)

                return action
    # row
    for x in range(boardLength):
        for y in range(boardLength-5):
            pieces = tuple(board[x][y+d] for d in range(6))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(color) == 3 and 0 in pieces[1:5]:
                d = pieces.index(0, 1, -1)
                actions = [(x, y), (x, y + 4)] if d == 4 else [(x, y + 1), (x, y + 5)] if d == 1 \
                    else [(x, y), (x, y + d), (x, y + 5)]

                _, action = Board.Q_value(legal_actions=actions)

                return action
    # positive diagonal
    for x in range(boardLength-5):
        for y in range(boardLength-5):
            pieces = tuple(board[x+d][y+d] for d in range(6))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(color) == 3 and 0 in pieces[1:5]:
                d = pieces.index(0, 1, -1)
                actions = [(x, y), (x + 4, y + 4)] if d == 4 else [(x + 1, y + 1), (x + 5, y + 5)] if d == 1 \
                    else [(x, y), (x + d, y + d), (x + 5, y + 5)]

                _, action = Board.Q_value(legal_actions=actions)

                return action
    # oblique diagonal
    for x in range(boardLength-5):
        for y in range(5, boardLength):
            pieces = tuple(board[x+d][y-d] for d in range(6))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(color) == 3 and 0 in pieces[1:5]:
                d = pieces.index(0, 1, -1)
                actions = [(x, y), (x + 4, y - 4)] if d == 4 else [(x + 1, y - 1), (x + 5, y - 5)] if d == 1 \
                    else [(x, y), (x + d, y - d), (x + 5, y - 5)]

                _, action = Board.Q_value(legal_actions=actions)

                return action
    return None


def search_double(Board, color):
    # 'double four', 'four-three' and 'double three'
    boardLength = pp.width
    board = Board.board
    # possible actions to achieve four
    # column
    col4_my = set()
    col4_op = set()
    for x in range(boardLength - 4):
        for y in range(boardLength):
            pieces = tuple(board[x + d][y] for d in range(5))
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
            pieces = tuple(board[x][y + d] for d in range(5))
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
            pieces = tuple(board[x + d][y + d] for d in range(5))
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
            pieces = tuple(board[x + d][y - d] for d in range(5))
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
            pieces = tuple(board[x + d][y] for d in range(6))
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
            pieces = tuple(board[x][y + d] for d in range(6))
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
            pieces = tuple(board[x + d][y + d] for d in range(6))
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
            pieces = tuple(board[x + d][y - d] for d in range(6))
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
