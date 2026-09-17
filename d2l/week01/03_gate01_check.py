import torch

# 创建两个随机张量（标准正态：均值 0、标准差 1）
x = torch.normal(0, 1, size=(3, 4))
y = torch.normal(0, 1, size=(4, 3))

# 要算梯度，得先声明这两个需要求导
x.requires_grad_(True)
y.requires_grad_(True)

# 矩阵乘法
z = x @ y

# 反向传播：backward 只能对标量用，所以先把 z 求和成一个数
z.sum().backward()

print("x =\n", x)
print("y =\n", y)
print("z = x @ y =\n", z)
print("x.grad =\n", x.grad)
print("y.grad =\n", y.grad)
