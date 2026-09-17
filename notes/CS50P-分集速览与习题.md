> ⚠️ 这份是**速览 + 习题专册**，不是详细课堂笔记。
> 完整课堂笔记（15.7 万字，含讲师现场演示、翻车现场、学生提问、每节视频时间标注）在 `notes/lectures/` 目录，按讲分文件，入口见 [lectures/README.md](lectures/README.md)。
> 本文件保留的价值：**41 道官方习题（PSet 0–8）逐题的考点、易错点与骨架代码**——学完一讲就来做对应那组题。

# CS50P 分集笔记（顺视频 + 课后习题融合版）

> 视频：BV1vkWbzSEUh《【高质量配音】哈佛大学 CS50P Python 编程入门 4K【已完结】》
> 来源：哈佛 CS50P（David J. Malan），官方站点 https://cs50.harvard.edu/python/
> 本笔记按视频分 P 顺序整理，每集末尾附「本讲习题」：题目要求 + 考点 + 易错点 + 最小骨架代码。

## 全集结构（11 个分 P，约 15 小时 54 分）

| 分 P | 内容 | 时长 |
|---|---|---|
| P1 | 课程简介 | 4:17 |
| P2 | Lecture 0 函数、变量 | 1:45:38 |
| P3 | Lecture 1 条件语句 | 56:08 |
| P4 | Lecture 2 循环语句 | 1:20:47 |
| P5 | Lecture 3 异常处理 | 44:36 |
| P6 | Lecture 4 函数库 | 1:17:29 |
| P7 | Lecture 5 单元测试 | 50:54 |
| P8 | Lecture 6 文件 I/O | 1:32:25 |
| P9 | Lecture 7 正则表达式 | 2:05:00 |
| P10 | Lecture 8 面向对象编程 | 2:47:41 |
| P11 | Lecture 9 其它内容 | 2:29:04 |

两条使用说明：

- 视频是 2022 年录制版，官网此后有微调（`match` 语句、`argparse`、部分题型都是后来加的）。笔记以**官网现行版**为准，属于新版补充的内容我都标了「新版补充」。
- 每讲对应一套 Problem Set（PSet 0 ~ PSet 8），第 9 讲之后是 Final Project，没有 PSet 9。你目前做到 PSet 5（单元测试）。

---

## P1 · 课程简介（4:17）

讲什么：CS50P 是 CS50 系列的 Python 版，面向零基础，10 讲 + 一个 Final Project。官方提供云端环境 `cs50.dev`（VS Code 网页版），作业用 `check50` 自测、`submit50` 提交，提交前需 GitHub 授权一次。

课程结构速记：函数与变量 → 条件 → 循环 → 异常 → 库 → 测试 → 文件 → 正则 → 面向对象 → 杂项。

**本讲配套**：无编程题，只有环境准备。你要做的三件事：

1. 用 GitHub 登录 cs50.dev，终端执行 `update50` 保证环境最新。
2. 学会基本终端命令：`cd`（回到家目录）、`mkdir xxx`、`cd xxx`、`ls`、`code xxx.py`、`python xxx.py`。
3. 本地路线（你自己用的）：`D:\llm-journey\.venv\Scripts\python.exe xxx.py`。官方的 `cs50` 库本地不一定有，遇到 `from cs50 import get_int` 的题目，用 `input()` + `try/except` 自己实现即可，判定标准看的是行为不是实现。

---

## P2 · Lecture 0 函数、变量（1:45:38）

### 核心内容

**输出与字符串**

```python
print("hello, world")
print("hello", "world", sep=", ", end="!")   # sep 分隔符，end 结尾（默认换行）
```

Python 里单引号双引号完全等价。字符串里要出现引号，有三种办法：换另一种引号包裹、用反斜杠转义 `\"`、用三引号 `"""..."""`（还能跨行）。

**变量与类型**

```python
name = "David"     # str
n = 28             # int
pi = 3.14          # float
ok = True          # bool（首字母必须大写）
```

Python 是动态类型：变量本身没类型，值才有类型。查看用 `type(x)`，转换用 `str() / int() / float() / bool()`。

**输入**

`input()` 永远返回 `str`，要算数必须 `int()` 转换。可以带提示语：`input("What's your name? ")`。

**字符串方法（第一梯队）**

```python
s.lower()  s.upper()  s.capitalize()  s.title()  s.strip()
s.lstrip()  s.rstrip()  s.replace("a", "b")  s.removeprefix("$")  # removeprefix 需 3.9+
```

`strip()` 是**按字符集**删除两端字符，不是删子串 —— `s.strip("$")` 会删掉两端所有 `$`，但 `"$5$$".strip("$")` 结果是 `"5"`，看着像删子串其实是逐字符删。想删固定前缀用 `removeprefix` 或切片。

**f-string（格式化字符串，最常用）**

```python
print(f"hello, {name}")            # 直接嵌变量
print(f"{x:.2f}")                  # 保留 2 位小数（会四舍五入）
print(f"{x:,}")                    # 千分位逗号
print(f"{x:>10}")                  # 右对齐，宽度 10
```

**数字**

`/` 永远得 float，`//` 整除，`**` 幂，`%` 取余。`round(x, n)` 四舍五入到 n 位。浮点有精度误差（`0.1 + 0.2 != 0.3`），涉及钱要小心，判等用误差范围或转整数分。

**自定义函数**

```python
def hello(to="world"):     # 默认参数
    return f"hello, {to}"   # 有 return 才能拿到结果；没有 return 的函数返回 None


def main():
    print(hello("David"))


if __name__ == "__main__":
    main()
```

