# %% [markdown]
# # d2l 第 2 章 · 起跑线
#
# **目标只有一个：把你在 TinySearch 里手写的 `cosine`，用 torch 重写一遍。**
#
# 你手写的就是「点积 ÷ 两个范数相乘」。d2l 2.3 只是给这两个操作起了名字，
# 并且提供了现成函数。所以这一章不是新知识，是给你已经会的东西换工具。
#
# **用法**：VS Code 里每个 cell 点 `Run Cell`，一个个跑，对照注释里的预期输出。
# 数对不上就停下来，别往下走。

# %%
import torch

print("torch:", torch.__version__)
print("CUDA 可用:", torch.cuda.is_available())

# %% [markdown]
# ---
# ## Part 1 · 2.1 数据操作（热身，20 分钟）
#
# **张量（tensor）是什么**：就是多维列表，外加一堆现成运算。
# 你昨天写的「一串数字」（词袋向量），在 torch 里就是一个一维张量。

# %%
x = torch.arange(12)
print(x)
print("shape:", x.shape)      # 形状 → torch.Size([12])
print("numel:", x.numel())    # 一共几个元素 → 12

# %%
# reshape：换个看法，元素总数不能变
X = x.reshape(3, 4)
print(X)
print("shape:", X.shape)      # → torch.Size([3, 4])

# %%
# 索引和切片 —— 跟 list 一模一样，从 0 开始
print("最后一行:", X[-1])
print("第 2 行:  ", X[1])
print("第 1~2 行:\n", X[0:2])
print("第 2 列:  ", X[:, 1])      # 逗号前管行，逗号后管列；`:` 表示全要

# %%
# 改元素（注意：这会直接改 X 本身）
X[0, 0] = 99
print(X)

# %% [markdown]
# ### 广播机制（2.1.3）
#
# 形状不同的两个张量做运算时，torch 会自动把小的那个「拡」到跟大的一样大。
#
# **规则**：两个形状**从右往左**逐位比，每一位满足其一就能广播：
# 相等 / 其中一个是 1 / 这一位缺失。
#
# 这是 torch 最省事的地方，也是最容易懵的地方。看懂下面这个例子就够用了。

# %%
a = torch.arange(3).reshape(3, 1)   # 3 行 1 列
b = torch.arange(2).reshape(1, 2)   # 1 行 2 列
print("a =\n", a)
print("b =\n", b)
print("a + b =\n", a + b)           # 自动扩成 3x2
print("结果形状:", (a + b).shape)    # → torch.Size([3, 2])

# %% [markdown]
# ---
# ## Part 2 · 2.3 点积与范数（主菜，30 分钟）
#
# 这两样就是你手写 `cosine` 的两块砖。
# 公式（直接给，这个不是你该凭空想出来的）：
#
# ```
# 点积 = 同位相乘，再全加起来        a·b = Σ(aᵢ × bᵢ)
# 范数 = 各位平方和，再开根号        |a| = √(Σaᵢ²)
# 余弦相似度 = 点积 / (|a| × |b|)
# ```

# %%
x = torch.tensor([1.0, 2, 3])
y = torch.tensor([4.0, 5, 6])

# 点积：1*4 + 2*5 + 3*6 = 32
print("点积:", torch.dot(x, y))       # → 32.0
# 对照你手写的：sum(i * j for i, j in zip(x, y))

# 范数（就是"长度"）：sqrt(1 + 4 + 9) = 3.7417
print("范数:", x.norm())               # → 3.7417
# 对照你手写的：math.sqrt(sum(i * i for i in x))

# %%
# 余弦相似度 —— 除法那步一个字都没变
sim = torch.dot(x, y) / (x.norm() * y.norm())
print("余弦相似度:", sim)              # → 0.9746

# 验证：自己跟自己比，必须精确等于 1.0
print("自己跟自己:", torch.dot(x, x) / (x.norm() * x.norm()))   # → 1.0

# %% [markdown]
# ---
# ## Part 3 · 用 torch 重写 TinySearch（收尾，20 分钟）
#
# 手写版和 torch 版跑同一批数据，数必须一模一样。

# %%
import math
import re

