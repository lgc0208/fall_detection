# -*- coding: UTF-8 -*-
"""
    File Name:          flask_LSTM.py
    Author:             LIN Guocheng
    Version:            1.1.2
    Description:        使用 Flask 进行摔倒检测的模型部署
    History:
        1.  Date:           2022-1-16
            Author:         LIN Guocheng
            Modification:   修改了预测结果的判断规则
        2.  Date:           2022-1-17
            Author:         LIN Guocheng
            Modification:   增加了初始的提示页面
        3.  Date:           2022-1-21
            Author:         LIN Guocheng
            Modification:   修改了host地址和预测返回值
        4.  Date:           2022-1-26
            Author:         LIN Guocheng
            Modification:   针对可能产生的错误 unexpected EOF while parsing 进行修正
        5.  Date:           2022-4-15
            Author:         LIN Guocheng
            Modification:   针对硬件端发送报文有限的情况，将每次需要传递 32 组值改为传递任意组值，并使用 CSV 文件存储32组值。每收到新的值传
                            递时更新 CSV 文件，并调用模型进行预测
        6.  Date:           2022-4-15
            Author:         LIN Guocheng
            Modification:   针对服务器使用的 8000 端口进行适配，同时只有当传输的数据数据符合预测条件时才更新 CSV
        7.  Date:           2022-4-15
            Author:         LIN Guocheng
            Modification:   增加对用户状态的记录文件和访问接口，可以直接获取用户当前是否摔倒的状态
        8.  Date:           2022-4-15
            Author:         LIN Guocheng
            Modification:   修改了对用户当前状态的判断规则，只有当连续20次预测结果中判断摔倒次数大于正常次数时，更新用户状态为摔倒
        9.  Date:           2022-4-16
            Author:         LIN Guocheng
            Modification:   优化了摔倒状态的判断方式
        10. Date:           2022-5-6
            Author:         LIN Guocheng
            Modification:   增加了经纬度位置的获取和设置接口
        11. Date:           2022-5-12
            Author:         LIN Guocheng
            Modification:   增加了 SSL 证书，支持 HTTPS
        12. Date:           2022-5-20
            Author:         LIN Guocheng
            Modification:   在主页增加项目说明和 LOGO
"""

import flask
import numpy as np
import logging

import pandas as pd
from gevent import pywsgi
from tensorflow.keras.models import load_model

host = '0.0.0.0'

# 实例化
app = flask.Flask(__name__)

# 加载模型
model = load_model("model/LSTM.h5")

# GPS 定位数据，初始位置定义为北京市
gps_data = {"lon": 116.397128, "lat": 39.916527}


# 初始界面
@app.route("/")
def index():
    return flask.render_template("index.html")


# 预测界面
@app.route("/predict", methods=["GET", "POST"])
def predict():
    data = {"success": False, "result": 0}
    params = flask.json

    if params is None:
        params = flask.request.form.getlist("")

    # 接收到输入参数，返回预测值
    if params is not None:
        app.logger.info("\n")
        test_data = flask.request.args.getlist("testData")
        if test_data is not None:
            test_data = eval(str(test_data).replace("\'", ""))
            test_data = np.array(test_data, dtype="float")

            predict_values = pd.read_csv("data.csv", header=None).dropna(axis=0, how="any").values

            if predict_values is None:
                predict_values = test_data[:, :]
            else:
                predict_values = np.append(predict_values, test_data, axis=0)[-32:, :]

            # 保存至 csv
            ready_to_save = predict_values

            predict_values = predict_values[None, :, :]

            app.logger.info("收到预测请求\n")
            y_predict = model.predict(predict_values)
            app.logger.info("预测结果为：")
            if y_predict > 0.5:
                data["result"] = 1  # "出现摔倒"
            else:
                data["result"] = 0  # "无事发生"
            app.logger.info(data["result"])
            app.logger.info("\n")
            data["success"] = True
            # 预测成功了才更新 csv
            data_to_save = pd.DataFrame(ready_to_save)
            data_to_save.to_csv('data.csv', header=False, index=False)

            # 记录判断的当前状态值
            new_state = np.array([[data["result"]]])
            old_state = pd.read_csv('state.csv', header=None).dropna(axis=0, how="any").values
            state_to_save = np.append(old_state, new_state, axis=0)[-20:]
            state_to_save = pd.DataFrame(state_to_save)
            state_to_save.to_csv("state.csv", header=False, index=False)
        # 返回 json
        return flask.jsonify(data["result"])


# 获取经纬度界面
@app.route("/gps", methods=["GET", "POST"])
def gps():
    params = flask.json

    if params is None:
        params = flask.request.form.get("")

    # 接收到输入参数，返回预测值
    if params is not None:
        app.logger.info("\n")
        lon = flask.request.args.get("lon")  # 获取经度
        lat = flask.request.args.get("lat")  # 获取纬度
        if lon is None and lat is None:
            print("GPS data is : ", gps_data)
            return flask.jsonify(gps_data)
        else:
            gps_data["lon"] = float(lon)
            gps_data["lat"] = float(lat)
            print("GPS data is : ", gps_data)
            return "GPS data has updated successfully"


# 获取用户当前状态
@app.route("/state", methods=['GET', 'POST'])
def state():
    all_state = pd.read_csv("state.csv", header=None).dropna(axis=0, how="any").values
    fall_down_state = int(np.sum(all_state == 1))
    normal_state = int(np.sum(all_state == 0))
    if fall_down_state > normal_state:
        user_state = 1
    else:
        user_state = 0
    return str(user_state)


# 启动 flask
if __name__ == '__main__':
    app.debug = True
    logging.disable_existing_loggers = False
    handler = logging.FileHandler('logs/flask.log', encoding='UTF-8')
    handler.setLevel(logging.DEBUG)
    logging_format = logging.Formatter("%(asctime)s flask %(levelname)s %(message)s")
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)
    server = pywsgi.WSGIServer(('0.0.0.0', 8000), app, log=app.logger)
    server.serve_forever()