两个必须记住的约定：

- `main()` + `if __name__ == "__main__":` —— 这个文件被 `import` 时不会自动执行 main，直接运行时才执行。**从 PSet 5（单元测试）开始这是硬性要求**，否则测试文件一 import 就卡在等待输入。
- 只让 `main()` 负责 `print`，业务逻辑放在有返回值的纯函数里。

### 本讲习题：Problem Set 0

**1. Indoor Voice（indoor.py）** —— 输入转小写输出。考点：`input()` 返回 str、`.lower()`。

```python
print(input().lower())
```

**2. Playback Speed（playback.py）** —— 把每个空格换成 `...`。考点：`.replace(" ", "...")`。

**3. Making Faces（faces.py）** —— 要求 `convert(s)` 把 `":)"` 换成 🙂、`":("` 换成 🙁，另有 `main()` 调用并打印。考点：函数拆分 + 字符串替换（`replace` 是从左到右依次执行，替换结果里若又出现被匹配的片段会被二次替换，本题不会，但要有这个意识）。

```python
def convert(s):
    return s.replace(":)", "🙂").replace(":(", "🙁")


def main():
    print(convert(input()))


if __name__ == "__main__":
    main()
```

**4. Einstein（einstein.py）** —— 输入质量（kg，int），输出能量 `E = m * c²`，c = 300000000。考点：`int(input())`、整数运算。

```python
m = int(input())
print(m * 300000000 ** 2)
```

**5. Tip Calculator（tip.py）** —— 补全 `dollars_to_float`（去掉 `$` 转 float）和 `percent_to_float`（去掉 `%` 转小数，如 `15%` → `0.15`），最后 `f"Leave ${tip:.2f}"`。考点：字符串清洗 + 类型转换 + 保留两位。

```python
def dollars_to_float(d):
    return float(d.removeprefix("$"))


def percent_to_float(p):
    return float(p.removeprefix("%")) / 100
```

**易错点**

- `int("3.5")` 会抛 `ValueError`，要先 `float()`。
- 大小写题别忘 `.lower()` 后再比较。
- 输出格式要一模一样，包括 `$`、空格、换行。

---

## P3 · Lecture 1 条件语句（56:08）

### 核心内容

```python
if x < 0:
    print("negative")
elif x == 0:
    print("zero")
else:
    print("positive")
```

- 缩进决定代码块（4 个空格是官方规范），**缩进错误是新手第一大坑**。
- 比较运算符：`== != < <= > >=`。`=` 是赋值，`==` 才是比较，别混。
- 逻辑运算：`and` / `or` / `not`。可以链式比较：`1 <= x <= 10`。
- `%` 取模判奇偶：`n % 2 == 0`。
- Pythonic 写法：

```python
# 不推荐
if n % 2 == 0:
    return True
else:
    return False

# 推荐：比较本身就是布尔值
return n % 2 == 0
```

- **新版补充 `match`**（Python 3.10+，2022 视频里没有）：

```python
match name:
    case "Harry" | "Hermione":
        print("Gryffindor")
    case _:
        print("Who?")
```

### 本讲习题：Problem Set 1

**1. Deep Thought（deep.py）** —— 输入 `42`、`forty-two`、`forty two`（不区分大小写）输出 `Yes`，否则 `No`。考点：先 `strip().lower()` 再判断，用 `in` 做多值匹配。

```python
s = input().strip().lower()
print("Yes" if s in ("42", "forty-two", "forty two") else "No")
```

**2. Home Federal Savings Bank（bank.py）** —— 问候语以 `hello` 开头 → `$0`；以 `h` 开头但不含 hello → `$20`；否则 `$100`。忽略首部空白、不区分大小写。考点：`startswith()`、判断顺序（hello 必须在 h 之前判）。

```python
g = input().strip().lower()
if g.startswith("hello"):
    print("$0")
elif g.startswith("h"):
    print("$20")
else:
    print("$100")
```

**3. File Extensions（extensions.py）** —— 按后缀输出 MIME 类型：`.gif .jpg .jpeg .png .pdf .txt .zip`，大小写不敏感；其它后缀或没有后缀 → `application/octet-stream`。考点：用 `rsplit(".", 1)` 取最后一段（而不是 `split(".")[-1]` 也行，但 `rsplit` 语义更准）、用 dict 做映射避免一长串 elif。

```python
types = {
    "gif": "image/gif", "jpg": "image/jpeg", "jpeg": "image/jpeg",
    "png": "image/png", "pdf": "application/pdf", "txt": "text/plain",
    "zip": "application/zip",
}
name = input().strip().lower()
ext = name.rsplit(".", 1)[-1] if "." in name else ""
print(types.get(ext, "application/octet-stream"))
```

**4. Math Interpreter（interpreter.py）** —— 输入 `x y z`（如 `1 + 1`），输出保留 1 位小数的结果。考点：`split()` 拆三份、运算符分支、`f"{r:.1f}"`。

```python
x, y, z = input().split(" ")
x, z = float(x), float(z)
if y == "+":
    r = x + z
elif y == "-":
    r = x - z
elif y == "*":
    r = x * z
elif y == "/":
    r = x / z
print(f"{r:.1f}")
```

**5. Meal Time（meal.py）** —— 输入 24 小时制时间，7:00–8:00 输出 `breakfast time`，12:00–13:00 `lunch time`，18:00–19:00 `dinner time`，其它不输出。要求写 `convert(time)` 把 `"7:30"` 转成 `7.5`。考点：字符串拆分 + 浮点比较。

