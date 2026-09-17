# CS50P / Python 知识点汇总（语法 · 函数 · 结构速查）

> 配合《CS50P-分集笔记-含习题.md》使用。这份是**按知识点**组织的速查，不按视频顺序。
> 覆盖 CS50P 全 10 讲涉及的所有语法、内置函数、数据结构、标准库与第三方库。

---

## 1. 基础语法

**注释与文档**

```python
# 单行注释
"""多行字符串也常当注释用（其实是字符串字面量，放在函数/类开头就是 docstring）"""
```

**变量与命名**：字母数字下划线，不能以数字开头；变量 `snake_case`，常量 `ALL_CAPS`，类 `PascalCase`。

**多行赋值 / 交换**

```python
a, b = 1, 2
a, b = b, a
x = y = 0
```

**海象运算符（3.8+）**

```python
if (n := len(items)) > 3:
    print(f"too many: {n}")
```

**运算符**

- 算术：`+ - * / // % **`
- 比较：`== != < <= > >=`
- 逻辑：`and or not`（短路求值）
- 身份：`is`（是不是同一个对象）vs `==`（值是否相等）
- 成员：`in` / `not in`
- 链式比较：`1 < x < 10`

**输出与输入**

```python
print(a, b, sep=", ", end="\n")
s = input("prompt: ")      # 永远返回 str
```

---

## 2. 字符串 str

**创建与转义**

```python
s = 'abc'  ;  s = "abc"  ;  s = """跨行
字符串"""
s = "He said \"hi\""       # 转义
s = r"C:\new\test"         # 原始字符串，反斜杠不转义（正则必用）
```

**索引与切片**：`s[0]`、`s[-1]`、`s[1:4]`、`s[:3]`、`s[3:]`、`s[::2]`、`s[::-1]`。字符串**不可变**，`s[0] = "x"` 会报错。

**常用方法**

- 大小写：`lower()` `upper()` `capitalize()` `title()` `swapcase()` `casefold()`
- 去空白：`strip()` `lstrip()` `rstrip()`（可按字符集：`strip("$.,")`）
- 查找：`find()` `index()` `count()` `startswith()` `endswith()` `in`
- 替换：`replace(a, b)` `removeprefix(x)` `removesuffix(x)`（后两个 3.9+）
- 拆分合并：`split(sep)` `rsplit(sep, 1)` `splitlines()` `"sep".join(list)`
- 判断：`isalpha()` `isdigit()` `isnumeric()` `isalnum()` `isupper()` `islower()` `isspace()`
- 对齐填充：`ljust()` `rjust()` `center()` `zfill(2)`（补零）

**格式化（f-string 优先）**

```python
f"{name}"              # 直接嵌入
f"{x:.2f}"             # 2 位小数
f"{x:,.2f}"            # 千分位 + 2 位小数
f"{x:>10}"             # 右对齐宽 10
f"{x:<10}"             # 左对齐
f"{x:^10}"             # 居中
f"{x:04d}"             # 整数补零到 4 位
f"{pct:.0%}"           # 百分比
```

---

## 3. 数值与数学

```python
int("42")        float("3.14")        str(42)
round(1.234, 2)  abs(-5)              pow(2, 10)    # 或 2 ** 10
max(a, b, c)     min(...)             sum([1, 2, 3])
divmod(7, 3)     # (2, 1)
```

浮点陷阱：`0.1 + 0.2 == 0.3` 是 `False`。比大小用 `math.isclose(a, b)`，算钱用「分」为单位的整数。

`math` 模块：`math.floor` `math.ceil` `math.sqrt` `math.pi` `math.inf` `math.isnan`。

---

## 4. 数据结构：list / tuple / dict / set

**list（有序、可变）**

```python
l = [1, 2, 3]
l.append(x)        # 末尾追加
l.insert(0, x)     # 指定位置插入
l.extend(other)    # 合并另一个可迭代对象
l.remove(x)        # 按值删（不存在抛 ValueError）
l.pop()            # 弹出末尾（或 l.pop(0)）
l.index(x)         # 找下标
l.count(x)
l.sort()           # 原地排序（返回 None）
sorted(l)          # 返回新列表
len(l)   x in l   l[1:3]   l + [4]   l * 2
del l[0]
```

**tuple（有序、不可变）**：`t = (1, 2)`，单元素要写 `(1,)`。用于「不会被改的数据」和函数多返回值。

**dict（键值对，3.7+ 保序）**

```python
d = {"a": 1}
d["b"] = 2               # 新增/修改
d.get("c", 0)            # 取不到给默认值，不抛 KeyError
d.setdefault("c", 0)     # 取不到就写入默认值
d.pop("a")               # 删除并返回值
d.keys()  d.values()  d.items()
"a" in d                 # 判断键
del d["a"]
d.update(other)          # 合并
{k: v for k, v in d.items() if v > 0}    # 字典推导
```

