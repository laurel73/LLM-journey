# Python 结课自测：TinySearch —— 一个能跑起来的本地笔记检索器

> 定位：CS50P 全部课程看完后的**收尾小作业**，2–3 天，纯标准库，手机上能跑。
> 目的只有一个：**把 dict / list / class 用熟**。不是做项目，是练手感。
> 做完它，再去读 d2l 第 2 章；它是 AskMyDocs（Final Project）的第 0 周。

---

## 零、三条硬规矩（针对手机环境定的，别违反）

1. **不许一次写完再跑。** 每个 Step 写完立刻运行、看到输出，才准进下一个 Step。
   你 Week 8 那题烂尾，根因就是「写了 100 行最后才跑，跑不动就放弃了」。
2. **不许用任何第三方库。** 只用 `math` / `re` / `json` / `argparse`（都是 Python 自带）。
   手机上装不了 Pillow、numpy，装不上的东西一律不许出现在代码里。
3. **语料直接写死在代码里。** 一个 `DOCS = [...]` 列表就够了，别去读写外部文件。
   手机文件管理是痛点，这个作业刻意绕开它。

最终代码量：**120–150 行**。超过 200 行说明你写复杂了。

---

## 语料（直接复制，8 段）

```python
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
```

---

## Step 1 · 分词与词表（练 dict）

写两个函数：

```python
def tokenize(text):        # 切成词的列表
def build_vocab(docs):     # 返回 {"词": 序号} 的字典
```

- `tokenize`：中文按**单字**切最简单（直接 `list(text)`），英文单词按空格切。
  最省事的做法：用 `re.findall(r"[a-zA-Z]+|[一-龥]", text)`，中英文都能切。
  **这一步不是练习重点，直接用这个正则就行。**
- `build_vocab`：遍历所有文档的所有词，没见过的分配一个新序号。
  提示：用 `if w not in vocab: vocab[w] = len(vocab)`，比 `setdefault` 更直观。

**跑起来应该看到：**
```
词表大小：137
前 20 个词：['列', '表', '推', '导', '式', ...]
```

---

## Step 2 · 词袋向量（练 list + dict 联动）

```python
def vectorize(doc_tokens, vocab) -> list[int]:
```

返回一个长度等于 `len(vocab)` 的列表，第 i 位是这个文档里第 i 个词出现的次数。

- 提示：先 `vec = [0] * len(vocab)`，再对每个词 `vec[vocab[w]] += 1`
- 这一步会让你真切感受到「dict 负责查编号，list 负责存数值」是怎么配合的

**跑起来应该看到：**
```
第 0 篇向量长度：137，非零位：23 个
非零的前 10 个：(词, 次数) = [('列', 2), ('表', 2), ('推', 1), ...]
```

---

## Step 3 · 余弦相似度（练 list 运算，不许用 numpy）

```python
def cosine(a: list, b: list) -> float:
```

公式：`点积 / (|a| * |b|)`

- 点积：`sum(x * y for x, y in zip(a, b))`
- 模长：`math.sqrt(sum(x * x for x in a))`
- 注意分母可能为 0，要处理

**跑起来应该看到（这一步最能自查对错）：**
```
自己和自己：1.0
第 0 篇 vs 第 1 篇：0.18      （两篇都讲 list/dict，应该偏高）
第 0 篇 vs 第 6 篇：0.05      （讲词袋，应该偏低）
```
**如果「自己 vs 自己」不是 1.0，说明算错了，别往下走。**

---

## Step 4 · 封装成 class（这一步是重点）

把前面散着的函数收进类里：

```python
class Vec:
    def __init__(self, values):        # 存 list
    def __add__(self, other):          # 逐元素相加，返回新 Vec
    def dot(self, other):              # 点积，返回 float
    def norm(self):                    # 模长，返回 float
    def __repr__(self):                # 打印成 Vec([...]) 或 Vec(137维)

class Doc:
    def __init__(self, doc_id, text):  # 存原文
    def tokens(self):                  # 分词结果
    def vector(self, vocab):           # 返回 Vec
```