```python
def convert(time):
    hours, minutes = time.split(":")
    return float(hours) + float(minutes) / 60


t = convert(input().strip())
if 7 <= t <= 8:
    print("breakfast time")
elif 12 <= t <= 13:
    print("lunch time")
elif 18 <= t <= 19:
    print("dinner time")
```

**易错点**

- 边界是否包含：题目说 inclusive，所以是 `<=` 不是 `<`。
- `strip()` 要在比较之前做，输入末尾带空格会直接判错。
- File Extensions 里 `.tar.gz` 这种要取 `gz`，用 `split(".")[1]` 会漏。

---

## P4 · Lecture 2 循环语句（1:20:47）

### 核心内容

```python
while True:                    # while 循环
    n = int(input("n? "))
    if n > 0:
        break                  # 跳出循环；continue 是跳过本轮

for i in range(3):             # 0,1,2
    print(i)

for c in "hello":              # 字符串可迭代
    print(c, end="")
```

**列表 list**

```python
names = []                     # 空列表
names.append("David")          # 追加
names += ["Carter"]            # 合并
len(names)                     # 长度
"David" in names               # 是否存在
names[0], names[-1]            # 索引，负数是倒数
names[1:3]                     # 切片（左闭右开）
sorted(names)                  # 返回新列表；names.sort() 原地排
```

**字典 dict**

```python
houses = {"Harry": "Gryffindor"}
houses["Hermione"] = "Gryffindor"      # 赋值即新增
houses.get("Ron", "Unknown")           # 取不到返回默认值，KeyError 更安全
for name, house in houses.items():     # 同时遍历键值
    print(name, house)
```

**Mario 砖块**：嵌套循环打印 `#`，理解「外层控制行、内层控制列」。

### 本讲习题：Problem Set 2

**1. camelCase（camel.py）** —— 把 `preferredFirstName` 转成 `preferred_first_name`。考点：逐字符遍历 + `isupper()` 判断 + 拼接。

```python
s = input()
out = ""
for c in s:
    if c.isupper():
        out += "_" + c.lower()
    else:
        out += c
print(out)
```

**2. Coke Machine（coke.py）** —— 一瓶 50 分，只收 25/10/5，每次告知 `Amount Due: x`，够了输出 `Change Owed: y`，非法面额忽略。考点：`while` 循环 + 状态变量。

```python
due = 50
while due > 0:
    coin = int(input("Insert Coin: "))
    if coin in (25, 10, 5):
        due -= coin
    print(f"Amount Due: {due}" if due > 0 else f"Change Owed: {-due}")
```

**3. Just setting up my twttr（twttr.py）** —— 去掉所有元音 AEIOU（大小写都去掉）。考点：字符串可迭代 + `in` 判断。

```python
s = input()
print("".join(c for c in s if c.lower() not in "aeiou"))
```

**4. Vanity Plates（plates.py）** —— 判断车牌是否合法，四条规则：长度 2–6；必须以两个字母开头；数字只能在末尾且第一个数字不能是 `0`；不能有标点空格（即 `s.isalnum()`）。考点：多条件拆分 + 字符串方法组合。

```python
def is_valid(s):
    if not (2 <= len(s) <= 6) or not s.isalnum():
        return False
    if not s[:2].isalpha():
        return False
    for i, c in enumerate(s):
        if c.isdigit():
            return c != "0" and s[i:].isdigit()   # 找到第一个数字：必须非 0 且后面全是数字
    return True
```

**5. Nutrition Facts（nutrition.py）** —— 输入水果名（不区分大小写），输出一份的热量；不在表里就忽略（不输出、继续问）。考点：**用 dict 查表代替 20 个 if**，循环直到 EOF。

```python
fruits = {"apple": 130, "avocado": 50, "banana": 110, "strawberries": 50, ...}
item = input().strip().lower()
if item in fruits:
    print(f"Calories: {fruits[item]}")
```

**易错点**

- Vanity Plates 里 `AAA22A` 必须判 False，靠「第一个数字之后必须全是数字」这条。
- Nutrition Facts 表里是 `strawberries`（复数），输入也是复数，别改成单数。
- `sorted(names)` 返回新列表，`names.sort()` 返回 `None`，别写 `x = names.sort()`。

---

## P5 · Lecture 3 异常处理（44:36）

### 核心内容

运行时错误（异常）类型，你要能认出来：

- `ValueError`：`int("abc")`
- `ZeroDivisionError`：除以 0
- `NameError`：用了没定义的变量
- `TypeError`：类型不匹配，如 `"a" + 1`
- `IndexError` / `KeyError`：列表越界 / 字典键不存在
- `EOFError`：`input()` 遇到 Ctrl-D（Ctrl-Z 在 Windows）

处理方式：

```python
while True:
    try:
        n = int(input("n? "))
    except ValueError:
        print("not a number")
    else:                      # 没抛异常才执行
        break
    # finally: 无论是否异常都执行，常用于收尾

pass                           # 占位符，什么都不做，用来满足语法要求
```

核心模式：**用 `try/except` 把「不合法输入」挡在循环里，重新问**。

### 本讲习题：Problem Set 3

**1. Fuel Gauge（fuel.py）** —— 输入 `X/Y`，输出百分比（四舍五入取整）；≤1% 输出 `E`，≥99% 输出 `F`；X/Y 非整数、X>Y 或 Y=0 时重新提示。考点：异常捕获 + `round()`。

