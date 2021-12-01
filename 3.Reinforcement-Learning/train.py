import Qlearning
import nn


network = nn.NN()
learner = Qlearning.Qlearner(network)
learner.learning()