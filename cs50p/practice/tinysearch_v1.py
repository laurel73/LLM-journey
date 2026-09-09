"""TinySearch v1 —— 今晚跑通的版本（Step 1~3 + main）

用法：python tinysearch_v1.py，然后输入一句问句。
这份是「先跑通」的版本，Step 4 的 class 包装留到明天。
"""

import re
import math


# ---------------------------------------------------------------- 语料

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


# ---------------------------------------------------------------- 主体

def main():
    # 1. 建词表：{词: 序号}
    vocab = build_vocab(DOCS)

    # 2. 把 8 篇文档各算成一个向量，存进 vecs
    vecs = []
    for doc in DOCS:
        vecs.append(vectorize(tokenize(doc), vocab))

    # 3. 把问句也算成一个向量
    q = input('想查什么？')
    qv = vectorize(tokenize(q), vocab)

    # 4. 跟每篇比一次，存成 (分数, 原文)
    result = []
    for i, v in enumerate(vecs):
        result.append((cosine(qv, v), DOCS[i]))

    # 5. 按分数降序，打印前 3 条
    for score, text in sorted(result, key=lambda t: t[0], reverse=True)[:3]:
        print(round(score, 3), text)


# ---------------------------------------------------------------- 四个零件

def tokenize(text):
    """把文本切成词的列表：英文按单词，中文按单字。"""
    return re.findall(r"[a-zA-Z]+|[\u4e00-\u9fff]", text)


def build_vocab(docs):
    """遍历所有文档的所有词，返回一个 {词: 序号} 字典，序号从 0 连续递增。"""
    vocab = {}
    for doc in docs:
        for w in tokenize(doc):
            if w not in vocab:
                vocab[w] = len(vocab)
    return vocab


def vectorize(doc_tokens, vocab):
    """把一串词变成词袋向量：长度 == len(vocab)，第 i 位是第 i 个词出现几次。"""
    vec = [0] * len(vocab)
    for w in doc_tokens:
        if w in vocab:
            vec[vocab[w]] += 1
    return vec


def cosine(a, b):
    """两个向量的余弦相似度 = 点积 / (|a| * |b|)。零向量当模长 1 处理。"""
    n = sum(x * y for x, y in zip(a, b))
    i = math.sqrt(sum(x * x for x in a))
    j = math.sqrt(sum(y * y for y in b))
    if i == 0:
        i = 1
    if j == 0:
        j = 1
    return n / (i * j)


if __name__ == "__main__":
    main()