```python
while True:
    try:
        x, y = input("Fraction: ").split("/")
        pct = round(int(x) / int(y) * 100)
        if int(x) > int(y):
            raise ValueError
    except (ValueError, ZeroDivisionError):
        pass
    else:
        break
print("E" if pct <= 1 else "F" if pct >= 99 else f"{pct}%")
```

**2. Felipe's Taqueria（taqueria.py）** —— 菜单 dict，逐行点单，Ctrl-D 结束，每次输入后打印累计金额 `f"Total: ${total:.2f}"`，忽略不在菜单上的项（大小写不敏感）。考点：EOFError + dict 累加。

```python
menu = {"Baja Taco": 4.25, "Burrito": 7.50, "Bowl": 8.50, ...}
total = 0.0
while True:
    try:
        item = input()
    except EOFError:
        print()
        break
    total += menu.get(item.strip().title(), 0)
    print(f"Total: ${total:.2f}")
```

**3. Grocery List（grocery.py）** —— 逐行输入，Ctrl-D 结束，按字母序输出「数量 + 大写的物品名」，大小写不敏感去重。考点：`EOFError` + dict 计数 + `sorted()`。

```python
counts = {}
while True:
    try:
        item = input().strip().upper()
    except EOFError:
        break
    counts[item] = counts.get(item, 0) + 1
for item in sorted(counts):
    print(f"{counts[item]} {item}")
```

**4. Outdated（outdated.py）** —— 输入 `9/8/1636` 或 `September 8, 1636`，输出 ISO 8601 `1636-09-08`。考点：两种输入格式的分支 + `zfill(2)` 补零 + 月份名列表查索引 + 非法输入重新提示（`ValueError` 或 `datetime` 都可以）。

```python
MONTHS = ["January", "February", ..., "December"]

if "/" in date:
    m, d, y = date.split("/")
    m, d, y = int(m), int(d), int(y)
else:
    month_name, rest = date.split(" ", 1)
    d, y = rest.replace(",", "").split(" ")
    m, d, y = MONTHS.index(month_name) + 1, int(d), int(y)

if not (1 <= m <= 12 and 1 <= d <= 31):
    raise ValueError
print(f"{y:04}-{m:02}-{d:02}")
```

**易错点**

- `except` 只捕获你列出的异常，写 `except:` 裸捕获会连 `KeyboardInterrupt` 一起吞掉，别这么写。
- Grocery List 里 Windows 终端 Ctrl-D 不可用，用 Ctrl-Z 后再回车（或 `python grocery.py < items.txt`）。
- Taqueria 大小写：`item.title()` 能把 `baja taco` 变成 `Baja Taco`。

---

## P6 · Lecture 4 函数库（1:17:29）

### 核心内容

**导入**

```python
import random                       # 用 random.randint(...)
from random import randint, choice  # 直接用 randint(...)
import statistics as stats          # 起别名
```

**random 模块**

```python
random.randint(1, 10)     # 含两端的整数
random.choice(["a", "b"]) # 随机选一个
random.shuffle(cards)     # 原地打乱
random.random()           # [0,1) 浮点
```

**statistics 模块**：`mean` / `median` / `mode` / `stdev` / `variance`。

**命令行参数**

```python
import sys
if len(sys.argv) != 2:
    sys.exit("Too few/many arguments")
print(sys.argv[1])        # sys.argv[0] 是脚本名本身
```

**切片 slice**

```python
s = "hello, world"
s[0:5]      # "hello"
s[:5]       # 同上
s[-5:]      # "world"
s[::2]      # 步长 2
s[::-1]     # 反转
```

**第三方包**：`pip install pyfiglet emoji inflect tabulate requests Pillow fpdf2 validators`。写 `requirements.txt` 记录依赖是工程习惯。

**API 调用**

```python
import requests, json

response = requests.get("https://api.coincap.io/v3/assets/bitcoin",
                        headers={"Authorization": "Bearer YOUR_API_KEY"})
data = response.json()          # 转成 dict
price = float(data["data"]["priceUsd"])
print(f"${price:,.4f}")
```

**自己写库**：任意 `.py` 文件就是模块，同目录下 `import mymodule` 即可。模块里的 `if __name__ == "__main__":` 保证被导入时不执行测试代码。

### 本讲习题：Problem Set 4

**1. Emojize（emojize.py）** —— 把 `:thumbsup:` 这类代码/别名转成 emoji。考点：`emoji` 库。

```python
import emoji
print(emoji.emojize(input(), language="alias"))
```

**2. Frank, Ian and Glen's Letters（figlet.py）** —— 零个参数用随机字体，两个参数 `-f/--font 字体名` 用指定字体（非法字体名 `sys.exit`）。考点：`pyfiglet` + `sys.argv` 分支。

```python
from pyfiglet import Figlet
import sys

figlet = Figlet()
fonts = figlet.getFonts()
args = sys.argv[1:]
if len(args) == 0:
    pass
elif len(args) == 2 and args[0] in ("-f", "--font") and args[1] in fonts:
    figlet.setFont(font=args[1])
else:
    sys.exit("Invalid usage")
print(figlet.renderText(input()))
```

**3. Adieu, Adieu（adieu.py）** —— 逐行读名字到 Ctrl-D，按牛津逗号规则告别：两个名字用 `and`，三个及以上用 `, ` 分隔 + 最后一个 `and`。考点：`inflect` 库，或手写拼接。

```python
import inflect
p = inflect.engine()
names = []
while True:
    try:
        names.append(input())
    except EOFError:
        break
print("Adieu, adieu, to " + p.join(names))
```