计数惯用法：`counts[x] = counts.get(x, 0) + 1`，或者 `collections.Counter(items)`。

**set（无序、去重）**

```python
s = {1, 2, 3}
s.add(x)   s.remove(x)   s.discard(x)   # discard 不存在不报错
s1 | s2    # 并集
s1 & s2    # 交集
s1 - s2    # 差集
s1 ^ s2    # 对称差集
```

**排序的 key 参数**

```python
sorted(words, key=len)                       # 按长度
sorted(rows, key=lambda r: r["name"])        # 按字典某列
sorted(words, key=str.lower)                 # 忽略大小写
sorted(items, reverse=True)                  # 降序
```

**拷贝陷阱**：`b = a` 是同一对象的两个名字；浅拷贝用 `a.copy()` 或 `a[:]`（二维结构仍共享内层）；深拷贝 `import copy; copy.deepcopy(a)`。

---

## 5. 控制流

```python
if cond:
    ...
elif cond2:
    ...
else:
    ...

while cond:
    ...
    break        # 跳出整个循环
    continue     # 跳过本轮剩余
else:            # 循环没被 break 打断时执行（少见但要知道）

for x in iterable:
    ...

for i in range(3):          # 0,1,2
for i in range(1, 4):       # 1,2,3
for i in range(0, 10, 2):   # 0,2,4,6,8
```

`match`（3.10+，新版补充）：

```python
match command:
    case "quit":
        print("bye")
    case "add" | "new":
        print("adding")
    case _:
        print("unknown")
```

推导式：

```python
[x * 2 for x in range(5)]
[x for x in range(10) if x % 2 == 0]
{w: len(w) for w in words}
{w.lower() for w in words}
```

---

## 6. 函数

```python
def greet(name: str, greeting: str = "hello") -> str:   # 默认参数 + 类型注解
    """Say hello to someone."""                          # docstring
    return f"{greeting}, {name}"


greet("David")
greet(name="David", greeting="hi")     # 关键字参数
```

**参数解包**

```python
def f(*args, **kwargs):    # args → tuple；kwargs → dict
    ...

f(1, 2, name="x")          # args=(1,2), kwargs={'name':'x'}
f(*[1, 2], **{"k": 3})     # 调用端解包
```

**作用域**：函数内读全局变量没问题，要修改必须 `global x`（嵌套函数用 `nonlocal`）。

**lambda（匿名函数）**：`lambda x: x * 2`，只能写一个表达式，常配合 `sorted(key=)`、`map`、`filter`。

**高阶函数**

```python
list(map(str.upper, words))
list(filter(lambda x: x > 0, nums))
from functools import reduce
```

**生成器**：含 `yield` 的函数，逐个产出、不一次性占内存。

```python
def gen(n):
    for i in range(n):
        yield i * i
```

**主函数惯例（CS50P 硬性要求）**

```python
def main():
    ...


if __name__ == "__main__":
    main()
```

---

## 7. 异常

**常见内置异常**：`ValueError`、`TypeError`、`ZeroDivisionError`、`NameError`、`IndexError`、`KeyError`、`FileNotFoundError`、`EOFError`、`AttributeError`、`ImportError`。

```python
try:
    n = int(input())
except ValueError:
    print("not a number")
except (TypeError, ZeroDivisionError) as e:
    print(e)
else:
    print("no exception")     # 只有没抛异常才走
finally:
    print("always")           # 无论怎样都走，用于收尾（关闭文件等）

raise ValueError("bad input")     # 主动抛
raise                             # 在 except 里重新抛出当前异常
pass                              # 空语句占位
```

自定义异常（L8）：

```python
class MyError(Exception):
    pass
```

输入校验的标准套路：

```python
while True:
    try:
        n = int(input("n: "))
        if n <= 0:
            continue
    except ValueError:
        continue
    break
```

---

## 8. 文件与 CSV

```python
with open("f.txt", "r", encoding="utf-8") as f:   # with 自动关闭，永远用它
    for line in f:            # 逐行（推荐）
        print(line.rstrip())  # 去掉行尾 \n
    # f.read()      一次读完
    # f.readline()  读一行
    # f.readlines() 读成列表

with open("out.txt", "w") as f:    # w 清空写；a 追加；r+ 读写
    f.write("hello\n")
```

模式：`r`（默认）、`w`（**清空**）、`a`、`x`（不存在才创建）、`b` 后缀（二进制）。

**CSV**

```python
import csv

with open("in.csv", newline="") as f:
    reader = csv.DictReader(f)                 # 每行 dict，键是表头
    rows = list(reader)

with open("in.csv") as f:
    rows = list(csv.reader(f))                 # 每行 list

with open("out.csv", "w", newline="") as f:    # newline="" 必写
    writer = csv.DictWriter(f, fieldnames=["first", "last"])
    writer.writeheader()
    writer.writerow({"first": "A", "last": "B"})
```

