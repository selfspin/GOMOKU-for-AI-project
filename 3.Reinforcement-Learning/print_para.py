import numpy as np

dic = np.load('para_replay_yx.npy', allow_pickle=True)
dic = dic.reshape(1)[0]

f = open('para.txt', 'w')

f.write('{')
for i in dic.keys():
    f.write('\'' + i + '\':\n')
    f.write('np.array([')
    for j in range(dic[i].shape[0]):
        f.write('[' + ",".join(str(i) for i in dic[i][j]) + ']')
        f.write(',\n')
    f.write(']),\n')

f.write('}')