**4. Guessing Game（game.py）** —— 先问 level（非正整数重新问），随机生成 1..n，猜大输出 `Too large!`，猜小 `Too small!`，猜中 `Just right!`。考点：`random.randint` + 两个 `while True` 校验循环。

```python
import random

while True:
    try:
        n = int(input("Level: "))
        if n > 0:
            break
    except ValueError:
        pass

target = random.randint(1, n)
while True:
    try:
        guess = int(input("Guess: "))
    except ValueError:
        continue
    if guess < target:
        print("Too small!")
    elif guess > target:
        print("Too large!")
    else:
        print("Just right!")
        break
```

**5. Little Professor（professor.py）** —— level 1/2/3 对应 1/2/3 位数，出 10 道加法题，答错输出 `EEE` 并重问，连错 3 次直接打印正确答案。考点：随机数范围 + 三层循环（题数、尝试次数、输入校验）。

```python
import random

def randint_level(level):
    if level == 1:
        return random.randint(0, 9)
    return random.randint(10 ** (level - 1), 10 ** level - 1)
```

**6. Bitcoin Price Index（bitcoin.py）** —— 命令行传比特币数量，查 CoinCap v3 API（**现在需要注册拿 API key**），输出 `f"${cost:,.4f}"`。考点：`sys.argv` 校验 + `requests` + JSON 解析 + 异常处理。

**易错点**

- `random.randint(a, b)` 两端都含，跟 `range()` 右开不一样。
- 命令行参数不足要用 `sys.exit("message")` 退出，别让 IndexError 崩出去。
- Little Professor 的 3 位数范围是 `100..999`，别写成 `100..1000`。
- CoinCap v2 已停用，2025 年之后必须走 v3 + API key。

---

## P7 · Lecture 5 单元测试（50:54）

> 你当前进度在这里。

### 核心内容

**为什么测**：把逻辑抽成纯函数（有输入有返回），就能自动验证它对不对，不用每次手敲输入。

**assert**

```python
assert square(2) == 4      # 条件为假就抛 AssertionError
```

**pytest**

1. 写 `test_xxx.py`，函数名以 `test_` 开头。
2. 运行：`pytest test_xxx.py`。
3. 一个测试函数里可以放多个 `assert`，建议一个函数测一个关注点。

```python
# test_calculator.py
from calculator import square

def test_positive():
    assert square(2) == 4
    assert square(3) == 9

def test_negative():
    assert square(-2) == 4

def test_zero():
    assert square(0) == 0
```

**测异常**

```python
import pytest
from fuel import convert

def test_zero_division():
    with pytest.raises(ZeroDivisionError):
        convert("1/0")

def test_value_error():
    with pytest.raises(ValueError):
        convert("cat/dog")
```

**组织**：测试多了可以放 `test/` 子目录（加 `__init__.py`），或保持 `test_被测文件名.py` 与源码同目录 —— CS50P 用后者，最简单。

**关键前提**：被测文件必须有 `if __name__ == "__main__": main()` 守卫，否则 `import` 时会去等输入，pytest 直接卡死。

### 本讲习题：Problem Set 5

**1. Testing my twttr（twttr.py + test_twttr.py）** —— 重写 PSet 2 的 twttr，抽出 `shorten(word)` 返回去元音后的字符串（`main` 才打印），写 1 个以上测试。

```python
# test_twttr.py
from twttr import shorten

def test_upper():
    assert shorten("TWITTER") == "TWTTR"

def test_lower():
    assert shorten("twitter") == "twttr"

def test_numbers():
    assert shorten("1234") == "1234"

def test_punctuation():
    assert shorten("hello, world!") == "hll, wrld!"
```

**2. Back to the Bank（bank.py + test_bank.py）** —— 把 PSet 1 的银行题改成 `value(greeting) -> int`（0/20/100），写 3 个以上测试。注意：题目假定传入的 str 没有前导空格，但仍要大小写不敏感。

**3. Re-requesting a Vanity Plate（plates.py + test_plates.py）** —— 抽出 `is_valid(s) -> bool`，写 4 个以上测试（建议一条规则一组：`test_starts_with_two_letters`、`test_length`、`test_numbers_at_end`、`test_no_punctuation`、`test_zero_first`）。

**4. Refueling（fuel.py + test_fuel.py）** —— 抽出 `convert(fraction) -> int` 和 `gauge(percentage) -> str`。这是唯一要用 `pytest.raises` 的一套：

```python
import pytest
from fuel import convert, gauge

def test_convert():
    assert convert("1/2") == 50
    assert convert("1/4") == 25

def test_gauge():
    assert gauge(1) == "E"
    assert gauge(99) == "F"
    assert gauge(50) == "50%"

def test_errors():
    with pytest.raises(ValueError):
        convert("cat/dog")
    with pytest.raises(ZeroDivisionError):
        convert("1/0")
```

**易错点**

- 被测函数必须 `return`，不能 `print` —— 打印出来的东西 pytest 拿不到。
- 测试文件名不要跟被测文件重名。
- `pytest` 找不到模块时，确认你在文件所在目录运行，且目录里没有同名冲突。
- `convert("3/2")`（分子大于分母）按现行要求要 `raise ValueError`。

---

## P8 · Lecture 6 文件 I/O（1:32:25）

### 核心内容

```python
with open("file.txt", "w") as file:   # 推荐写法，自动关闭
    file.write("hello\n")
```

