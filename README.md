<h2 align="center"> 基于 ATK-MPU6050 和 LSTM 的摔倒检测算法 </h2>
<p align="center"><b>2021-2022大学生创新创业训练项目/人工智能学院/北京邮电大学</b></p>




## 目录

- [环境依赖](#环境依赖)
- [目录结构描述](#目录结构描述)
- [版本更新](#版本更新)
	- [Version 1.0.0](#Version 1.0.0)
	- [Version 1.0.1](#Version 1.0.1)
- [贡献者](#贡献者)





## 环境依赖

- TensorFlow 2.7.0
- flask 1.1.2
- numpy 1.19.5
- h5py 3.6.0

## 目录结构描述

```
├── README.md                  // help
├── h5_to_pb.py                  // 将 h5 模型转换为 pb 模型
├── flask_LSTM.py 		// 基于 flask 框架的 LSTM 模型部署代码
├── model                            // 模型
│   ├── LSTM.h5 	 	// h5 模型
│   └── LSTM.pb 	        // pb模型
├── 2021.10实验处理         // 2021年10月的实验数据处理和模型训练稿
└── 2021.12实验处理         // 2021年12月的实验数据处理和模型训练稿
```

## 版本更新

### Version 1.0.0

1. 在已有的基于LSTM分类预测模型的基础上，通过修改隐藏层节点数，更改输出层激活函数的方式，将模型预测的准确度由原来的平均96.29%提升到了100%。测试方式为每次任意选取80%数据作为训练集，20%数据作为测试集，将模型从零重新训练。
2. 基于Flask框架，设计并实现了将已有机器学习部署的后端程序，在本地服务器上使用POSTMAN测试通过。后端可以接收通过URL传递的32组来自传感器6个不同纬度的数据，并调用已经训练完成的机器学习模型进行预测，最终将预测的结果通过result键返回。

### Version 1.0.1 
1. 增加了访问的初始界面，可用于后期前端代码的部署

## 贡献者
- [LIN Guocheng](https://github.com/lgc0208)
- [Huang ShiYang](https://github.com/moontree613)
- Dong Tianyu