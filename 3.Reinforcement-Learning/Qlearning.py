from board import *
import numpy as np

replay_f = np.empty((302,0))
replay_y = np.empty((1,0))

class Qlearner:
    def __init__(self, network, boardSize=10, learning_rate=0.001, gamma=0.99):
        self.network = network
        self.boardSize = boardSize
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.C = 3  # Fixed Q-Targets

    def learning(self, numTrails=100):
        global replay_f, replay_y
        fixed_network = deepcopy(self.network)
        for t in range(numTrails):
            newGame = np.zeros((self.boardSize, self.boardSize))
            board = Board(newGame, fixed_network)
            board.update_board(int(self.boardSize / 2), int(self.boardSize / 2))

            # reward = 0
            while True:
                x, y = board.e_greedy()
                print(x, y)

                board.update_board(x, y)
                # print('update board done')

                feature = board.extract_feature()
                # print('extract_feature done')

                winner = board.is_win()
                if winner == 1:
                    target = np.array(1).reshape((1, 1))
                    self.network.train(feature, target)
                    replay_y = np.concatenate((replay_y, target), axis=1)
                    replay_f = np.concatenate((replay_f, feature), axis=1)
                    # file_handle = open('replay.txt', mode='a')
                    # file_handle.write(str(replay)+'\n')
                    # file_handle.close()
                    # print('end feature')
                    # print(feature)
                    # print(board.board)
                elif winner == 2:
                    target = np.array(0).reshape((1, 1))
                    self.network.train(feature, target)
                    replay_y = np.concatenate((replay_y, target), axis=1)
                    replay_f = np.concatenate((replay_f, feature), axis=1)
                    # replay = (feature, target)
                    # file_handle = open('replay.txt', mode='a')
                    # file_handle.write(str(replay)+'\n')
                    # file_handle.close()
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

                if winner:
                    break

            if (t + 1) % self.C == 0:
                fixed_network = deepcopy(self.network)
                # print(fixed_network.params)

            print('###########', t)
            print(self.network.params)
            print(board.board)
            np.save('para.npy', self.network.params)
            # file_handle = open('para.txt', mode='a')
            # file_handle.write(str(self.network.params))
            # file_handle.close()
        np.save('replay_feature', replay_f)
        np.save('replay_target', replay_y)
        # print(replay)