打开模式：`r`（读，默认）、`w`（写，**会清空原文件**）、`a`（追加）、`r+`（读写）、`rb`/`wb`（二进制）。

读取方式：

```python
with open("names.txt") as file:
    for line in file:                 # 逐行，最省内存
        print(line.rstrip())

# 或者
lines = file.readlines()              # 一次读成列表
content = file.read()                 # 一次读成整串
```

**CSV**

```python
import csv

with open("students.csv") as f:                  # 读
    reader = csv.DictReader(f)                   # 每行是 dict，键来自表头
    for row in reader:
        print(row["name"], row["house"])

with open("out.csv", "w", newline="") as f:      # 写（newline="" 是官方要求，避免空行）
    writer = csv.DictWriter(f, fieldnames=["first", "last", "house"])
    writer.writeheader()
    writer.writerow({"first": "Hannah", "last": "Abbott", "house": "Hufflepuff"})
```

**排序**：`sorted(rows, key=lambda r: r["name"])`，`key=` 后面接「取哪一列」的函数。

**图像（Pillow）**

```python
from PIL import Image, ImageOps

photo = Image.open("input.jpg")
shirt = Image.open("shirt.png")
photo = ImageOps.fit(photo, shirt.size)      # 缩放并裁剪到指定尺寸
photo.paste(shirt, shirt)                    # 第二个 shirt 当遮罩，保留透明背景
photo.save("output.jpg")
```

### 本讲习题：Problem Set 6

**1. Lines of Code（lines.py）** —— 命令行传一个 `.py` 文件，统计有效代码行（排除注释和空行）。考点：`sys.argv` 校验（必须恰好 1 个参数且以 `.py` 结尾）+ 逐行判断。

```python
count = 0
with open(sys.argv[1]) as f:
    for line in f:
        stripped = line.strip()
        if stripped == "" or stripped.startswith("#"):
            continue
        count += 1
print(count)
```

**2. Pizza Py（pizza.py）** —— 读 CSV 菜单，用 `tabulate` 输出 ASCII 表格，表头格式 `grid`。考点：`csv.reader` + `tabulate` + 两个命令行参数校验（`sys.exit` 提示）。

```python
import csv, sys
from tabulate import tabulate

if len(sys.argv) != 2 or not sys.argv[1].endswith(".csv"):
    sys.exit("Usage: python pizza.py file.csv")

with open(sys.argv[1]) as f:
    rows = list(csv.reader(f))
print(tabulate(rows[1:], headers=rows[0], tablefmt="grid"))
```

**3. Scourgify（scourgify.py）** —— 读 `before.csv`（`name,house`，姓名是 `"姓, 名"`），拆成 `first,last,house` 写进 `after.csv`。考点：`csv.DictReader`/`DictWriter` + 字符串拆分 + 参数个数校验。

```python
last, first = row["name"].split(", ")
writer.writerow({"first": first, "last": last, "house": row["house"]})
```

**4. CS50 P-Shirt（shirt.py）** —— 两个命令行参数（输入图、输出图），把 `shirt.png` 叠上去。考点：Pillow 的 `ImageOps.fit` + `paste` 遮罩用法（见上）。

**易错点**

- 写 CSV 一定加 `newline=""`，否则 Windows 下每行之间多一个空行，check50 判不过。
- `open(path, "w")` 会立刻清空文件，路径写错就是灾难。
- 文件不存在会 `FileNotFoundError`，需要时用 `try/except` 或 `sys.exit` 提示。

---

## P9 · Lecture 7 正则表达式（2:05:00）

### 核心内容

```python
import re

re.search(r"^\w+@\w+\.(com|edu|org)$", s)   # 有没有匹配（返回 Match 或 None）
re.match(pattern, s)                        # 只从开头匹配
re.fullmatch(pattern, s)                    # 整串完全匹配（校验首选）
re.findall(pattern, s)                      # 返回所有匹配的字符串列表
re.sub(pattern, repl, s)                    # 替换
re.split(pattern, s)                        # 分割
```

常用元字符：

| 符号 | 含义 |
|---|---|
| `.` | 任意单个字符（除换行） |
| `*` `+` `?` | 0 次或多次 / 1 次或多次 / 0 或 1 次 |
| `{m,n}` | 重复 m 到 n 次 |
| `^` `$` | 开头 / 结尾锚点 |
| `[a-z]` `[^0-9]` | 字符集合 / 取反 |
| `\d` `\w` `\s` | 数字 / 单词字符 / 空白（`\D \W \S` 取反） |
| `\b` | 单词边界 |
| `(a\|b)` | 分组与或 |
| `(?:...)` | 非捕获分组 |

修饰符：`re.IGNORECASE`（忽略大小写）、`re.MULTILINE`（`^`/`$` 匹配每行）、`re.DOTALL`（`.` 也匹配换行）。

分组取值：

```python
m = re.search(r"^(\d+) (\w+)$", s)
if m:
    print(m.group(1), m.group(2))     # group(0) 是整串
```

### 本讲习题：Problem Set 7

**1. NUMB3RS（numb3rs.py + test_numb3rs.py）** —— 判断 IPv4 是否合法：四段，每段 0–255。考点：可以先 `re.fullmatch(r"\d+\.\d+\.\d+\.\d+")` 再检查范围，或者干脆用 `split(".")` 手写（更简单也更不容易错）。

```python
import re

def validate(ip):
    if not re.fullmatch(r"\d+\.\d+\.\d+\.\d+", ip):
        return False
    return all(0 <= int(n) <= 255 for n in ip.split("."))
```

