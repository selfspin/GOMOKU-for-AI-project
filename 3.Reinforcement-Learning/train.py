import Qlearning
import nn
import numpy as np

par = np.load('para.npy', allow_pickle=True)
par = par.reshape(1)[0]
network = nn.NN(params=par)
learner = Qlearning.Qlearner(network)
learner.learning()
