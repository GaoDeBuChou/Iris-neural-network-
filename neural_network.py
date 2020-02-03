import numpy as np
from sklearn.datasets import load_iris

def sigmoid(A):
    return 1 / (1 + np.exp(-A))

def costfunc(h,y,m): # 代价函数  h：估计函数结果  y：目标  m：样本数
    return -1/m*np.sum(y*np.log(h)+(1-y)*np.log(1-h))

#导入训练集、测试集
iris_dataset = load_iris()
X=np.array(iris_dataset['data'])
X=np.insert(X, 0, values=[1], axis=1)
X_test=X[4::5].T
X_train=np.concatenate([X[0::5],X[1::5],X[2::5],X[3::5]]).T

y_temp=np.array(iris_dataset['target'])
y=np.zeros((3,150))
for i in range(0,150):
    if y_temp[i]==0:
        y[0,i]=1 #[1,0,0]
    elif y_temp[i]==1:
        y[1,i]=1 #[0,1,0]
    else:
        y[2,i]=1 #[0,0,1]
y_test=np.array(y[:,0::5])
y_train=np.concatenate([y[:,1::5],y[:,2::5],y[:,3::5],y[:,4::5]],axis=1)

m=120

#输入：4个单元 隐藏层：2层 每层4个单元 输出层：3个单元
theta1=-1+2*np.random.random((4,5))
theta2=-1+2*np.random.random((4,5))
theta3=-1+2*np.random.random((3,5))
Delta4=np.zeros((3,m))
Delta3=np.zeros((5,m))
Delta2=np.zeros((5,m))

while True:#梯度下降
    #正向传播
    a2_train=sigmoid(theta1 @ X_train)
    a2_train=np.insert(a2_train, 0, values=[1], axis=0)
    a3_train=sigmoid(theta2 @ a2_train)
    a3_train=np.insert(a3_train, 0, values=[1], axis=0)
    a4_train=sigmoid(theta3 @ a3_train)

    J=costfunc(a4_train,y_train,m)
    print(J)
    if J<0.15:break

    #逆向传播
    Delta4=a4_train - y_train
    Delta3=theta3.T @ Delta4 * (a3_train * (1-a3_train))
    Delta3=np.delete(Delta3,0,axis=0)
    Delta2=theta2.T @ Delta3 * (a2_train * (1-a2_train))
    Delta2=np.delete(Delta2,0,axis=0)

    D3=Delta4 @ a3_train.T / m
    D2=Delta3 @ a2_train.T / m
    D1=Delta2 @ X_train.T / m

    theta3-=0.02*D3
    theta2-=0.02*D2
    theta1-=0.02*D1

#测试
a2_test = sigmoid(theta1 @ X_test)
a2_test = np.insert(a2_test, 0, values=[1], axis=0)
a3_test = sigmoid(theta2 @ a2_test)
a3_test = np.insert(a3_test, 0, values=[1], axis=0)
a4_test = sigmoid(theta3 @ a3_test)

a4_test=np.rint(a4_test)
s=0
for i in range(0,30):
    if a4_test[0,i]==y_test[0,i] and a4_test[1,i]==y_test[1,i]:
        s+=1
print('测试得分：',s/30)

#使用模型
new=[[1],[5],[2.9],[1],[0.2]]
a2_new = sigmoid(theta1 @ new)
a2_new = np.insert(a2_new, 0, values=[1], axis=0)
a3_new = sigmoid(theta2 @ a2_new)
a3_new = np.insert(a3_new, 0, values=[1], axis=0)
a4_new = sigmoid(theta3 @ a3_new)
print(np.rint(a4_new))

#一些优化待补充