**2. Watch on YouTube（watch.py + test_watch.py）** —— 从 `<iframe src="https://www.youtube.com/embed/xxxxx">` 里提取视频 ID，输出 `https://youtu.be/xxxxx`。考点：正则分组提取，且要拒绝非 YouTube 的 embed 链接。

```python
import re

def parse(s):
    if m := re.search(r"^.*(?:https?://)?(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]+).*$", s):
        return f"https://youtu.be/{m.group(1)}"
    return None
```

**3. Working 9 to 5（working.py + test_working.py）** —— 把 `9:00 AM to 5:00 PM` 转成 `09:00 to 17:00`。考点：字符串解析 + 12/24 小时制转换，**12 点是特例**：`12 AM → 00`、`12 PM → 12`；格式不合法要 `raise ValueError`。

```python
def convert(s):
    if m := re.fullmatch(r"(\d{1,2})(?::(\d{2}))? (AM|PM) to (\d{1,2})(?::(\d{2}))? (AM|PM)", s):
        ...
    raise ValueError
```

**4. Regular, um, Expressions（um.py + test_um.py）** —— 数「um」作为独立单词出现的次数，不区分大小写，`yummy` 不算。考点：`\b` 单词边界 + `re.IGNORECASE`。

```python
import re

def count(s):
    return len(re.findall(r"\bum\b", s, re.IGNORECASE))
```

**5. Response Validation（response.py）** —— 用 `validator-collection` 或 `validators` 库判断邮箱是否合法。考点：第三方库引入（`pip install validators`）。

```python
import validators
print("Valid" if validators.email(input("Email: ")) else "Invalid")
```

**易错点**

- 模式字符串一律加 `r` 前缀（原始字符串），不然 `\b` 会被 Python 当转义吃掉。
- 做校验用 `fullmatch` 或加 `^...$`，只用 `search` 会放过 `abc123@x.com.cn` 这类尾部多余内容。
- `\b` 在 `um,` 后面能匹配，在 `yummy` 里不能 —— 这正是考点。

---

## P10 · Lecture 8 面向对象编程（2:47:41）

### 核心内容

```python
class Student:
    def __init__(self, name, house):     # 构造器，self 是实例自身
        if not name:
            raise ValueError("Missing name")
        self.name = name
        self.house = house

    def __str__(self):                   # print(实例) 时调用
        return f"{self.name} from {self.house}"

    @property                            # 读方法，像属性一样访问
    def house(self):
        return self._house

    @house.setter                        # 写方法，赋值时校验
    def house(self, house):
        if house not in ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]:
            raise ValueError("Invalid house")
        self._house = house

    @classmethod
    def get(cls):                        # 类方法，第一个参数是 cls
        return cls(input("Name: "), input("House: "))

    @staticmethod
    def yell(text):                      # 不访问实例/类，就是普通函数挂进来
        return text.upper()
```

要点：

- 类变量（直接在类体里定义）被所有实例共享，要用 `ClassName.var` 改，别用 `self.var = `（那只给实例加了个新属性）。
- 继承：`class Wizard(Student): pass`，子类重写方法，`super().__init__(...)` 调父类构造。
- 自定义异常：

```python
class TooManyCookiesError(Exception):
    pass
```

- 运算符重载：`__add__`、`__eq__`、`__lt__`、`__len__` 等，让你的对象支持 `+`、`==`、排序。
- `raise ValueError("msg")` 主动抛异常，配合 `try/except` 使用。

### 本讲习题：Problem Set 8

**1. Seasons of Love（seasons.py）** —— 输入生日 `YYYY-MM-DD`，输出活了多少分钟的**英文大写开头**字符串，如 `Five hundred twenty-five thousand, six hundred minutes`。考点：`datetime.date` + `inflect.number_to_words`。

```python
from datetime import date
import inflect
import sys

def main():
    try:
        birth = date.fromisoformat(input("Date of Birth: "))
    except ValueError:
        sys.exit("Invalid date")
    minutes = (date.today() - birth).days * 24 * 60
    p = inflect.engine()
    print(p.number_to_words(minutes, andword="").capitalize() + " minutes")


if __name__ == "__main__":
    main()
```

**2. Cookie Jar（jar.py + test_jar.py）** —— 实现 `Jar` 类：`__init__(capacity=12)`（capacity 不是非负 int 就 `raise ValueError`）、`__str__` 返回 n 个 🍪、`deposit(n)` / `withdraw(n)` 超界 `raise ValueError`、`@property` 暴露 `size` 和 `capacity`。考点：类 + property + 异常，测试用 `pytest.raises`。

```python
class Jar:
    def __init__(self, capacity=12):
        if not isinstance(capacity, int) or capacity < 0:
            raise ValueError("Invalid capacity")
        self._capacity = capacity
        self._size = 0

    def __str__(self):
        return "🍪" * self._size

    def deposit(self, n):
        if self._size + n > self._capacity:
            raise ValueError("Too many cookies")
        self._size += n

    def withdraw(self, n):
        if n > self._size:
            raise ValueError("Not enough cookies")
        self._size -= n

    @property
    def capacity(self):
        return self._capacity

    @property
    def size(self):
        return self._size
```

**3. CS50 Shirtificate（shirtificate.py）** —— 用 `fpdf2` 生成 A4 竖版 PDF：顶部居中 `CS50 Shirtificate`，中间 shirtificate.png 居中，名字用白字压在衣服上。考点：`FPDF(orientation="P", unit="mm", format="A4")`、`set_font`、`cell(w=0, txt=..., align="C")`、`image(x=..., y=..., w=...)`、`set_text_color(255, 255, 255)`、`output("shirtificate.pdf")`。

