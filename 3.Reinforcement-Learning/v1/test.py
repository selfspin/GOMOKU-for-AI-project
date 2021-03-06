import numpy as np
import nn

# 读取参数
x = np.array([[0.],
              [1.],
              [0.],
              [1.],
              [1.],
              [1.],
              [0.],
              [0.],
              [0.],
              [0.],
              [1.],
              [1.],
              [0.],
              [0.],
              [0.],
              [0.],
              [0.],
              [1.],
              [1.],
              [1.],
              [1.],
              [0.],
              [0.],
              [0.],
              [1.],
              [1.],
              [1.],
              [1.],
              [1.],
              [1.5],
              [0.],
              [1.],
              [1.],
              [1.],
              [1.],
              [1.],
              [0.],
              [0.],
              [1.],
              [1.],
              [1.],
              [0.],
              [0.],
              [0.],
              [0.],
              [1.],
              [1.],
              [1.],
              [1.],
              [1.],
              [1.],
              [0.],
              [1.],
              [1.],
              [1.],
              [1.],
              [0.],
              [0.],
              [0.],
              [1.],
              [1.],
              [1.],
              [1.],
              [1.],
              [2.],
              [0.],
              [1.],
              [1.],
              [1.],
              [1.],
              [1.],
              [0.],
              [0.],
              [1.],
              [1.],
              [1.],
              [1.],
              [1.],
              [0.],
              [0.],
              [1.],
              [1.],
              [1.],
              [1.],
              [1.],
              [4.],
              [0.],
              [1.],
              [1.],
              [1.],
              [1.],
              [0.],
              [0.],
              [0.],
              [1.],
              [1.],
              [1.],
              [1.],
              [1.],
              [1.],
              [0.],
              [1.],
              [1.],
              [1.],
              [1.],
              [1.],
              [3.5],
              [0.],
              [1.],
              [1.],
              [1.],
              [1.],
              [1.],
              [6.5],
              [0.],
              [1.],
              [1.],
              [1.],
              [1.],
              [1.],
              [5.],
              [0.],
              [1.],
              [1.],
              [1.],
              [1.],
              [1.],
              [7.5],
              [0.],
              [1.],
              [1.],
              [1.],
              [1.],
              [1.],
              [2.5],
              [0.],
              [1.],
              [1.],
              [1.],
              [1.],
              [0.],
              [0.],
              [0.],
              [1.],
              [1.],
              [1.],
              [1.],
              [0.],
              [0.],
              [0.],
              [0.],
              [0.],
              [0.],
              [1.],
              [1.],
              [0.],
              [0.],
              [0.],
              [0.],
              [0.],
              [0.],
              [0.],
              [0.],
              [0.],
              [0.],
              [0.],
              [0.],
              [1.],
              [1.],
              [1.],
              [0.],
              [0.],
              [0.],
              [0.],
              [1.],
              [1.],
              [1.],
              [0.],
              [0.],
              [0.],
              [0.],
              [1.],
              [1.],
              [0.],
              [0.],
              [0.],
              [0.],
              [0.],
              [1.],
              [1.],
              [1.],
              [1.],
              [0.],
              [0.],
              [0.],
              [1.],
              [1.],
              [1.],
              [1.],
              [1.],
              [0.5],
              [0.],
              [1.],
              [1.],
              [0.],
              [0.],
              [0.],
              [0.],
              [0.],
              [1.],
              [1.],
              [1.],
              [1.],
              [1.],
              [4.5],
              [0.],
              [1.],
              [1.],
              [1.],
              [0.],
              [0.],
              [0.],
              [0.],
              [1.],
              [1.],
              [1.],
              [0.],
              [0.],
              [0.],
              [0.],
              [0.],
              [0.],
              [0.],
              [0.],
              [0.],
              [0.],
              [0.],
              [0.],
              [0.],
              [0.],
              [0.],
              [0.],
              [0.],
              [0.],
              [1.],
              [1.],
              [0.],
              [0.],
              [0.],
              [0.],
              [0.],
              [1.],
              [1.],
              [1.],
              [1.],
              [1.],
              [1.5],
              [0.],
              [1.],
              [1.],
              [1.],
              [1.],
              [1.],
              [6.],
              [0.],
              [1.],
              [1.],
              [1.],
              [1.],
              [1.],
              [6.5],
              [0.],
              [1.],
              [1.],
              [1.],
              [1.],
              [1.],
              [1.5],
              [0.],
              [1.],
              [1.],
              [1.],
              [1.],
              [0.],
              [0.],
              [0.],
              [1.],
              [1.],
              [1.],
              [1.],
              [1.],
              [3.],
              [0.],
              [1.],
              [1.],
              [1.],
              [1.],
              [1.],
              [1.],
              [1.],
              [1.],
              [0.]])
par = np.load('para_replay_yx.npy', allow_pickle=True)
par = par.reshape(1)[0]
net = nn.NN(params=par)
print(net.full_forward_propagation(x, par)[0])

# 训练经验回放
f = np.load('replay_feature_yx.npy', allow_pickle=True)
y = np.load('replay_target_yx.npy', allow_pickle=True)
_ = net.train(f, y, 100)
print(net.full_forward_propagation(x, net.params)[0])
np.save('para_replay_yx.npy', net.params)

# 初始化经验回放
replay_f = np.empty((302, 0))
replay_y = np.empty((1, 0))
np.save('replay_feature_yx', replay_f)
np.save('replay_target_yx', replay_y)
