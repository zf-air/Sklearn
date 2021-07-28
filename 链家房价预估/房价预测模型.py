# 房价预测模型
# 用到的特征（面积，朝向，装修，板塔）
# 目标（房价）

# 导入库
import joblib
import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 接收参数,一定有一个参数是python路径，list下标从1开始
# 一共12个参数，前11个是用户输入，最后一个是模型名称
# X_data = [70, 0,1,0,0, 1,0,0, 1,0,0 ,Model]
X_data = []
if(len(sys.argv)>1):
        for i in range(1,len(sys.argv)):
                # print("\n",sys.argv[i])
                X_data.append(sys.argv[i])
else:
        print("无参数\n")

# 获取模型名
Model = X_data.pop()

# 把string类型转为int类型
for i in range(len(X_data)):
        X_data[i] = int(X_data[i])

# 特征
X_TeZheng = ['面积', '朝向_东', '朝向_南', '朝向_西', '朝向_北', '装修_毛坯', '装修_简装',
        '装修_精装', '板塔_塔楼', '板塔_板塔结合', '板塔_板楼']

# 转换为DataFrame对象
df = pd.DataFrame(data = [X_data],columns = X_TeZheng)

# 划分为测试集
X_test = df[0:1]

# 加载模型
os.chdir("E:\\GitProjects\\Sklearn\\链家房价预估\\")
# forest_reg = joblib.load("GaoXin_ForestModel.model")
forest_reg = joblib.load(Model)

# 模型预测
Y_predict = forest_reg.predict(X_test)

# 输出价格
print(Y_predict)

# success
# print("success")