**易错点**

- `capacity` 校验要用 `isinstance(capacity, int)`，注意 `bool` 是 `int` 的子类（`isinstance(True, int)` 为 True），想严格点就额外排除 bool。
- `__str__` 返回的是 `n` 个饼干，不是 `"n cookies"`。
- Seasons 用 `andword=""` 去掉英文里的 "and"，并 `.capitalize()` 首字母大写。
- fpdf2 的 `image()` 定位需要自己算 `x = (210 - w) / 2` 之类，A4 宽 210mm。

---

## P11 · Lecture 9 其它内容（2:29:04）

### 核心内容

**set 集合**：无序、去重。

```python
s = set()
s.add(1); s.remove(1)
s1 | s2    # 并集
s1 & s2    # 交集
s1 - s2    # 差集
list(set(names))    # 快速去重（会丢顺序，要保序用 dict.fromkeys）
```

**全局变量**：函数里改全局变量要先声明 `global x`，否则会被当成局部变量。尽量少用，用参数传递代替。

**常量约定**：全大写命名 `PI = 3.14`，Python 并不阻止你改，只是约定。

**类型注解 + docstring**

```python
def greet(name: str) -> str:
    """Greet the user by name."""       # docstring，可用 help() 查看
    return f"hello, {name}"
```

注解只是提示，不强制；`mypy` 可以做静态检查。

**argparse（新版补充）**：比 `sys.argv` 更专业的命令行解析，自动生成 `--help`。

```python
import argparse

parser = argparse.ArgumentParser(description="Say hello")
parser.add_argument("name", help="your name")
parser.add_argument("-s", "--shout", action="store_true")
args = parser.parse_args()
print(args.name.upper() if args.shout else args.name)
```

**解包**

```python
a, b = b, a                 # 交换（不用临时变量）
first, *rest = [1, 2, 3]    # first=1, rest=[2,3]
coords = (1, 2); x, y = coords
```

**args 与 kwargs**

```python
def f(*args, **kwargs):     # args 收成元组，kwargs 收成字典
    print(args, kwargs)
f(1, 2, name="David")       # (1, 2) {'name': 'David'}
```

**map / filter / lambda**

```python
list(map(str.upper, ["a", "b"]))              # ['A', 'B']
list(filter(lambda x: x > 0, [-1, 2, 3]))     # [2, 3]
```

**推导式（Pythonic 的代表）**

```python
squares = [x ** 2 for x in range(10)]                 # 列表推导
evens = [x for x in range(10) if x % 2 == 0]
lengths = {w: len(w) for w in words}                  # 字典推导
unique = {w.lower() for w in words}                   # 集合推导
```

**enumerate / zip**

```python
for i, name in enumerate(names):          # 同时拿索引和值
    print(i, name)

for name, house in zip(names, houses):    # 并行遍历多个序列
    print(name, house)
```

**生成器与迭代器**

```python
def countdown(n):
    while n > 0:
        yield n            # 产出值并暂停，下次继续
        n -= 1

for i in countdown(3):
    print(i)               # 3 2 1
```

生成器不会一次性把所有值算出来，处理大文件时省内存。

### 本讲配套：Final Project

没有固定题目，要求：自己想一个 Python 项目，用上课上讲过的东西，带 README 说明怎么跑、带测试。官方有 Gallery of Final Projects 可以参考选题。

结合你的情况，建议往「能解决实际问题的工具」上靠（这批项目以后能写进简历）：

- 化工/制造：物料配比计算器 + 单位换算、进出库台账 CSV 汇总、化验单数据清洗与统计图表。
- 通用小工具：批量重命名/整理文件夹、Excel 报表合并、网页信息抓取 + 结构化入库。

**易错点**

- 可变默认参数陷阱：`def f(items=[])` 的列表会被所有调用共享，要写 `def f(items=None)` 然后在函数里 `items = items or []`。
- 生成器和列表推导的区别：生成器只能用一次，遍历完就没了。

---

## 附：全课程习题总表（41 题）

- **PSet 0（L0）**：Indoor Voice、Playback Speed、Making Faces、Einstein、Tip Calculator
- **PSet 1（L1）**：Deep Thought、Home Federal Savings Bank、File Extensions、Math Interpreter、Meal Time
- **PSet 2（L2）**：camelCase、Coke Machine、Just setting up my twttr、Vanity Plates、Nutrition Facts
- **PSet 3（L3）**：Fuel Gauge、Felipe's Taqueria、Grocery List、Outdated
- **PSet 4（L4）**：Emojize、Frank Ian and Glen's Letters、Adieu Adieu、Guessing Game、Little Professor、Bitcoin Price Index
- **PSet 5（L5）**：Testing my twttr、Back to the Bank、Re-requesting a Vanity Plate、Refueling
- **PSet 6（L6）**：Lines of Code、Pizza Py、Scourgify、CS50 P-Shirt
- **PSet 7（L7）**：NUMB3RS、Watch on YouTube、Working 9 to 5、Regular um Expressions、Response Validation
- **PSet 8（L8）**：Seasons of Love、Cookie Jar、CS50 Shirtificate
- **Final Project（L9 之后）**：自选项目

提交流程（官方环境）：`check50 cs50/problems/2022/python/indoor` 自测 → `submit50 cs50/problems/2022/python/indoor` 提交。年份路径按官网当年为准。
