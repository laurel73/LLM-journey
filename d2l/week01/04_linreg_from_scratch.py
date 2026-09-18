import random
import torch
from d2l import torch as d2l


def synthetic_data(w, b, num_examples):  # 造数据集
    X = torch.normal(0, 1, (num_examples, len(w)))  # 取 X
    y = torch.matmul(X, w) + b  # 建立 y 和 X 映射
    y += torch.normal(0, 0.01, y.shape)  # 添加噪声
    return X, y.reshape((-1, 1))


true_w = torch.tensor([2, -3.4])
true_b = 4.2

features, labels = synthetic_data(true_w, true_b, 1000)  # 计算 X=features、y=labels


def data_iter(batch_size, features, labels):  # 取小批量
    num_example = len(features)
    indices = list(range(num_example))  # 排序
    random.shuffle(indices)  # 打乱
    for i in range(0, num_example, batch_size):  # 遍历切分
        batch_indices = torch.tensor(indices[i: min(i + batch_size, num_example)])
        yield features[batch_indices], labels[batch_indices]  # 输出单个批次


w = torch.normal(0, 0.01, size=(2, 1), requires_grad=True)  # 初始化 w
b = torch.zeros(1, requires_grad=True)  # b


def linreg(X, w, b):  # @save 定义函数
    y = torch.mm(X, w) + b
    return y


def squared_loss(y_hat, y):  # 定义损失函数
    l = (y_hat - y.reshape(y_hat.shape)) ** 2 / 2
    return l


def sgd(params, lr, batch_size):  # 定义梯度下降函数
    with torch.no_grad():  # 不要求 grad
        for param in params:  # 轮询所有参数做梯度下降
            param -= lr * param.grad / batch_size
            param.grad.zero_()  # 归零梯度
    return params


lr = 0.03
num_epochs = 3
batch_size = 10
net = linreg
loss = squared_loss

for epoch in range(num_epochs):  # 轮数执行
    for X, y in data_iter(batch_size, features, labels):  # 单轮批数
        l = loss(net(X, w, b), y)  # 损失计算
        l.sum().backward()  # 反向传播
        sgd([w, b], lr, batch_size)  # 由梯度下降
    with torch.no_grad():  # 不要求 grad
        train_l = loss(net(features, w, b), labels)
        print(f'epoch {epoch + 1}, loss {float(train_l.mean()):f}')

print('w 的误差估计：', true_w - w.reshape(true_w.shape))
print('b 的误差估计：', true_b - b)
