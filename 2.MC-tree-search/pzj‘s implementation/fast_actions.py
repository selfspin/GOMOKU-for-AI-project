import pisqpipe as pp
import copy
import regex
from main import logDebug


def fast_kill_action(board, color):
    action = search_five(board, color)
    if action is not None:
        return action
    action = search_five(board, 3 - color)
    if action is not None:
        return action
    action = search_four(board, color)
    if action is not None:
        return action
    action = search_four_op(board, 3 - color)
    if action is not None:
        return action
    action = search_double(board, color)
    if action is not None:
        return action
    return None


def search_five(board, color):
    boardLength = pp.width
    # column
    for x in range(boardLength - 4):
        for y in range(boardLength):
            pieces = tuple(board[x + d][y] for d in range(5))
            if pieces.count(color) == 4 and 0 in pieces:
                d = pieces.index(0)
                return x + d, y
    # row
    for x in range(boardLength):
        for y in range(boardLength - 4):
            pieces = tuple(board[x][y + d] for d in range(5))
            if pieces.count(color) == 4 and 0 in pieces:
                d = pieces.index(0)
                return x, y + d
    # positive diagonal
    for x in range(boardLength - 4):
        for y in range(boardLength - 4):
            pieces = tuple(board[x + d][y + d] for d in range(5))
            if pieces.count(color) == 4 and 0 in pieces:
                d = pieces.index(0)
                return x + d, y + d
    # oblique diagonal
    for x in range(boardLength - 4):
        for y in range(4, boardLength):
            pieces = tuple(board[x + d][y - d] for d in range(5))
            if pieces.count(color) == 4 and 0 in pieces:
                d = pieces.index(0)
                return x + d, y - d
    return None


def search_four(board, color):
    boardLength = pp.width
    # column
    for x in range(boardLength - 5):
        for y in range(boardLength):
            pieces = tuple(board[x + d][y] for d in range(6))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(color) == 3 and 0 in pieces[1:5]:
                d = pieces.index(0, 1, -1)
                return x + d, y
    # row
    for x in range(boardLength):
        for y in range(boardLength - 5):
            pieces = tuple(board[x][y + d] for d in range(6))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(color) == 3 and 0 in pieces[1:5]:
                d = pieces.index(0, 1, -1)
                return x, y + d
    # positive diagonal
    for x in range(boardLength - 5):
        for y in range(boardLength - 5):
            pieces = tuple(board[x + d][y + d] for d in range(6))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(color) == 3 and 0 in pieces[1:5]:
                d = pieces.index(0, 1, -1)
                return x + d, y + d
    # oblique diagonal
    for x in range(boardLength - 5):
        for y in range(5, boardLength):
            pieces = tuple(board[x + d][y - d] for d in range(6))
            if pieces[0] == 0 and pieces[5] == 0 and pieces[1:5].count(color) == 3 and 0 in pieces[1:5]:
                d = pieces.index(0, 1, -1)
                return x + d, y - d
    return None


def search_four_op(board, color):
    boardLength = pp.width
    # column
    for x in range(boardLength - 5):
        for y in range(boardLength):
            pieces = tuple(board[x + d][y] for d in range(6))
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
                    fea_my_new, fea_op_new = update_features(board_new, x, y, fea, fea)
                    value = utility(fea_my_new, fea_op_new)
                    if value > max_utility:
                        action = a
                        max_utility = value
                return action
    # row
    for x in range(boardLength):
        for y in range(boardLength - 5):
            pieces = tuple(board[x][y + d] for d in range(6))
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
                    fea_my_new, fea_op_new = update_features(board_new, x, y, fea, fea)
                    value = utility(fea_my_new, fea_op_new)
                    if value > max_utility:
                        action = a
                        max_utility = value
                return action
    # positive diagonal
    for x in range(boardLength - 5):
        for y in range(boardLength - 5):
            pieces = tuple(board[x + d][y + d] for d in range(6))
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
                    fea_my_new, fea_op_new = update_features(board_new, x, y, fea, fea)
                    value = utility(fea_my_new, fea_op_new)
                    if value > max_utility:
                        action = a
                        max_utility = value
                return action
    # oblique diagonal
    for x in range(boardLength - 5):
        for y in range(5, boardLength):
            pieces = tuple(board[x + d][y - d] for d in range(6))
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
                    fea_my_new, fea_op_new = update_features(board_new, x, y, fea, fea)
                    value = utility(fea_my_new, fea_op_new)
                    if value > max_utility:
                        action = a
                        max_utility = value
                return action
    return None


def search_double(board, color):
    # 'double four', 'four-three' and 'double three'
    boardLength = pp.width

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


def update_actions(board, old_actions, x, y, k = 1):
    actions = copy.deepcopy(old_actions)
    if (x, y) in actions:
        actions.remove((x, y))
    for i in range(x - k, x + k + 1):
        for j in range(y - k, y + k + 1):
            if i >= 0 and j >= 0 and i < pp.width and j < pp.height and board[i][j] == 0 and (i, j) not in actions:
                actions.append((i, j))
    return actions


def update_features_string(s, position, fea_my, fea_op):
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
    i = 0
    for goal in pattern1:
        num = 0
        for mod in goal:
            num += len(regex.findall(mod, s, overlapped = True))
        fea_my[i] += num
        i += 1
    i = 0
    for goal in pattern2:
        num = 0
        for mod in goal:
            num += len(regex.findall(mod, s, overlapped = True))
        fea_op[i] += num
        i += 1

    s = s[:position] + '0' + s[position + 1:]
    i = 0
    for goal in pattern1:
        num = 0
        for mod in goal:
            num += len(regex.findall(mod, s, overlapped = True))
        fea_my[i] -= num
        i += 1
    i = 0
    for goal in pattern2:
        num = 0
        for mod in goal:
            num += len(regex.findall(mod, s, overlapped = True))
        fea_op[i] -= num
        i += 1
    return


def update_features(board, x, y, old_fea_my, old_fea_op):
    k = 5
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
    coefmy = [1e11, 1e9, 1e7, 0, 1e6, 5e2, 0, 1e2, 3, 0]
    coefop = [1e11, 8e8, 5e6, 0, 1e4, 5e2, 0, 1e2, 3, 0]
    l = len(coefmy)
    for i in range(l):
        value = value + coefmy[i] * fea_my[i] - coefop[i] * fea_op[i]
    return value