DOCS = [
    "列表推导式可以在一行里生成新列表，比如 squares = [x*x for x in range(10)]。",
    "字典的 setdefault 方法可以在键不存在时插入默认值，常用于分组统计。",
    "类是对象的模板，__init__ 方法在实例化时自动调用，self 指向实例自己。",
    "余弦相似度衡量两个向量的方向差异，等于点积除以两个模长的乘积。",
    "sorted 函数的 key 参数接受一个函数，用来指定排序依据，reverse=True 表示降序。",
    "运算符重载通过 __add__、__mul__ 等双下划线方法实现，让自定义类支持加减乘除。",
    "词袋模型忽略词序，只统计每个词出现的次数，把文本变成定长的数字向量。",
    "enumerate 可以在遍历列表时同时拿到下标和元素，zip 可以同时遍历多个列表。",
]


def tokenize(text):
    """中文按单字，英文按单词。中文那部分不能加 + ，加了会粘成一整块。"""
    return re.findall(r"[a-zA-Z]+|[\u4e00-\u9fff]", text)


def build_vocab(docs):
    vocab = {}
    for doc in docs:
        for w in tokenize(doc):
            if w not in vocab:
                vocab[w] = len(vocab)
    return vocab


vocab = build_vocab(DOCS)
print("词表大小:", len(vocab))       # 应该还是 139

# %%
def vectorize_py(tokens, vocab):
    """你手写的版本：普通 list"""
    vec = [0] * len(vocab)
    for w in tokens:
        if w in vocab:
            vec[vocab[w]] += 1
    return vec


def vectorize_torch(tokens, vocab):
    """torch 版本：同样的逻辑，容器换成张量"""
    vec = torch.zeros(len(vocab))
    for w in tokens:
        if w in vocab:
            vec[vocab[w]] += 1
    return vec


def cosine_py(a, b):
    """你手写的余弦"""
    n = sum(i * j for i, j in zip(a, b))
    x = math.sqrt(sum(i * i for i in a)) or 1
    y = math.sqrt(sum(j * j for j in b)) or 1
    return n / (x * y)


def cosine_torch(a, b):
    """torch 版余弦 —— 一行"""
    return torch.dot(a, b) / (a.norm() * b.norm())


# %%
q = "怎么给字典设置默认值"
qv_py = vectorize_py(tokenize(q), vocab)
qv_t = vectorize_torch(tokenize(q), vocab)

rows = []
for i, doc in enumerate(DOCS):
    s_py = cosine_py(qv_py, vectorize_py(tokenize(doc), vocab))
    s_t = float(cosine_torch(qv_t, vectorize_torch(tokenize(doc), vocab)))
    rows.append((s_t, i, s_py, doc))

for s_t, i, s_py, doc in sorted(rows, reverse=True)[:3]:
    print(f"torch={s_t:.4f}  手写={s_py:.4f}  第{i}篇  {doc[:22]}")

# 前三行 torch 和手写的数必须完全一致，第一条应该是第 1 篇（setdefault 那句），约 0.423

# %% [markdown]
# ### 进阶：一次算完 8 篇（torch 真正的用处在这）
#
# 把 8 篇的向量堆成一个矩阵（8 行 × 139 列），问句是 1 个向量（139）。
# **一次矩阵乘法就把 8 个相似度全算出来，不需要 for 循环。**
#
# 这就是「向量化」——你的 Python 循环是一次算一个，torch 是一次算一整批。

# %%
M = torch.stack([vectorize_torch(tokenize(d), vocab) for d in DOCS])
print("矩阵形状:", M.shape)          # → torch.Size([8, 139])

qvec = vectorize_torch(tokenize(q), vocab)

dots = M @ qvec                       # 矩阵 × 向量 → 8 个点积，一次算完
norms = M.norm(dim=1) * qvec.norm()   # dim=1 = 按行算范数
sims = dots / norms

print("8 篇相似度:", sims)
print("最高分是第", int(sims.argmax()), "篇，分数", round(float(sims.max()), 4))

# %%
# 别忘了除零：如果问句一个字都没命中，qvec 全是 0，norm 就是 0
qvec_zero = vectorize_torch(tokenize("zzz"), vocab)
print("zzz 的范数:", float(qvec_zero.norm()))    # → 0.0
# 这时候直接除会炸。torch 的做法：
safe = torch.where(norms == 0, torch.ones_like(norms), norms)
print("加保护后:", dots / safe)
