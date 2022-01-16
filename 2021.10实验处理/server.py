#server.py
"""
Created on Sun Nov 28 20:12:21 2021

@author:LIN Guocheng
@email: lgc0208@bupt.edu.cn

Description:
"""

# 引入包，构建网络并加载训练好的参数
from flask import Flask, request
import numpy as np
import tensorflow as tf
from tensorflow import keras
import sys, os
import base64
import cv2
sys.path.append(os.path.abspath('./model'))
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),
    keras.layers.Dense(128, activation=tf.nn.relu),
    keras.layers.Dense(10, activation=tf.nn.softmax)
])
model.load_weights('./model/LSTM.h5')
graph = tf.get_default_graph()

def b64_to_ndarray(image_b64):
    img_bytes = base64.b64decode(image_b64)
    nparr = np.frombuffer(img_bytes, np.uint8)
    arr = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
    assert arr.shape == (28, 28)
    arr = arr[None, :, :] / 255.0
    return arr

app = Flask(__name__)
# global model, graph
@app.route('/predict', methods=['POST'])
def predict():
    b64 = request.get_data()
    arr = b64_to_ndarray(b64)
    print(arr.shape)
    with graph.as_default():
        ret = model.predict(arr)
    resp = np.array_str(np.argmax(ret, axis=1))
    return resp

port = int(os.environ.get('PORT', 5060))
app.run(host='0.0.0.0', port=port)