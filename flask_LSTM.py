"""
    File Name:          flask_LSTM.py
    Author:             LIN Guocheng
    Version:            0.0.1
    Description:        使用 Flask 进行模型部署
    History:            
        1.  Date:           q
            Author:         LIN Guocheng
            Modification:   1
"""

import flask
import pandas as pd
import numpy as np
import json
from tensorflow.keras.models import load_model

host = '0.0.0.0'

# 实例化
app = flask.Flask(__name__)

# 加载模型
model = load_model("model/LSTM.h5")

@app.route("/predict", methods=["GET", "POST"])

def predict():
    data = {"success" : False}
    data = {"result" : ""}
    
    params = flask.json
    if(params == None):
        params = flask.request.form.getlist("")
        
    # 接收到输入参数，返回预测值
    if(params != None):
        print("##################/n")
        test_data = flask.request.args.getlist("testData")
        test_data = eval(str(test_data).replace("\'", ""))
        test_data = np.array(test_data)
        # 升维
        test_data = test_data[None,:,:]
        print("收到预测请求\n")
        y_predict = model.predict(test_data)  
        print("预测结果为：")
        if(y_predict > 0.5):
            data["result"] = "出现摔倒"
        else:
           data["result"] = "无事发生"
        #data["prediction"] = str(y_predict)
        print(data["result"])
        data["success"] = True
        
        # 返回 json
        return flask.jsonify(data)
    
# 启动 flask
if __name__ == '__main__':
    app.run(debug=False, host=host)