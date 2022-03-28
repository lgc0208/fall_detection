"""
    File Name:          flask_LSTM.py
    Author:             LIN Guocheng
    Version:            1.0.3
    Description:        使用 Flask 进行模型部署
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
"""

import flask
import numpy as np
import logging
from gevent import pywsgi
from tensorflow.keras.models import load_model

host = '0.0.0.0'

# 实例化
app = flask.Flask(__name__)

# 加载模型
model = load_model("model/LSTM.h5")


@app.before_request
def enable_form_raw_cache():
    if flask.request.path.startswith('/predict'):
        if flask.request.content_length > 1024 * 1024:  # 1mb
            flask.abort(413)  # Payload too large
        app.logger.info(flask.request.headers)
        app.logger.info(flask.request.data)


# 初始界面
@app.route("/")
def index():
    return "<h1> 服务器正在正常运行 <h1>"


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
            test_data = np.array(test_data)
            # 升维
            test_data = test_data[None, :, :]
            app.logger.info("收到预测请求\n")
            y_predict = model.predict(test_data)
            app.logger.info("预测结果为：")
            if y_predict > 0.5:
                data["result"] = 1  # "出现摔倒"
            else:
                data["result"] = 0  # "无事发生"
            app.logger.info(data["result"])
            app.logger.info("\n")
            data["success"] = True

        # 返回 json
        return flask.jsonify(data)


# 启动 flask
if __name__ == '__main__':
    app.debug = True
    logging.disable_existing_loggers = False
    handler = logging.FileHandler('logs/flask.log', encoding='UTF-8')
    handler.setLevel(logging.DEBUG)
    logging_format = logging.Formatter("%(asctime)s flask %(levelname)s %(message)s")
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app, log=app.logger)
    server.serve_forever()