- `Vec.__add__` 用列表推导：`Vec([x + y for x, y in zip(...)])`
- 写完后把 Step 3 的 `cosine` 改成接受两个 `Vec`：`a.dot(b) / (a.norm() * b.norm())`
- **`__repr__` 一定要写**，否则你打印对象时看到的是 `<__main__.Vec object at 0x...>`，
  在手机上没有任何调试价值

**跑起来应该看到：**
```
v = Vec([1, 2, 3])
print(v)              # Vec([1, 2, 3])
print(v + v)          # Vec([2, 4, 6])
print(v.dot(v))       # 14
print(v.norm())       # 3.7416573867739413
```

---

## Step 5 · 检索器（把 dict / list / class 串起来）

```python
class TinySearch:
    def __init__(self, docs):          # docs 是字符串列表
    def build(self):                   # 建词表 + 给每篇算向量
    def query(self, q, k=3):           # 返回 top-k：(分数, 原文) 的列表
```

- `build` 里要存：词表（dict）、每篇的 Vec（list 或 dict）
- `query`：把问句也 `vectorize` 成 Vec，跟每篇算余弦，排序取前 k
- 排序用 `sorted(..., key=lambda t: t[0], reverse=True)`

**跑起来应该看到（这是整个作业最爽的一刻）：**
```
>>> s = TinySearch(DOCS); s.build()
>>> for score, text in s.query("怎么给字典设置默认值"):
...     print(round(score, 3), text)

0.289 字典的 setdefault 方法可以在键不存在时插入默认值，常用于分组统计。
0.134 类是对象的模板，__init__ 方法在实例化时自动调用，self 指向实例自己。
0.098 sorted 函数的 key 参数接受一个函数，用来指定排序依据，reverse=True 表示降序。
```

**问句里没出现过的词怎么处理？** 这是必踩的坑：`vocab[w]` 会 `KeyError`。
正确做法是查不到就跳过（`if w in vocab`）。别用 try/except 糊过去。

---

## Step 6 · 加分项（选做，做不完不影响结课）

- 用 `json` 把索引存盘、下次启动时加载（练文件 I/O + dict 序列化）
- 加 `if __name__ == "__main__":` 和一个 `argparse` 命令行，支持 `python tinysearch.py "问句"`
- 加一个简单的 `while True` 交互循环，能连续问

---

## 验收清单（8 条，每条都能立刻验证）

- [ ] `tokenize` 对中英文混合文本都能切出词
- [ ] `build_vocab` 返回 dict，词不重复，序号从 0 连续
- [ ] `vectorize` 返回的列表长度 == `len(vocab)`
- [ ] `cosine(v, v)` 精确等于 `1.0`
- [ ] `Vec` 类有 `__init__` / `__add__` / `dot` / `norm` / `__repr__` 五个方法
- [ ] `Doc` 类有 `__init__` / `tokens` / `vector`
- [ ] `TinySearch.query("运算符重载")` 的第一条是第 5 篇（讲 `__add__` 那篇）
- [ ] 问一个词表里完全没有的词（比如 `"zzz"`）不报错，返回空或全 0

**最后一条最容易漏，也最值钱**——它考的是你有没有想过「查不到怎么办」。

---

## 常见坑（提前说，免得你卡住）

1. **`__repr__` 忘了写** → 打印对象全是内存地址，手机上调试全瞎
2. **`self` 漏写** → `TypeError: __init__() takes 1 positional argument but 2 were given`
3. **`[0] * n` 的浅拷贝陷阱** → 一维列表没问题，二维千万别用 `[[0]*n]*m`
4. **分母为 0** → 两个零向量算余弦会 `ZeroDivisionError`
5. **中文标点没过滤** → 词表里全是「，」「。」，拉低相似度。可以在 `tokenize` 里只保留字母和汉字

---

## 做完之后

- 你的 `cosine` 就是 d2l 第 2 章讲的**向量点积 + 归一化**，到时候看到 `torch` 的写法会有「哦就是这个」的感觉
- 你的 `TinySearch.query` 不用改一行，把「词频向量」换成「embedding 向量」就是 **AskMyDocs** 的核心检索 —— 那时你已经有信心了
