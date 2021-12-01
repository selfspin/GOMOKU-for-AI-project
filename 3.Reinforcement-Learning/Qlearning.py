from board import *


class Qlearner:
    def __init__(self, network, boardSize=20, learning_rate=0.001, gamma=0.9):
        self.network = network
        self.boardSize = boardSize
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.C = 10  # Fixed Q-Targets

    def learning(self, numTrails=200):
        fixed_network = deepcopy(self.network)
        for t in range(numTrails):
            newGame = np.zeros(self.boardSize, self.boardSize)
            board = Board(newGame, fixed_network)
            board.update_board(int(self.boardSize / 2), int(self.boardSize / 2))

            reward = 0
            while True:
                x, y = board.e_greedy()
                board.update_board(x, y)
                feature = board.extract_feature()

                winner = board.is_win()
                if winner == 1:
                    target = 100
                elif winner == 2:
                    target = -100
                else:
                    bestQ, _ = board.Q_value()
                    target = reward + self.gamma * bestQ

                self.network.train(feature, target)

                if winner:
                    break

            if (t+1) % self.C == 0:
                fixed_network = deepcopy(self.network)
                print(fixed_network.params)
