'''
@name:      LSTM.py
@author:    LIN Guocheng
@vision:    1.0.0
@function:  对一期实验数据进行处理，输出训练模型
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from os import listdir
from keras.preprocessing import sequence 
import tensorflow as tf 
from keras.models import Sequential 
from keras.layers import Dense 
from keras.layers import LSTM 

from keras.optimizers import adam_v2
from keras.models import load_model 
from keras.callbacks import ModelCheckpoint

df = pd.read_csv("10-15一期实验数据/10-15-001.csv", header=None, usecols=[0,1,2,3,4,5])
path = "10-15一期实验数据/"
sequences = list()
# 正样本数据
for i in range(1, 39):
    if i < 10:
        filePath = path + "10-15-00" + str(i) + ".csv"
    else:
        filePath = path + "10-15-0" + str(i) + ".csv"
    print(filePath)
    df = pd.read_csv(filePath, header=None, usecols=[0,1,2,3,4,5]).dropna(axis=0,how='any')
    values = df.values
    sequences.append(values)
# 负样本数据
for i in range(1, 20):
    filePath = path + "0-" + str(i) + ".csv"
    print(filePath)
    df = pd.read_csv(filePath, header=None, usecols=[0,1,2,3,4,5]).dropna(axis=0,how='any')
    values = df.values
    sequences.append(values)
    
targets = pd.read_csv("10-15一期实验数据/target.csv", header=None).values

# 由于时间序列数据长度不一，我们不能直接在这个数据集上建立模型。先找出最小、最大和平均长度：
len_sequences = [] 
for one_seq in sequences: 
    len_sequences.append(len(one_seq)) 

# 大多数文件的长度在 20 到 40 之间。只有极少个文件的长度超过 60 。因此，取最小或最大长度
# 没有多大意义。选择上四分位数作为序列的长度，进行数据处理
    
#用最后一行的值填充序列到最大长度
to_pad = 84
new_seq = []
for one_seq in sequences:
    len_one_seq = len(one_seq)
    last_val = one_seq[-1]
    n = to_pad - len_one_seq
   
    to_concat = np.repeat(one_seq[-1], n).reshape(6, n).transpose()
    new_one_seq = np.concatenate([one_seq, to_concat])
    new_seq.append(new_one_seq)
final_seq = np.stack(new_seq)

#将序列截断为长度 33
from keras.preprocessing import sequence
seq_len = 33
final_seq=sequence.pad_sequences(final_seq, maxlen=seq_len, padding='post', dtype='float', truncating='post')

# 引入训练集、测试集划分函数
from sklearn.model_selection import train_test_split

# 将数据集按照 80% 和 20% 的比例随机划分为训练集和测试集
train_data, test_data, train_target, test_target = train_test_split(final_seq, targets)

train_data = np.array(train_data)
test_data = np.array(test_data)

train_target = np.array(train_target)
#train_target = (train_target+1)/2

test_target = np.array(test_target)
#test_target = (test_target+1)/2

model = Sequential() 
model.add(LSTM(256, input_shape=(seq_len, 6))) 
model.add(Dense(1, activation='sigmoid'))
adam = adam_v2.Adam(lr=0.001)
chk = ModelCheckpoint('best_model.pkl', monitor='val_acc', save_best_only=True, mode='max', verbose=1)
model.compile(loss='binary_crossentropy', optimizer=adam, metrics=['accuracy'])
model.fit(train_data, train_target, epochs=200, batch_size=128, callbacks=[chk])
from sklearn.metrics import accuracy_score

test_preds = model.predict_classes(test_data)
accuracy_score(test_target, test_preds)