**JSON**

```python
import json
json.dump(obj, f)        # 写
data = json.load(f)      # 读文件
s = json.dumps(obj)      # 转成字符串
obj = json.loads(s)      # 从字符串解析
```

**os / pathlib（常用）**

```python
import os
os.path.exists(p)      os.path.basename(p)     os.path.splitext(p)[1]   # 扩展名
os.listdir(d)          os.remove(p)
```

---

## 9. 正则表达式

```python
import re

re.search(p, s)     # 找第一个，返回 Match 或 None
re.match(p, s)      # 只从开头
re.fullmatch(p, s)  # 整串匹配（做校验首选）
re.findall(p, s)    # 所有匹配 → list
re.finditer(p, s)   # 迭代器
re.sub(p, r, s)     # 替换
re.split(p, s)      # 分割
m.group(0) / m.group(1)          # 整串 / 第 1 个分组
re.IGNORECASE  re.MULTILINE  re.DOTALL     # 修饰符
```

元字符速查：

| 符号 | 含义 |
|---|---|
| `.` | 任意字符（不含换行，除非 DOTALL） |
| `^` `$` | 串首 / 串尾 |
| `*` `+` `?` | 0+ / 1+ / 0 或 1 |
| `{m}` `{m,n}` | 精确 m 次 / m 到 n 次 |
| `[]` `[^]` | 字符集合 / 取反 |
| `\d` `\D` | 数字 / 非数字 |
| `\w` `\W` | 单词字符 `[A-Za-z0-9_]` / 取反 |
| `\s` `\S` | 空白 / 非空白 |
| `\b` | 单词边界 |
| `\|` | 或 |
| `()` `(?:)` | 捕获分组 / 非捕获分组 |
| `(?P<n>...)` | 命名分组 |

常用模式：

```python
r"^\d{3}-\d{4}$"                          # 电话
r"^[\w.+-]+@[\w-]+\.[\w.]+$"              # 邮箱（简化版）
r"^(?:25[0-5]|2[0-4]\d|1?\d?\d)$"         # 0-255（IP 段）
r"\bum\b"                                 # 单词 um
r"^(?:https?://)?(?:www\.)?youtube\.com/embed/([\w-]+)$"
```

---

## 10. 面向对象

```python
class Jar:
    class_var = 0                  # 类变量，所有实例共享

    def __init__(self, capacity=12):        # 构造器
        self._capacity = capacity            # 实例属性；_ 前缀表示「内部用」
        self._size = 0

    def __str__(self):                      # print(obj) / str(obj)
        return f"Jar({self._size})"

    def __repr__(self):                     # 调试显示
        return f"Jar(capacity={self._capacity})"

    def __len__(self):                      # len(obj)
        return self._size

    def __eq__(self, other):                # obj == other
        return self._size == other._size

    def __add__(self, other):               # obj + other
        ...

    @property
    def size(self):                         # 像属性一样读：jar.size
        return self._size

    @size.setter
    def size(self, n):                      # 赋值时校验：jar.size = 5
        if n < 0:
            raise ValueError
        self._size = n

    @classmethod
    def from_dict(cls, d):                  # 工厂方法，参数是 cls
        return cls(d["capacity"])

    @staticmethod
    def help():                             # 不碰实例和类
        return "I am a jar"
```

继承：

```python
class Wizard(Student):
    def __init__(self, name, house, pet):
        super().__init__(name, house)       # 调父类构造
        self.pet = pet

    def __str__(self):                      # 重写父类方法
        return f"{super().__str__()} with {self.pet}"
```

常用魔术方法：`__str__` `__repr__` `__len__` `__eq__` `__lt__` `__add__` `__getitem__` `__contains__` `__iter__`。

---

## 11. 标准库（CS50P 用到的）

```python
import random
random.randint(1, 10)        # 含两端
random.choice(seq)           # 随机选一个
random.shuffle(lst)          # 原地打乱
random.random()              # [0,1)
random.seed(42)              # 固定随机序列（复现用）

import statistics
statistics.mean / median / mode / stdev / variance

import sys
sys.argv                     # 命令行参数列表，[0] 是脚本名
sys.exit("msg")              # 带消息退出
sys.exit(1)                  # 非 0 表示异常退出

from datetime import date, datetime, timedelta
date.today()
date.fromisoformat("2000-01-01")
(date.today() - birth).days

import collections
collections.Counter(items)       # 计数
collections.defaultdict(int)     # 默认值的 dict
collections.namedtuple

import itertools
itertools.chain / combinations / permutations

import os, csv, json, math, re, sys, statistics, random
```

