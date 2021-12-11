from board import *
import numpy as np

replay_f = np.empty((302, 0))
replay_y = np.empty((1, 0))


class Qlearner:
    def __init__(self, network, boardSize=15, learning_rate=0.01, gamma=0.999):
        self.network = network
        self.boardSize = boardSize
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.C = 10  # Fixed Q-Targets

    def learning(self, numTrails=5):
        global replay_f, replay_y
        try:
            fixed_network = deepcopy(self.network)
            for t in range(numTrails):
                newGame = np.zeros((self.boardSize, self.boardSize))
                board = Board(newGame, fixed_network, explore_prob=0.2)
                board.update_board(int(self.boardSize / 2), int(self.boardSize / 2))

                # reward = 0
                k = 1
                while True:
                    x, y = board.e_greedy(e=0)
                    print(x, y)

                    board.update_board(x, y)
                    # print('update board done')

                    feature = board.extract_feature()
                    # print('extract_feature done')

                    winner = board.is_win()
                    if winner == 1:
                        target = np.array(1).reshape((1, 1))
                        # self.network.train(feature, target)
                        replay_y = np.concatenate((replay_y, np.ones((1, k))), axis=1)
                        # replay_f = np.concatenate((replay_f, feature), axis=1)

                        # print('end feature')
                        # print(feature)
                        # print(board.board)
                    elif winner == 2:
                        target = np.array(0).reshape((1, 1))
                        # self.network.train(feature, target)
                        replay_y = np.concatenate((replay_y, np.zeros((1, k))), axis=1)
                        # replay_f = np.concatenate((replay_f, feature), axis=1)
                        # replay = (feature, target)

                        # print('end feature')
                        # print(feature)
                        # print(board.board)
                    else:
                        bestQ, _ = board.Q_value()
                        # print('best Q done')
                        target = self.gamma * bestQ
                        print(target)

                    # self.network.train(feature, target)
                    # print('train done')

                    replay_f = np.concatenate((replay_f, feature), axis=1)

                    if winner:
                        break

                    k += 1

                if (t + 1) % self.C == 0:
                    fixed_network = deepcopy(self.network)
                    # print(fixed_network.params)

                print('###########', t)
                #print(self.network.params)
                print(board.board)
                #np.save('para.npy', self.network.params)

            #np.save('replay_feature', replay_f)
            #np.save('replay_target', replay_y)

        finally:
            pass
            #np.save('replay_feature', replay_f)
            #np.save('replay_target', replay_y)
        # print(replay)
