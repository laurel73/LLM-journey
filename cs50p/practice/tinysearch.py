"""TinySearch —— Python 结课自测作业（骨架）

用法：把每个 TODO 填完，每填完一个 Step 就运行一次看输出。
配套说明见同目录的《结课自测-TinySearch.md》。

运行：python tinysearch.py
"""

import math
import re


# ---------------------------------------------------------------- 语料（已给，不用改）

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


# ---------------------------------------------------------------- Step 1

def tokenize(text: str) -> list[str]:
    """把文本切成词的列表（中文按单字，英文按单词）。

    提示：re.findall(r"[a-zA-Z]+|[一-龥]", text)
    """
    # TODO
    ...


def build_vocab(docs: list[str]) -> dict[str, int]:
    """遍历所有文档，建立 {词: 序号} 的字典，序号从 0 连续递增。

    提示：if w not in vocab: vocab[w] = len(vocab)
    """
    # TODO
    ...


# ---------------------------------------------------------------- Step 2

def vectorize(tokens: list[str], vocab: dict[str, int]) -> list[int]:
    """把一串词变成词袋向量：长度 == len(vocab)，第 i 位是第 i 个词出现的次数。

    提示：vec = [0] * len(vocab)，然后 vec[vocab[w]] += 1
    注意：vocab 里没有的词要跳过，别让它 KeyError
    """
    # TODO
    ...


# ---------------------------------------------------------------- Step 3

def cosine(a: list, b: list) -> float:
    """两个列表的余弦相似度 = 点积 / (|a| * |b|)。

    提示：点积 sum(x*y for x, y in zip(a, b))，模长 math.sqrt(sum(x*x for x in a))
    注意：分母为 0 时返回 0.0
    """
    # TODO
    ...


# ---------------------------------------------------------------- Step 4

class Vec:
    """一个向量，内部存一个 list。"""

    def __init__(self, values: list):
        # TODO: self.values = values
        ...

    def __add__(self, other: "Vec") -> "Vec":
        """逐元素相加，返回一个新 Vec（不要改自己）。"""
        # TODO
        ...

    def dot(self, other: "Vec") -> float:
        """点积，返回 float。"""
        # TODO
        ...

    def norm(self) -> float:
        """模长，返回 float。"""
        # TODO
        ...

    def __repr__(self) -> str:
        """打印成 Vec([1, 2, 3]) 这样，别让它输出内存地址。"""
        # TODO
        ...


class Doc:
    """一篇文档。"""

    def __init__(self, doc_id: int, text: str):
        # TODO
        ...

    def tokens(self) -> list[str]:
        """分词结果。"""
        # TODO
        ...

    def vector(self, vocab: dict[str, int]) -> Vec:
        """转成 Vec。"""
        # TODO
        ...


# ---------------------------------------------------------------- Step 5

class TinySearch:
    """迷你检索器：建索引 + 查询 top-k。"""

    def __init__(self, docs: list[str]):
        # TODO: 存文档，准备好后面要用的容器
        ...

    def build(self) -> None:
        """建词表，并给每篇文档算出向量存起来。"""
        # TODO
        ...

    def query(self, q: str, k: int = 3) -> list[tuple[float, str]]:
        """把问句也向量化，跟每篇算余弦，返回 [(分数, 原文), ...] 前 k 条。

        提示：sorted(结果, key=lambda t: t[0], reverse=True)[:k]
        """
        # TODO
        ...


# ---------------------------------------------------------------- 自检

def main() -> None:
    # --- Step 1
    print("== Step 1 词表 ==")
    vocab = build_vocab(DOCS)
    print("词表大小：", len(vocab))
    print("前 20 个词：", list(vocab)[:20])

    # --- Step 2
    print("\n== Step 2 词袋向量 ==")
    v0 = vectorize(tokenize(DOCS[0]), vocab)
    print("第 0 篇向量长度：", len(v0), "，非零位：", sum(1 for x in v0 if x))

    # --- Step 3
    print("\n== Step 3 余弦相似度 ==")
    print("自己和自己：", round(cosine(v0, v0), 6), "（必须是 1.0）")
    v1 = vectorize(tokenize(DOCS[1]), vocab)
    print("第0 vs 第1：", round(cosine(v0, v1), 3))
    v6 = vectorize(tokenize(DOCS[6]), vocab)
    print("第0 vs 第6：", round(cosine(v0, v6), 3))

    # --- Step 4
    print("\n== Step 4 Vec 类 ==")
    v = Vec([1, 2, 3])
    print("v        =", v)
    print("v + v    =", v + v)
    print("v.dot(v) =", v.dot(v), "（应该是 14）")
    print("v.norm() =", round(v.norm(), 4), "（应该是 3.7417）")

    # --- Step 5
    print("\n== Step 5 检索 ==")
    s = TinySearch(DOCS)
    s.build()
    for score, text in s.query("怎么给字典设置默认值"):
        print(round(score, 3), text)

    print("\n-- 边界：查一个词表里没有的词 --")
    for score, text in s.query("zzz"):
        print(round(score, 3), text)


if __name__ == "__main__":
    main()