`argparse`（新版补充）：

```python
import argparse

p = argparse.ArgumentParser(description="do something")
p.add_argument("name")                              # 位置参数
p.add_argument("-n", "--number", type=int, default=1)
p.add_argument("-v", "--verbose", action="store_true")
args = p.parse_args()
```

---

## 12. 第三方库（pip install）

```bash
pip install cs50 pytest requests emoji pyfiglet inflect tabulate Pillow fpdf2 validators
```

| 库 | 用途 | 典型调用 |
|---|---|---|
| `pytest` | 单元测试 | `pytest test_x.py` |
| `emoji` | emoji 转换 | `emoji.emojize(s, language="alias")` |
| `pyfiglet` | ASCII 艺术字 | `Figlet().renderText(s)` / `getFonts()` / `setFont(font=)` |
| `inflect` | 英文数字转词、列表拼接 | `p.number_to_words(n, andword="")` / `p.join(names)` |
| `tabulate` | 表格输出 | `tabulate(rows, headers=h, tablefmt="grid")` |
| `Pillow` | 图像处理 | `Image.open` / `ImageOps.fit(img, size)` / `img.paste` |
| `fpdf2` | 生成 PDF | `FPDF(orientation="P", unit="mm", format="A4")` → `add_page` `set_font` `cell` `image` `output` |
| `requests` | HTTP 请求 | `requests.get(url, headers=...)` → `.json()` |
| `validators` | 数据校验 | `validators.email(s)` |
| `cs50` | 官方辅助库 | `get_string` `get_int` `SQL`（云端环境才有） |

---

## 13. 代码风格与常见陷阱

**风格（PEP 8 精简版）**

- 缩进 4 空格，不用 Tab。
- 运算符两侧空格，逗号后空格，冒号后不空格（`f"{x}"` 里不加空格）。
- 行宽建议 ≤ 79（实际 100 也行，保持统一）。
- 常量全大写，变量名有意义，别用 `l` `O` 这种易混的单字母。
- 顶层定义之间空两行，方法之间空一行。

**Pythonic 写法**

```python
# 别这么写
if n % 2 == 0:
    return True
else:
    return False

# 这么写
return n % 2 == 0

# 别这么写
i = 0
for i in range(len(lst)):
    print(lst[i])

# 这么写
for item in lst:
    print(item)

# 需要索引时
for i, item in enumerate(lst):
    print(i, item)
```

**十大陷阱**

1. `input()` 返回 str，算数前必须转 `int()` / `float()`。
2. 可变默认参数：`def f(items=[])` 的列表会被多次调用共享 → 用 `None`。
3. `is` 和 `==` 混用：`is` 比身份，字符串数字比较一律用 `==`。
4. `sorted()` 返回新列表，`list.sort()` 返回 `None`，别写 `x = l.sort()`。
5. 循环里改列表长度会漏元素 → 遍历副本 `for x in l[:]`。
6. `open(path, "w")` 立即清空文件。
7. `strip()` 是按字符集删，不是删子串。
8. 写 CSV 忘了 `newline=""` → 每行之间多空行。
9. 正则忘了加 `r` 前缀 → `\b` `\d` 被 Python 转义吃掉。
10. 被测模块没有 `if __name__ == "__main__":` 守卫 → pytest 一 import 就卡在等输入。

---

## 14. 速查：一行流的常用写法

```python
# 读入多行直到 Ctrl-D
lines = []
while True:
    try:
        lines.append(input())
    except EOFError:
        break

# 计数
counts[x] = counts.get(x, 0) + 1

# 去重保序
list(dict.fromkeys(items))

# 字典按键排序输出
for k in sorted(d):
    print(k, d[k])

# 反转字符串 / 列表
s[::-1]

# 读文件去空行去注释
[l.strip() for l in open(f) if l.strip() and not l.strip().startswith("#")]

# 安全取嵌套值
d.get("a", {}).get("b")

# 三元表达式
"yes" if flag else "no"

# 多值比较
if x in (1, 2, 3):
```

---

## 15. 工具命令

```bash
python xxx.py                    # 运行
python -m pytest test_x.py       # 跑测试（等价于 pytest test_x.py）
python -m pip install 包名        # 装包
python -m pip freeze > requirements.txt
python -c "print(1)"             # 单行执行
check50 cs50/problems/2022/python/indoor     # 官方自测（云端）
submit50 cs50/problems/2022/python/indoor    # 官方提交（云端）
```

Windows 本机注意：终端里结束输入用 **Ctrl-Z 然后回车**（不是 Ctrl-D）；激活虚拟环境用 `D:\llm-journey\.venv\Scripts\activate`，或直接 `D:\llm-journey\.venv\Scripts\python.exe xxx.py`。
