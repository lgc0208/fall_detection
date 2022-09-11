<h2 align="center"> 基于 ATK-MPU6050 和 LSTM 的摔倒检测算法 </h2>
<p align="center"><b>国家级/2021-2022大学生创新创业训练项目/人工智能学院/北京邮电大学</b></p>

<p align="center">
    <img src="https://badgen.net/github/license/lgc0208/fall_detection/">
    <img src="https://badgen.net/github/commits/lgc0208/fall_detection/main/">
    <img src="https://badgen.net/github/releases/lgc0208/fall_detection/">    
    <img src="https://badgen.net/github/release/lgc0208/fall_detection">
    <img src="https://badgen.net/github/last-commit/lgc0208/fall_detection/main/">
</p>

## 目录

- [环境依赖](#环境依赖)
- [目录结构描述](#目录结构描述)
- [版本更新](#版本更新)
    - [Version 1.0.0](#version-100)
    - [Version 1.1.0](#version-110)
- [贡献者](#贡献者)





## 环境依赖

- TensorFlow 2.7.0
- flask 1.1.2
- gevent 21.8.0
- numpy 1.19.5
- h5py 3.6.0

## 目录结构描述

```
├── README.md              // 说明文档
├── LICENSE                // 开源协议
├── h5_to_pb.py            // 将 h5 模型转换为 pb 模型
├── flask_LSTM.py	   // 基于 flask 框架的 LSTM 模型部署代码
├── interface_test.py	   // 测试接口
├── data.csv     	   // 用户姿态信息
├── state.csv	           // 用户历史状态信息
├── model                  // 模型
│   ├── LSTM.h5  	   // h5 模型
│   └── LSTM.pb            // pb 模型
├── image                  // 图文件夹
│   └── logo.png           // 团队 LOGO
├── logs                   // 日志文件夹
│   └── flask.log          // flask 运行日志
├── templates              // HTML 文件夹
│   └── index.html         // 服务器首页信息
├── 2021.10实验处理         // 2021年10月的实验数据处理和模型训练稿
├── 2021.12实验处理         // 2021年12月的实验数据处理和模型训练稿
└── arduino     	   // 硬件arduino部分代码
```

## 版本更新

### Version 1.0.0

1. 在已有的基于LSTM分类预测模型的基础上，通过修改隐藏层节点数，更改输出层激活函数的方式，将模型预测的准确度由原来的平均96.29%提升到了100%。测试方式为每次任意选取80%数据作为训练集，20%数据作为测试集，将模型从零重新训练。
2. 基于Flask框架，设计并实现了将已有机器学习部署的后端程序，在本地服务器上使用POSTMAN测试通过。后端可以接收通过URL传递的32组来自传感器6个不同纬度的数据，并调用已经训练完成的机器学习模型进行预测，最终将预测的结果通过result键返回。
3. 增加了访问的初始界面，可用于后期前端代码的部署。

### Version 1.1.0

1. 修改了摔倒的判决规则，只有当连续20次预测结果中判断摔倒次数大于正常次数时，判断用户状态为摔倒。
2. 增加对用户状态的文件记录功能和访问接口，可以直接获取用户当前是否摔倒的状态。
3. 针对硬件端发送报文有限的情况，将每次需要传递 32 组值改为传递任意组值，并使用 CSV 文件存储32组值。每收到新的值传递时更新 CSV 文件，并调用模型进行预测。
4. 制定 CSV 更新规则，同时只有当传输的数据数据符合模型预测条件时才更新 CSV。
5. 增加了用户定位信息的获取和设置接口。

## 贡献者
- [LIN Guocheng](https://github.com/lgc0208)
- [HUANG ShiYang](https://github.com/moontree613)
- DONG Tianyu
