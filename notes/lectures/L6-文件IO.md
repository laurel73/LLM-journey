# CS50P 第 6 讲 · 文件 I/O（File I/O）完整笔记

> 讲师：David J. Malan（哈佛大学）
> 本讲主题：让程序把数据保存到文件里、再从文件里读回来 —— 从此数据不再随着程序退出而消失。

---

## 本讲速览

**一句话主题**：之前我们写的所有程序都把数据存在内存（memory，内存）里，程序一退出数据就没了；这一讲用**文件 I/O（Input/Output，输入/输出）**把数据持久地存进磁盘，并学会处理纯文本、CSV 表格和二进制图片三类文件。

**本讲知识清单**

1. 为什么需要文件：内存中的变量（`list`（列表）也一样）在程序退出后全部消失
2. `open()` 函数：以 `"w"`（write，写）模式打开文件，写入、关闭
3. `"w"` 模式的坑：每次打开都会**重建**文件，旧内容被覆盖
4. `"a"`（append，追加）模式：往文件末尾追加内容
5. `write()` 不会自动换行，必须自己写 `\n`
6. `with` 关键字：自动关闭文件，不用担心忘记 `close()`
7. `"r"`（read，读）模式，且读模式是默认模式，可以省略
8. `readlines()` 一次性读出所有行，返回 `list`
9. 直接 `for line in file` 逐行遍历，更 Pythonic
10. `rstrip()` 去掉行尾的换行符，避免 `print` 多打一个空行
11. 想要排序就必须先把数据全部读进内存，不能边读边排
12. `sorted()` 的 `reverse=True` 参数实现倒序
13. CSV（Comma-Separated Values，逗号分隔值）文件格式：一行一条记录，逗号分列
14. `split(",")` 手工拆逗号，以及"序列解包"（unpack）一次赋两个变量
15. 用"列表 + 字典"保存结构化数据：`list of dict`
16. `sorted(..., key=函数名)`：告诉 Python 按哪个字段排
17. `lambda`（匿名函数）：只用一次的小函数不必起名字
18. 数据里本身含逗号会让 `split` 崩掉：`ValueError: too many values to unpack`
19. `csv` 标准库：`csv.reader` / `csv.DictReader` / `csv.writer` / `csv.DictWriter`
20. 在 CSV 第一行写表头（header），配合 `DictReader` 实现"防御式编程"
21. 二进制文件（binary file）与 `PIL`（Pillow）库
22. 用 Pillow 把多张静态图合成一张动图 GIF

**本讲时间轴**（总时长 1:32:19）

| 时间点 | 当时在讲什么 |
| --- | --- |
| [00:00:00] | 开场：为什么需要 File I/O |
| [00:05:02] | 用列表收集三个名字并排序打印 |
| [00:10:02] | `"w"` 模式每次都重建文件，Hermione 和 Harry 丢了 |
| [00:15:00] | `with open(...) as file` 自动关闭文件 |
| [00:20:01] | 不必显式读完所有行，直接 `for line in file` |
| [00:25:00] | 保留"先收集到列表再排序"的写法 |
| [00:30:01] | 想再存一个"学院"字段，引出 CSV |
| [00:35:01] | `split(",")` 与 `row` 命名约定 |
| [00:40:01] | 为了排序，先把整句英文塞进列表 |
| [00:45:02] | 改用字典保存 name/house |
| [00:50:02] | 换成 `get_house`，按学院排序 |
| [00:55:03] | `lambda`：没有名字的函数 |
| [01:00:02] | 分隔符用竖线？加引号？还是用库？ |
| [01:05:04] | `csv.reader` 成功解析含逗号的地址 |
| [01:10:01] | `csv.DictReader`，用列名取值 |
| [01:15:01] | `csv.writer` 的 `writerow` |
| [01:20:02] | `csv.DictWriter` 与单双引号的选择 |
| [01:25:00] | 二进制文件与 Pillow 库 |
| [01:30:01] | `sys.argv[1:]` 切片去掉程序名 |

---

## 一、开场：程序一退出，数据就蒸发了 [00:00:00]

这一讲是 CS50P 的文件 I/O 周。

Malan 先回顾了此前所有程序的一个共同缺陷：我们写过的几乎每一个程序，都只是把收集到的信息存在**内存**（memory）里 —— 也就是存在变量里、存在程序内部。这样做的坏处是：**程序一退出，你输入过的一切、程序做过的一切，全部丢失。**

而在 Mac 或 PC 上，文件当然是可以长期保存信息的。所谓 **File I/O**，就是写代码去：

- **read**（读）：把信息从文件里**加载**进程序；
- **write**（写）：把信息**保存**到文件里。

这一讲的目标，就是完成一次过渡：从"只用内存和变量"，过渡到"能写文件、能让数据持久保存的代码"。

---

## 二、从列表开始：收集多个名字 [00:03:00]

### 2.1 最简单的版本：一个名字 [00:03:00]

Malan 打开 VS Code，创建 `names.py`，先用我们熟悉的老办法收集一个名字：

```python
# 提示用户输入名字，存进变量 name
name = input("What's your name?")
# 用 f-string 把变量值插进字符串里打印出来
print(f"hello, {name}")
```

命令行运行（`$` 是终端提示符，你不用自己输入它）：

```bash
$ python names.py
What's your name? David
hello, David
```

一切如常。

### 2.2 想收集多个名字？用 `list` [00:04:00]

如果想支持输入**多个**名字（比如就 3 个，方便讨论），自然会想到用 `list`（列表）—— 一个变量通常只存一个值，但如果这个变量是列表，就能存多个值。

先在文件顶部主动准备一个变量，这次叫 `names`（复数），赋值为空列表：

```python
names = []

for _ in range(3):
    name = input("What's your name?")
    names.append(name)
```

要点解释：

- `[]` 这个方括号记号，里面什么都不写，就表示"给我一个空列表"，之后可以往里加东西。
- `for _ in range(3)`：循环三次，每次用 `input()` 问一次名字。
- `names.append(name)`：用列表的 `append` 方法把这个名字追加进去。

> **讲师的口头强调（Pythonic 约定）**：这里的循环变量你完全可以叫 `i`（这是传统写法）。但如果后续代码里你**根本没用到** `i` 的值，那就干脆用 `_`（下划线），这是 Python 的约定俗成，意思是"这个变量我不关心"。

### 2.3 精简版：去掉中间变量 [00:04:30]

注意，`name` 这个变量其实没什么必要 —— 我们只是给它赋个值，然后立刻 `append`。完全可以再紧凑一点：

```python
names = []

for _ in range(3):
    names.append(input("What's your name?"))
```

> **讲师的设计权衡**：这属于两种都可以的设计取向。一方面，写成一行确实很短、很好读；另一方面，如果哪天你把提示语从 `What's your name?` 改成很长的一句话，那把它拆回两行又更合适。目前这样写挺可读的。

### 2.4 排序后再打印 [00:05:02]

现在程序后面要做的，是把这些名字**按字母序排好**再打印出来 —— 既然我们把它们都收集到一起了，排序再输出才说得通。

Python 里最简单的做法是用内置函数 `sorted()`，它会**返回**一个排好序的新版本：

```python
names = []

for _ in range(3):
    names.append(input("What's your name?"))

# sorted() 返回一个排序后的新列表，不改变原列表
for name in sorted(names):
    print(f"hello, {name}")
```

运行：

```bash
$ python names.py
What's your name? Hermione
What's your name? Harry
What's your name? Ron
hello, Harry
hello, Hermione
hello, Ron
```

输入的顺序是 Hermione、Harry、Ron，完全不是字母序；但循环一跑起来，输出的就是排好序的 Harry、Hermione、Ron。

**但是！** 到这里 Malan 立刻泼了一盆冷水：

> 如果你再运行一次这个程序，**所有名字都没了**。

如果这个程序再大一点，每次都要重新输入同样的信息，那会非常痛苦。想想现在的手机 App、笔记本、云端程序 —— 哪一个不是能把信息"存起来"的？这就是 File I/O 存在的理由。文件就是一种把信息**持久地**存在你自己的手机、Mac、PC 或者某台云服务器磁盘上的方式，等你下次再运行程序时，它们还在那儿。

---

## 三、`open()`：把名字写进文件 [00:07:00]

### 3.1 先简化回"一个名字" [00:07:30]

为了讲清楚写文件，Malan 先把程序简化回只收集一个名字：

```python
name = input("What's your name? ")
```

接下来要做的不是把它加进列表、也不是立刻打印，而是**把这个刚输入的名字存进一个文件**。

### 3.2 `open()` 是什么 [00:08:00]

Python 有一个内置函数叫 `open`，它命里的任务就是：**打开一个文件** —— 但是以编程的方式打开，好让作为程序员的你真正能从里面读信息、往里面写信息。

> **讲师的类比**：`open` 就相当于"程序员版的双击桌面图标"。之所以说它是程序员的手段，是因为你可以精确地指定你想从文件里读什么、往文件里写什么。

`open` 的最简用法只需要一个参数：你想打开的**文件名**；可选地再传第二个参数：你想**以什么方式**打开它。

### 3.3 第一版：以 `"w"`（写）模式打开 [00:08:30]

```python
name = input("What's your name? ")

# 打开（不存在就创建）names.txt，模式 "w" = write，可写
file = open("names.txt", "w")
# 把 name 写进文件
file.write(name)
# 关闭并保存文件
file.close()
```

逐行讲：

- `open("names.txt", "w")`：第一个参数是文件名 `names.txt`。名字你想叫什么都行，但因为它存的是纯文本，惯例是用 `.txt` 后缀。
- 第二个参数 `"w"` 是 **w**rite（写）的首字母，告诉 `open`：我要以"允许我改动内容"的方式打开这个文件。更妙的是，**如果这个文件还不存在，它会替你创建出来**。
- `open` 的返回值叫做 **file handle**（文件句柄），是一个特殊的值，让你之后能访问这个文件。这里我们把它赋给变量 `file`。
- `file.write(name)`：`write` 是打开的文件自带的一个函数（更准确说是**方法 / method**），用来把内容写进文件。
- `file.close()`：关闭文件，也就是真正**保存**它。

> **讲师的总结**：这三行代码，本质上就是"程序员版的双击图标 → 在 Word 里改点东西 → 点菜单 File → Save"。我们只不过是用这三行代码把整件事做完了。

### 3.4 演示：运行三次，然后翻车 [00:09:30]

```bash
$ python names.py
What's your name? Hermione
$ code names.txt      # 打开刚生成的文件
```

文件里确实是 `Hermione`。

再运行两次，分别输入 Harry 和 Ron。然后满怀希望地打开 `names.txt`：

```
Ron
```

**只有 Ron。Hermione 和 Harry 去哪儿了？** 明明运行了三次，代码里也确实写了"把这个名字写进文件"。

**学生（Vishal）的回答（非常精彩，讲师原话确认"Exactly"）**：

> 因为我们不是追加（append），而是直接写（write）。每次都在擦掉旧内容，替换成我们最后一次写进去的字符。

Malan 的补充：

> **`"w"` 有点危险。** 它不只会在文件不存在时替你**创建**文件，它还会在你**每次**以这个模式打开文件时，替你**重新创建**一遍。

所以：第一次打开写 Hermione，没问题；第二次打开时文件被重建，写进 Harry；第三次又被重建，写进 Ron。三个版本先后存在过，最后只剩 Ron。

我们真正想要的，是像 Vishal 说的那样，把每个名字**追加**（append）到文件里，而不是每次都把文件**碾平重写**（clobber / overwrite）。

---

## 四、改成 `"a"`（追加）模式 [00:11:00]

### 4.1 一个字的修改 [00:11:00]

先删掉旧文件，再把 `"w"` 改成 `"a"`：

```bash
$ rm names.txt      # rm = remove，删除文件
```

```python
name = input("What's your name? ")

file = open("names.txt", "a")   # "a" = append，追加到文件末尾
file.write(name)
file.close()
```

`a` 是 **a**ppend（追加）的首字母，意思是"一次次地加到文件的底部、底部、底部"。

再跑三次，输入 Hermione、Harry、Ron，打开 `names.txt`：

```
HermioneHarryRon
```

### 4.2 第二个翻车：名字全黏在一起了 [00:12:00]

三个名字是都在了，但是**完全看不出每个名字从哪儿结束、下一个从哪儿开始**。

学生的第一反应（讲师纠正了措辞）：

> 英文格式不对，它把它们连接（concatenate）起来了。

**讲师的纠正（这里很值钱）**：

> 看起来像是在做字符串拼接，但严格来说这只是**追加** —— 先追加 Hermione，再追加 Harry，再追加 Ron。效果上是把它们背靠背连在了一起，但它**并不是**在做字符串意义上的拼接（concatenation）。

另一位学生给出了真正的解法：

> 我们应该在写新名字之前加一个换行。

**讲师的点睛（重要对比）**：

> 回想一下，`print` 默认**总是**自动输出一个行尾换行 `\n`，除非你用命名参数 `end` 去覆盖它。
> 但 `write` **不会**。`write` 是非常字面地执行你的指令：你说写 `Hermione`，那就只有 H 到 e；你说写 `Harry`，那就只有 H 到 y。**它不会自动给你加任何换行。**

所以如果你想让每个名字后面都有换行，这个换行得你自己手动加。

### 4.3 修好：手动写 `\n` [00:13:30]

删掉当前文件，改代码：

```python
name = input("What's your name? ")

file = open("names.txt", "a")
# 手动在名字后面拼一个换行符 \n
file.write(f"{name}\n")
file.close()
```

> 讲师说明：修法有很多种。你可以单独再 `write` 一个换行，也可以用别的技巧；我这里按我一贯的习惯，用 f-string 把"名字 + 换行"一次写完。

再跑三次（Hermione / Harry / Ron），`names.txt` 现在清爽了：

```
Hermione
Harry
Ron
```

每个名字各占一行，而且行尾有换行符，这样我们就能把一条记录和另一条区分开。

> **讲师的设计提醒**：当然，如果你写解析代码时靠"大小写字母的变化"去猜名字边界，也未必不行 —— 但那很快就会变得一团糟。一般来说，长期把数据存在文件里时，你应该存得**干净**一点，比如"一行一个值"。

---

## 五、`with`：让 Python 自动帮你关文件 [00:15:00]

### 5.1 为什么需要 `with` [00:14:30]

现在代码是能正常工作的，但**设计上还能更好**。

问题在于：写代码时**太容易忘记关文件了**。有时候这不算大事，但有时候会出问题 —— 文件可能被损坏、被意外删除之类，取决于你的代码里发生了什么。

好消息是：如果你换一种写法，你就**不必**自己去调 `close()`。

### 5.2 `with` 的写法 [00:15:00]

在 Python 里，操作文件更 Pythonic 的方式是引入另一个关键字，名字就叫 `with`。它的含义是："在这个上下文中，我要打开某个文件，并且让它**自动**关闭。"

```python
name = input("What's your name? ")

# 文件会在 with 代码块结束后自动关闭
with open("names.txt", "a") as file:
    file.write(f"{name}\n")
```

注意这些细节：

- 我们**删掉了** `file.close()` 那一行。
- 不再写 `file = open(...)`，而是写 `with open(...)`，参数还是老样子，然后**有点奇怪地把变量放到了这一行的末尾**。
- 为什么放末尾？**就是这么设计的，没有为什么。** 你说 `with`，调用那个函数，然后说 `as`，再指定一个变量名，用来接收 `open` 的返回值。
- 下面那行要**缩进**，表示"写名字"这行代码处在 `with` 语句的上下文里。

**`with` 的效果**：这不会改变刚才已经发生的事情，但它把"关闭文件"这件事**自动化**了。只要执行完缩进块的最后一行，即使这个文件下面还有很多不缩进的代码，文件也已经自动关闭了。这样我就不会忘，也就不会因此出岔子。

---

## 六、把名字读回来 [00:17:00]

### 6.1 先往文件里多塞一条数据 [00:17:00]

到目前为止我们只写了"往文件里写名字"的代码。现在假设文件里已经有 Hermione、Harry、Ron 了，再多加一个 Draco：

```bash
$ python names.py
What's your name? Draco
```

现在 `names.txt` 里有四个名字：

```
Hermione
Harry
Ron
Draco
```

### 6.2 第一版：`readlines()` 读出所有行 [00:18:00]

思路类似：还是 `with open(...)`，第一个参数还是文件名，但这次用 `"r"`（**r**ead，读）模式打开 —— 读文件就是**加载**它，不是保存它。

```python
with open("names.txt", "r") as file:
    lines = file.readlines()

for line in lines:
    print("hello,", line)
```

- `readlines` 是打开的文件自带的一个特殊方法，它的命里任务就是：把文件里**所有行**读出来，作为一个 `list` 返回给你。
- 所以上面第 2 行的作用是：读出所有行，存进变量 `lines`。
- 然后用一个标准的 `for` 循环遍历：每次 `line` 会被自动设成其中一行，打印出来。

运行结果 —— 能跑，但**很丑**：

```bash
$ python names.py
hello, Hermione

hello, Harry

hello, Ron

hello, Draco

```

每个 hello 之间都多出一个空行。

### 6.3 第三个翻车：换行符被打了两次 [00:19:00]

**学生（Ripal）的回答（讲师说"Perfect"）**：

> 因为文本文件里每个名字后面本来就带着换行符，而 `print` 又总是会在末尾再加一个换行。所以同一个符号被用了两次。

讲师顺势夸了一句：

> 这就是一个很好的 **bug**（程序中的错误）例子。但只要你回到**第一性原理**去想 —— 我用的每一行代码各自是怎么工作的？ —— 你就应该能推理出来：其中一个换行来自文件里名字的后面，另一个换行是 `print` 这么多周以来一直在免费送给我们的。

### 6.4 两种修法 [00:19:30]

**修法一：给 `print` 传命名参数 `end=""`**

```python
with open("names.txt", "r") as file:
    lines = file.readlines()

for line in lines:
    print("hello,", line, end="")
```

**修法二（讲师更推荐）：用 `rstrip()` 把行尾的换行剥掉**

```python
with open("names.txt", "r") as file:
    lines = file.readlines()

for line in lines:
    print("hello,", line.rstrip())
```

> **讲师的设计取向**：我认为第二种稍微更好一点。让 `print` 负责打印所有内容（人名 + 换行），而我们只是把文件里那个**实现细节**剥掉。
> "用换行符来分隔一条条记录"是**我自己选择的**文件设计；既然如此，把它剥掉、让 `print` 去打印一个真正的"名字"，设计上更干净。
> 但这终究是个设计选择 —— 两种写法的**效果完全一样**。

### 6.5 更简洁：`for line in file` [00:20:01]

既然我们要"打开文件 → 读所有行 → 遍历所有行 → 逐个打印"，那这其实做了**两遍**工作。Python 里可以直接合成一件事。把大部分行删掉，只留顶上的 `with`：

```python
with open("names.txt", "r") as file:
    for line in file:
        print("hello,", line.rstrip())
```

注意这个写法有多优雅：第 1 行打开文件，如果你想遍历文件里的每一行，你**不必**很显式地"先读完所有行、再遍历所有行"，你可以把这两件事合成一念。

在 Python 里你只要说 `for line in file`，就能得到一个逐行遍历文件的循环，每轮自动把变量 `line` 更新成 Hermione、然后 Harry、然后 Ron、然后 Draco。

> **讲师的感慨**：这又是 Python 讨人喜欢的一个地方 —— 它读起来很像英语："for line in file, print this"。写成这样也更紧凑。

---

## 七、想排序？那就不能边读边打印 [00:22:00]

### 7.1 新的需求：无论如何都要排好序 [00:22:00]

现在跑 `python names.py` 是对的：每个 hello 一行，中间没有多余空行。

但 Malan 故意刁难一下自己：他希望这些 hello 是**排好序**的 —— 不管文件里的顺序如何，都要先看到 Draco，再 Harry，再 Hermione，最后 Ron。

当然，你可以直接进文件手动改。但如果这个文件是随着用户不断输入名字而变化的，那就不是个好办法。**在代码里，我应该能够加载任意样子的文件，然后一次性排好序。**

### 7.2 为什么 `for line in file` 在这里不够用 [00:22:30]

这正是**不能**用刚才那个简洁写法的原因：

> 我不能一边逐行遍历文件、一边打印，同时又想"提前把所有东西排序"。逻辑上，如果我是看一行打印一行，那排序就已经太晚了。我真正需要的是：**先把所有行读进来（不打印），排序，然后再打印。** 为了加这个新功能，我们得退一步。

### 7.3 正确做法：先收集到列表，再排序 [00:23:00]

```python
names = []

with open("names.txt") as file:
    for line in file:
        names.append(line.rstrip())

for name in sorted(names):
    print(f"hello, {name}")
```

这里还有一个**可以收紧的小细节**：

> 如果你打开文件是为了**读**它，你其实**不需要**指定 `"r"`。那就是隐含的默认值。所以你可以写成 `open("names.txt")`，照样能读不能写。

逐行解释：

- 第 1 行：在文件开头建一个列表，只是给自己一个收集数据的地方。
- 第 3~5 行：从上到下遍历文件，每次读进一行，剥掉行尾的换行，**只把学生名字**加进这个列表。注意：这是往**内存里的列表**追加，不是往文件里追加。
- 第 7~8 行：现在所有名字都在内存里了，于是可以排序再打印。

**为什么必须这样？** 因为要排序，就得先**全部加载进内存**。否则我会在排序之前就把它们打印出来，Draco 就会排在最后而不是最前。

运行结果：

```bash
$ python names.py
hello, Draco
hello, Harry
hello, Hermione
hello, Ron
```

> **讲师总结（通用套路）**：这真的是一个非常常见的技巧。处理文件和信息时，如果你想对数据做某种改动（比如排序），那就：
> 1. 在程序顶部创建某种变量（比如一个 `list`）；
> 2. 把信息 `append` 进去，收集到一处；
> 3. 然后对这个集合做点有意思的事。

### 7.4 更紧凑的版本（但要小心） [00:24:30]

如果**只想**给文件排序，Python 里甚至可以更简单 —— 不用 `names` 列表，也不用第二个 `for` 循环：

```python
with open("names.txt") as file:
    for line in sorted(file):
        print("hello,", line.rstrip())
```

这里直接对 `file` 本身调用 `sorted()`，然后在这个循环里立刻打印（仍然用 `rstrip` 剥掉行尾空白）。运行结果一样，但代码紧凑得多。

**不过为了后续讨论，Malan 又把改动撤了回去**，保留"先收集到列表"的版本 —— 因为我们往往想在遍历数据时**对它做点改动**（比如强制转大写/小写），然后再排序打印。

---

## 八、学生提问环节（第一轮） [00:26:00]

### 8.1 怎么倒序排？`reverse=True` [00:26:00]

**学生问**：能不能反过来排？不是 A 到 Z，而是 Z 到 A。有没有什么"小扩展"可以加在末尾，还是说必须自己写个新函数？

**Malan 的回答**：确实有。一如既往，**文档是你的朋友**。

Python 官方文档里 `sorted` 的签名大致是这样：

```
sorted(iterable, *, key=None, reverse=False)
```

- 第一个参数叫 **iterable**（可迭代对象）。所谓"可迭代"，就是你可以**一个一个地遍历**它，也就是能对它做循环。
- 中间那个 `key`："你想按什么来排序"，这个稍后讲。
- 最后一个命名参数是 `reverse`。**按文档，它的默认值是 `False`** —— 默认不反转。但如果改成 `True`，我猜就成了。

于是回 VS Code，给 `sorted` 传第二个参数：

```python
names = []

with open("names.txt") as file:
    for line in file:
        names.append(line.rstrip())

# reverse=True 覆盖默认的 False
for name in sorted(names, reverse=True):
    print(f"hello, {name}")
```

运行：Ron 跑到最上面，Draco 落到最下面。

> **讲师的方法论**：以后你再碰到这类问题，先想想**文档怎么说**，看看里面有没有一丝线索。因为大概率 —— 如果你有某个问题，**在你之前的某个程序员也遇到过同样的问题**。

### 8.2 能限制名字数量吗？能查找特定名字吗？ [00:28:00]

**学生问**：能不能限制名字的数量？还有，能不能在列表里找到某个特定的名字？

**Malan 的回答**：非常好的问题，两个都能做。

- **限制数量**：可以先打开文件，数一数现在已经有多少行；如果已经太多了，就用 `sys.exit` 或者别的提示退出程序，告诉用户"抱歉，课满了"。
- **查找某人**：完全可以。想象一下：打开文件，用 `for` 循环一遍遍遍历，然后加一个条件判断 —— 如果当前行 `== "Harry"`，那就说明找到了，打印点什么就行。

> 也就是说，你完全可以把这些新想法和之前学过的**条件判断**结合起来，去问同样的问题。

### 8.3 既然每次都要 `rstrip`，为什么函数不自己剥掉？ [00:29:00]

**学生问**：`readlines` 这个函数看起来是用换行符把各行分开的，但我们似乎并不需要这个字符，每次都要自己 `strip` 掉。这看起来像是**糟糕的设计** —— 为什么不干脆在函数里面就把它剥掉呢？

**Malan 的回答**（这是个很好的问题）：

> 到目前为止我的例子里确实用 `rstrip` 剥掉了行尾的所有空白，但**你可能并不想这么做**。
>
> 我现在之所以剥掉它，是因为我知道：这里的每一行并不是什么"通用的一行文本"，**每一行真的就代表一个我自己放进去的名字**，我用换行符只是为了分隔一个值和另一个值。
>
> 但在别的场景里，你很可能**想保留**那个行尾 —— 比如那是一段很长的文本、一个段落之类的，你希望它和其它段落彼此区分开。
>
> 说到底这只是个**约定**。我们总得用点什么东西来把一块文本和另一块文本分开。

> Python 里确实还有**别的**函数会自动帮你处理掉那些空白。但 `readlines` 就干它字面上的那件事：**原样读出所有行**。

---

## 九、CSV：一行存不下"名字 + 学院" [00:30:01]

### 9.1 混着存的坏设计 [00:30:01]

回到 `names.txt`。它能很好地存名字，但如果我们还想存**别的信息**呢？比如学生的名字**和**他在霍格沃茨的学院（Gryffindor / Slytherin 之类）。

一个天真的做法是直接在文本里这么写：

```
Hermione
Gryffindor
Harry
Gryffindor
Ron
Gryffindor
Draco
Slytherin
```

> **讲师的担忧**：我担心这有点**把苹果和橘子混在一起**了 —— 有些行是名字，有些行是学院。这大概不是最好的设计，光是"令人困惑 / 含义模糊"这一点就够糟了。

### 9.2 换成 CSV 约定 [00:31:00]

于是我们可以采用一个约定 —— 事实上这也是**很多程序员**的做法：把这个文件不叫 `names.txt`，而是新建一个 `students.csv`。

**CSV = Comma-Separated Values（逗号分隔值）**。这是"在同一个文件里存多条相关信息"的一种非常常见的约定。

做法是：**每个学生仍然占一行**，但在一行内部，用一个**逗号**（而不是换行）来分隔这个学生的各项信息：

```
Hermione,Gryffindor
Harry,Gryffindor
Ron,Gryffindor
Draco,Slytherin
```

> **讲师的比喻**：这样我们就有了一个"二维"的文件。一行一行看，是我们一个个学生；如果你把那些逗号想象成**列**（虽然因为名字长短不一，看起来有点参差不齐），那些逗号就代表了列。

**CSV 的现实用途**：当你在 Microsoft Excel、Apple Numbers 或 Google Spreadsheets 里想把数据**导出**给别人时，非常常见的做法就是导出成 CSV 文件；反过来，你也可以把一个 CSV 文件**导入**到你喜欢的表格软件里。

所以 CSV 是一种非常常见、非常简单的文本格式：**用逗号分隔值，用换行分隔一条条记录**。

---

## 十、手工解析 CSV：`split` 与解包 [00:33:00]

### 10.1 建文件、建程序 [00:33:00]

```bash
$ code students.csv     # 新建一个空文件，然后填入上面的四行
$ code students.py      # 新建一个读它的程序
```

### 10.2 第一版：用 `split(",")` 拆 [00:34:00]

思路和之前类似：

```python
with open("students.csv") as file:
    for line in file:
        row = line.rstrip().split(",")
        print(f"{row[0]} is in {row[1]}")
```

先要搞清楚一件事：在这个循环里，每一轮我拿到的是**整行文本**。我不会自动拿到"只有 Hermione"或者"只有 Gryffindor"。

> **讲师的课堂互动**：逻辑上，如果循环给你的是一整行文本，而你想拿到里面的各个值（Hermione 和 Gryffindor、Harry 和 Gryffindor），你打算在循环里做什么？凭直觉说就行，哪怕你不知道函数名。

- 学生 A：能不能像字典那样用 key / value 访问？
  - **讲师**：理想情况下我们确实想用 key 和 value 访问。但在这个故事的这一刻，我们手上只有这个循环，而循环给我的是一整行文本。**我现在是程序员，我得自己解决这个问题 —— 此刻还没有什么字典。**
- 学生 B：能不能按逗号把这两个词**拆开**？
  - **讲师**：对！哪怕你还不确定哪个函数能做这件事，直觉上你想做的是：把整行文本（`Hermione, Gryffindor`、`Harry, Gryffindor`……）拆成两块。而妙的是，**我们要用的函数真的就叫 `split`**。

`split` 的用法：

- `split` 是 `str`（字符串）自带的方法 —— Python 里**任何一个 `str`** 都内置了这个功能。
- 你传一个参数进去，比如逗号 `","`，`split` 就会反复找这个字符，把当前字符串切成 1 块、2 块、3 块甚至更多块。
- 最终 `split` 会把"逗号左边和右边的各个部分"作为一个 `list` 返回给我们。

变量为什么叫 `row`？

> 这是个常见范式。当你明确知道自己在遍历一个 CSV 文件时，习惯上把**每一行**想成 row（行），把行里被逗号分开的**各个值**想成 column（列）。所以我故意把变量命名为 `row`，跟这个约定保持一致。

打印时怎么取值？

- `row` 里有几块？**两块** —— 因为每行只有一个逗号，切出来就是左一块右一块（Hermione / Gryffindor）。
- 那怎么拿到列表里的单个值？用下标：`row[0]` 是第一个元素（学生名字），`row[1]` 是第二个元素（学院）。
- 记住：**Python 从 0 开始数**。

看起来第一眼有点 cryptic（难懂），但大部分只是 f-string 的花括号语法，花括号里塞的是 `row[0]` 和 `row[1]`。

运行：

```bash
$ python students.py
Hermione is in Gryffindor
Harry is in Gryffindor
Ron is in Gryffindor
Draco is in Slytherin
```

到这里，我们**从零开始自己实现了一个真正的 CSV 解析器**（parse = 读取并解释）。

### 10.3 学生提问：能改文件中间某一行吗？ [00:37:00]

**学生问**：我们能随时编辑文件里的任意一行吗？还是说唯一的选项只有往末尾追加？比如我们想把 Harry 的学院改成 Slytherin 或别的。

**Malan 的回答**：很好的问题。如果你想在 Python 里**改动文件中的某一行**而不只是追加到末尾，**这个逻辑得你自己实现**。

比如你可以：打开文件，把所有内容读进来，然后遍历每一行，一看到当前名字 `== "Harry"`，就把他的学院改成 Slytherin。然后**还得由你**把这些改动全部写回文件。

最简单的形式是：

1. 读一遍文件，然后让它关闭；
2. 再打开一次，这次以**写**的方式打开，把整个文件改掉。

> 想只改动文件的一部分，其实**不是做不到的，但并不容易**。更简单可靠的做法是：**整个读出来 → 在内存里改 → 整个写回去**。当然，如果文件非常大、整个重写会很慢，那你可以做得更聪明一些。

### 10.4 改进：`row[0]` / `row[1]` 太难读 [00:38:00]

`row[0]`、`row[1]` 这种写法， lecturer 直言"我认为目前写得不太好，可读性欠佳"。

好消息是：当你有一个列表变量 `row` 时，你**不必**把这些值都塞进一个列表里 —— 你可以**一次性解包（unpack）整个序列**。

也就是说：如果你知道 `split` 会返回一个列表，而且你**事先知道**它会返回两个值（第一个和第二个），那你就不必把它们都扔进一个"本身是列表"的变量里，而是可以**同时**把它们解包到两个变量中：

```python
with open("students.csv") as file:
    for line in file:
        # 一次给两个变量并行赋值
        name, house = line.rstrip().split(",")
        print(f"{name} is in {house}")
```

`name, house` 是一个很棒的 Python 技巧：**一次性创建并同时（并行）给两个变量赋值**，而不是只赋一个。效果是：左边的 `name` 拿到 Hermione，右边的 `house` 拿到 Gryffindor。

现在我们**没有 `row` 了**，代码可以直接写成 `name` 和 `house`，可读性更好 —— 尽管**功能上完全一样**。

运行结果不变：

```bash
$ python students.py
Hermione is in Gryffindor
Harry is in Gryffindor
Ron is in Gryffindor
Draco is in Slytherin
```

---

## 十一、排序：从"排整句话"到"排真正的字段" [00:40:01]

### 11.1 第一版：把整句英文塞进列表再排序 [00:40:01]

现在假设我们想让输出也是排好序的：先 Draco，再 Harry，再 Hermione，最后 Ron。

从前面的例子取经，那就在拼好句子之后，先把它临时存进一个列表，攒起来，之后再排序：

```python
students = []

with open("students.csv") as file:
    for line in file:
        name, house = line.rstrip().split(",")
        # 注意：不是打印，而是把整句英文追加进列表（内存里）
        students.append(f"{name} is in {house}")

for student in sorted(students):
    print(student)
```

运行：

```bash
$ python students.py
Draco is in Slytherin
Harry is in Gryffindor
Hermione is in Gryffindor
Ron is in Gryffindor
```

确实 Draco 第一、Harry 第二、Hermione 第三、Ron 第四。

### 11.2 讲师的自我批评：这有点 hackish [00:41:00]

> 但这 arguably 有点**潦草**。我在这儿拼这些英文句子，感觉有点像 hack（凑合）。
> 虽然我**技术上**想按名字排序，但我**实际**排序的是这些完整的英文句子。

这不算错，也确实达到了预期效果，但**设计得不好** —— 我只是**运气好**，因为英文是从左往右读的，所以排出来的顺序碰巧是对的。

真正好的做法是：**找到一种"按学生名字排序"的技术**，而不是按我在第 6 行拼出来的某个英文句子排序。

### 11.3 引入字典：把"名字"和"学院"的关联保住 [00:42:00]

要做到这一点，得先把生活搞复杂一点：**在拼句子之前，先把每个学生的信息收集起来**。

回想一下，Python 支持 `dict`（字典）—— 字典就是**键和值的集合**。你可以把某个东西和另一个东西关联起来，比如"name 关联 Hermione"、"house 关联 Gryffindor"。这真的就是一个字典。

**写法一：先建空字典，再逐个塞键**

```python
students = []

with open("students.csv") as file:
    for line in file:
        name, house = line.rstrip().split(",")
        student = {}                  # 花括号 = 空字典
        student["name"] = name
        student["house"] = house
        students.append(student)

for student in students:
    print(f"{student['name']} is in {student['house']}")
```

- 就像用 `[]` 创建空列表一样，你可以用 `{}` 创建一个空字典 —— 给我一个空字典，它马上就会有 `name` 和 `house` 两个键。

**这里有个学生提问（非常关键）**：

> 在这个 f-string 里，我用花括号、花括号里放变量名 —— 这些都照旧。但我为什么要在 `house` 和 `name` 外面套**单引号**？

**学生回答 + 讲师确认（Exactly）**：

> 因为你这行（第 12 行）外面已经用了**双引号**。所以你必须告诉 Python 把里面和外面区分开。

**讲师的完整解释**：

> 正是如此。因为我在 f-string 外面已经用了双引号，如果我想在**里面**再给字符串加引号（而对字典来说我**必须**加）—— 回想一下，**索引字典时你用的不是数字（0、1、2……），而是字符串，而字符串需要引号** —— 那么既然外面是双引号，里面最简单的做法就是**用单引号**，这样 Python 就不会搞混哪个引号跟哪个引号配对。

**为什么要把代码变复杂？**

> 我承认我把代码搞复杂了，行数变多了。但我现在把关于学生的**所有信息都收集起来了，同时还保留着"什么是名字、什么是学院"的区分**。而那个 `students`（复数）列表，则把所有这些学生的名字和学院都装在了一起。

### 11.4 精简：一步建好非空字典 [00:45:00]

如果你习惯于"先建一个空字典，然后立刻塞进两个键 `name` 和 `house`、值分别是 `name` 和 `house`"，那你其实可以**一次性**做完：

```python
students = []

with open("students.csv") as file:
    for line in file:
        name, house = line.rstrip().split(",")
        # 一行搞定，等价于上面三行
        student = {"name": name, "house": house}
        students.append(student)

for student in students:
    print(f"{student['name']} is in {student['house']}")
```

右边不再是空花括号，而是直接把键和值定义好：`"name"` 对应 `name`，`"house"` 对应 `house`。

效果一模一样：创建一个包含 `name` 键（值是学生名字）和 `house` 键（值是学生学院）的非空字典，但**三行变一行**。其它代码都不用改。

运行结果还是那些问候语 —— **但仍然没有排序**。

---

## 十二、`sorted` 的 `key` 参数：告诉 Python 按什么排 [00:46:00]

### 12.1 问题：字典本身没法排序 [00:46:00]

现在没法像之前那样直接排序了。因为那些 `student` **不再是名字**（不像最开始），**也不再是句子**（不像刚才那个 hack），每一个 `student` 都是一个**字典** —— 而"怎么排序一个装在列表里的字典"，并不显然。

我们理想中想要的是：

> 此刻我们有一个装着所有学生的列表，列表里每个学生是一个字典，每个字典有 `name` 和 `house` 两个键。要是能用代码告诉 Python "**排序这个列表时，请去看每个字典里的这个键**"，那该多好？
>
> 因为那样我们就能自由选择按 `name` 排、按 `house` 排，甚至按以后往这个文件里加的**任何字段**排。

### 12.2 解法：定义一个 `get_name` 函数 [00:47:00]

`sorted` 除了能 `reverse`，还接受另一个**命名参数** `key`，你可以在里面指定"用什么键来排序这个字典列表"。

先定义一个函数（暂时用一下）：

```python
students = []

with open("students.csv") as file:
    for line in file:
        name, house = line.rstrip().split(",")
        students.append({"name": name, "house": house})

def get_name(student):
    return student["name"]

for student in sorted(students, key=get_name):
    print(f"{student['name']} is in {student['house']}")
```

- `get_name` 这个函数的命里任务很简单：给它一个 `student`，它就**返回这个学生的名字**。就这一件事，这是它存在的唯一意义。
- 然后 `key=get_name`：把 `get_name` 作为 `key` 参数的值传进去。

**这里是 Python 的一个特性：Python 允许你把函数作为参数传给另一个函数。**

- `get_name` 是个函数，`sorted` 是个函数，我们把 `get_name` 传进 `sorted`，作为 `key` 参数的值。

**为什么能这么干？**

> 想想 `get_name` 这个函数，它只是一段"能取到学生名字"的代码块。这恰好就是 `sorted` 需要的能力。
>
> 当 `sorted` 拿到一个"每个元素都是字典"的学生列表时，它需要知道"**我怎么拿到这个学生的名字？**"才能帮你做字母序排序。
>
> 而 Python 的作者们并不知道我们这门课上会创建"学生"这种东西，所以他们**不可能预先**写好专门针对 `student` 这个字段、甚至针对 `name` 或 `house` 的排序代码。
>
> 那他们做了什么？他们在 `sorted` 里内置了 `key` 这个命名参数，让我们这些年后可以**告诉他们的 `sorted` 函数：该怎么排序这个字典列表**。

运行：

```bash
$ python students.py
Draco is in Slytherin
Harry is in Gryffindor
Hermione is in Gryffindor
Ron is in Gryffindor
```

现在输出是排好序的了，因为那个字典列表已经**按学生名字**排过了。

### 12.3 叠加 `reverse=True` [00:50:00]

就像之前一样，如果想整个反过来，加 `reverse=True`：

```python
for student in sorted(students, key=get_name, reverse=True):
    print(f"{student['name']} is in {student['house']}")
```

现在变成 Ron、Hermione、Harry、Draco。

### 12.4 换成 `get_house`：按学院排 [00:50:02]

我们还可以做点不一样的：比如**按学院名字倒序**排。

把函数从 `get_name` 改成 `get_house`，实现也改成返回 `student["house"]`：

```python
students = []

with open("students.csv") as file:
    for line in file:
        name, house = line.rstrip().split(",")
        students.append({"name": name, "house": house})

def get_house(student):
    return student["house"]

for student in sorted(students, key=get_house, reverse=True):
    print(f"{student['name']} is in {student['house']}")
```

运行：现在是按学院**倒序**排 —— Slytherin 第一，然后才是 Gryffindor。

如果去掉 `reverse`、保留 `get_house` 再跑一次，就变成按学院正序：Gryffindor 第一，Slytherin 最后。

> **讲师的总结（这一段的精髓）**：
> 现在的好处在于，因为我用了**字典列表**，并且**一直保留着学生的完整数据、直到最后一刻才拼打印语句**，所以我对这些信息有了**完全的控制权**，我可以按这个排、也可以按那个排。
> 我不必像第一次那样、很 hack 地**提前把句子拼好**。

---

## 十三、学生提问环节（第二轮） [00:52:00]

### 13.1 排序一定要自己写循环吗？ [00:52:00]

**学生问**：我们排序文件的时候，每次都要用循环、或者文本字典、或者某种列表吗？有没有办法只靠"排序"本身，不用循环、不用那些东西？

**Malan 的回答**：好问题。简短的回答是 —— **光用 Python 的话，你是程序员，排序得你来做。** 但**借助库和别的技术，绝对可以**做得更自动化，因为**别人已经把那段代码写好了**。

> 我们现在所做的一切，都是**从零自己动手**。但毫无疑问，用上别的函数或库，其中一些事可以做得更轻松。

### 13.2 `key` 能不能等于一个变量或值？ [00:53:00]

**学生问**：`key` 等于某个函数的返回值，那它能不能就等于一个变量、或一个值？

**Malan 的澄清（这段非常重要，讲师自己说"这点其实并不显然，我应该澄清一下"）**：

> 是的，它应该等于一个**值**。
>
> 当你把 `get_name` 或 `get_house` 这样的函数作为 `key` 的值传给 `sorted` 时，**这个函数会被 `sorted` 自动替你调用**，对列表里的**每一个字典**各调用一次。
>
> 然后 `sorted` 用 `get_name` / `get_house` 的**返回值**来决定"实际用哪些字符串去做比较"，从而判定字母序谁先谁后。
>
> 所以：这个函数你是**只按名字传进去的，末尾不带括号** —— 它由 `sorted` 去调用，好替你搞清楚该怎么比较这些值。

> **讲师再次强调**：注意我这里调用 `get_name` 时**没有加括号**。我只是按名字把它传进去，好让 `sorted` 函数替我去调用它。

### 13.3 嵌套字典 vs 列表套字典 [00:54:00]

**学生问**：怎么用**嵌套字典**（nested dictionaries）？我读过嵌套字典。嵌套字典和"字典放在列表里"有什么区别？我觉得我们现在这个就是。

**Malan 的回答**：

> 我们用的是**列表套字典**。为什么？
> - 因为其中**每个字典代表一个学生**，而一个学生有名字和学院，我想**保住这个关联**；
> - 之所以是**列表**，是因为我们有多个学生（这里是四个）。
>
> 你当然可以构造一个**字典套字典**的结构。但我会说：**它并不能解决什么问题**。我现在不需要"字典套字典"，我需要的是"一组键值对的列表"。就这么简单。

---

## 十四、`lambda`：不需要名字的函数 [00:55:00]

### 14.1 为什么可以砍掉 `get_name` [00:55:00]

回到 `students.py`，回到"定义并使用 `get_name`、它返回学生名字"的版本。已经很清楚的是：`sorted` 会拿 `key` 的值（`get_name`）去对列表里**每一个字典**调用，而 `get_name` 返回一个字符串，`sorted` 就真的用这个字符串来决定谁左谁右，据此做字母序。

而注意：我传函数时**没有加括号**，只是按名字传进去。

现在，一如既往的规律又来了：**如果你定义了某个东西（一个变量，或者这里是一个函数），马上就用到它，而且之后再也不需要它的名字（比如 `get_name`）了 —— 那你就可以把代码再收紧一点。**

就像你可以砍掉一个并非必需的变量一样，你也可以**把 `get_name` 整个删掉**。

### 14.2 `lambda` 的写法 [00:55:03]

不再给 `key` 传"一个函数的名字"，而是传一个 **lambda 函数** —— 也就是**匿名函数**（anonymous function），一个**没有名字**的函数。

> 为什么没有名字？因为你只在一个地方调用它，那就没必要给它起名字。

Python 里这个语法有点怪，长这样：

```python
students = []

with open("students.csv") as file:
    for line in file:
        name, house = line.rstrip().split(",")
        students.append({"name": name, "house": house})

for student in sorted(students, key=lambda student: student["name"]):
    print(f"{student['name']} is in {student['house']}")
```

逐字拆开 `lambda student: student["name"]`：

- 先写关键字 **`lambda`**；
- 然后写**参数名**，比如 `student`（我期待这个函数接受的参数叫这个名字）；
- 然后**不敲回车**，直接接着写 `student["name"]`。

> **讲师的原话**：我在高亮的这段代码，等价于我刚才实现的 `get_name` 函数。语法确实不太一样：我没用 `def`，我甚至没给它起名字（比如 `get_name`），我用的是 Python 里另一个关键字 `lambda`，意思是"嘿 Python，来了一个函数，但它没有名字，它是匿名的"。

- 这个函数接受一个参数。参数名**你想叫什么都可以**，我这里叫 `student`。为什么？因为作为 `key` 传进去的这个函数，会被作用在列表里的**每一个学生**（每一个字典）上。
- 那我想让这个匿名函数返回什么？**给定一个 `student`，我要索引进那个字典、取出他的名字**，从而最终返回 Hermione、Harry、Ron、Draco 这些字符串。而 `sorted` 就用它来决定：怎么排序这些**还带着 `house` 等其它键的**大字典。

**效果**：跑起来还是一样，但**设计上 arguably 更好** —— 我没有浪费几行代码去定义另一个函数、然后只在一处调用它，而是一口气把事情做完了。

### 14.3 学生提问：lambda [00:58:00]

**问题一：能定义两次 lambda 吗？**

> **Malan**：你**可以**用两次 lambda，你想创建多少个匿名函数都行。一般来说你是在**这样的场景**里用它们：你想把"一个本身不需要名字的函数"传给某个别的函数。所以你绝对可以在多个地方用。我只是目前只有一个用例。

**问题二：如果 lambda 需要多个参数呢？**

> **Malan**：没问题。如果你的 lambda 函数接受多个参数，直接**用逗号分隔、把参数名依次列在 `student` 后面**就行，比如 `x` 和 `y` 之类。
>
> 所以 lambda 跟 `def` 看起来确实很不一样：**没有括号、没有 `def` 关键字、没有函数名**。但它们最终达到的效果是一样的 —— **匿名地创建一个函数**，并允许你把它（比如这里）作为某个值传进去。

---

## 十五、第四个翻车：地址里竟然有逗号 [00:59:00]

### 15.1 改需求：不存学院了，存"老家" [00:59:00]

现在把 `students.csv` 改成存的不是霍格沃茨学院，而是**他们长大的地方**（home）：

- Draco 在 Malfoy Manor 长大；
- Ron 在 The Burrow 长大；
- Harry 在 **Number Four, Privet Drive** 长大；
- 而据网上说法，没人知道 Hermione 在哪儿长大（电影似乎在这一点上擅自发挥了一下）。所以为了这个目的，我们**把 Hermione 删掉**，因为她的出生地不明。

于是 CSV 变成三行：

```
Harry,"Number Four, Privet Drive"
Ron,The Burrow
Draco,Malfoy Manor
```

> **讲师的铺垫**：如果有人能看出这里潜在的麻烦，这会是个多大的坏事？我们先跑一下自己的代码试试。

### 15.2 对应改代码 [01:00:00]

回 `students.py`，把语义从 house 改成 home（变量名、英文措辞都改），但仍然按名字排序：

```python
students = []

with open("students.csv") as file:
    for line in file:
        name, home = line.rstrip().split(",")
        students.append({"name": name, "home": home})

for student in sorted(students, key=lambda student: student["name"]):
    print(f"{student['name']} is in {student['home']}")
```

### 15.3 报错：`ValueError: too many values to unpack` [01:01:00]

```bash
$ python students.py
Traceback (most recent call last):
  File "students.py", line 5, in <module>
    name, home = line.rstrip().split(",")
ValueError: too many values to unpack
```

**我们的第一个 `ValueError`。** 程序直接跑不起来了。怎么解释？错误信息相当 cryptic：**too many values to unpack（要解包的值太多了）**，出问题的正是 `split` 那一行。

**在所有这些成功运行之后，第 5 行怎么突然就崩了？**

**学生回答**：CSV 里有一行有三个值。

**Malan 的解释（还带了个花絮）**：

> 是的。我花了好长时间去查每个学生该来自哪儿，好给我们制造出这个问题。而妙的是，书里的第一句话就是 **Number Four, Privet Drive** —— **这个地址里自带一个逗号**，这就麻烦了。为什么？
>
> 因为我们（你和我）在前面某个时刻决定：**统一用逗号** —— CSV，逗号分隔值 —— 来**划定一个值和另一个值的边界**。
>
> 而如果学生的老家**在语法上**就含逗号，那它显然会被误当成这个**特殊符号**。于是对 Harry 这一行，`split` 试图拆出**三个**值而不是两个 —— 这就是"要解包的值太多"的原因，因为我们只准备了 `name` 和 `home` 两个变量去接。

### 15.4 三种自救方案，然后放弃 [01:01:30]

**方案一：换个分隔符，比如竖线 `|`**

可以把所有逗号改成竖线。

> 但这**迟早也会咬我们一口** —— 万一哪天文件里出现了竖线，照样会崩。所以这大概不是最好的办法。

**方案二：转义（escape）数据 —— 给含逗号的字符串加引号**

也可以像我以前做过的那样，给任何"本身含逗号"的英文字符串**加上引号**。这没问题，我可以这么做。

> 但那样一来，我的 `students.py` **也得跟着改** —— 因为我不能再天真地按逗号 `split` 了。我得变聪明点：只切分那些**不在引号里面**的逗号。
>
> 噢，这下迅速变复杂了。

**方案三（正解）：别重复造轮子**

> 到了这一步，你得退一步想一想：**如果我们有这个问题，我们之前大概率已经有无数人遇到过同样的问题。**
>
> 把数据存进文件，这是极其常见的需求；**用 CSV 文件**，这也是极其常见的需求。
>
> 所以：**为什么不看看 Python 里是不是已经有一个库，专门用来读和/或写 CSV 文件？**
>
> 与其"重新发明轮子"，不如**站在前人的肩膀上** —— 用那些早已离开我们的程序员写好的代码，去真正地读写 CSV，这样我们就能把精力集中在我们真正在乎的那部分问题上。

---

## 十六、`csv` 标准库之 `csv.reader` [01:04:00]

### 16.1 `import csv` + `csv.reader` [01:04:00]

Python 里确实有一个模块叫 `csv`。改代码：

```python
import csv

students = []

with open("students.csv") as file:
    reader = csv.reader(file)
    for row in reader:
        students.append({"name": row[0], "home": row[1]})

for student in sorted(students, key=lambda student: student["name"]):
    print(f"{student['name']} is from {student['home']}")
```

- 在程序开头 `import csv`，用上别人写好的库 —— 让**它**去处理所有这些"边角情况"（corner cases）。
- 我仍然给自己一个初始为空的列表，用来装所有学生。
- 打开文件时这么写：`reader = csv.reader(file)`。

**`csv.reader` 是干什么的？**

> 如果你去读 `csv` 模块的文档，会发现它自带一个函数叫 `reader`，它的命里任务就是：替你读 CSV 文件，自己搞清楚**逗号在哪儿、引号在哪儿、所有潜在的边角情况都在哪儿**，然后**替你处理好**。
>
> 如果你不是用逗号、而是用竖线之类的，你也可以覆盖它的某些默认假设。但默认情况下，我觉得它直接就能用。

**怎么遍历 `reader`（而不是原始文件）？**

几乎一样，库允许你这样写：`for row in reader`。

- 现在你**不是**在直接遍历文件本身，而是在遍历 `reader` —— 而 `reader` 会替你处理所有逗号、换行等等的解析工作。
- `reader` 每读到文件里的一行，就返回一个 `row`。但这个 `row` 是**一个列表**：列表第一个元素是学生名字，第二个元素是学生的老家。
- 想取值就还是用下标 —— 记住**列表从 0 开始**：`row[0]` 是名字，`row[1]` 是老家。

### 16.2 也可以在 `for` 里直接解包 [01:06:00]

如果我知道这个 CSV 只有两列，我甚至可以这么写：

```python
import csv

students = []

with open("students.csv") as file:
    reader = csv.reader(file)
    for name, home in reader:
        students.append({"name": name, "home": home})

for student in sorted(students, key=lambda student: student["name"]):
    print(f"{student['name']} is from {student['home']}")
```

这样我就不用列表下标了，可以一次性解包，然后下面直接写 `name` 和 `home`。其余代码完全不用动 —— 第 8 行构造的还是同一个字典（只不过现在是 home 而不是 house），而我是从 `reader` 而不是从"文件 + 我自己的 `split`"里取值。

运行：

```bash
$ python students.py
Draco is from Malfoy Manor
Harry is from Number Four, Privet Drive
Ron is from The Burrow
```

成功了，而且还是排好序的。Harry 的地址里那个逗号被完整地保留了下来。

### 16.3 学生提问 [01:07:00]

**问题一：能让一个文件既可读又可写吗？**

> **Malan**：非常好的问题。简短回答是：**可以**。
>
> 不过，历史上人们对文件的**心智模型**是**磁带**（cassette tape）。很多年前的东西，现在不怎么用了，但磁带是**顺序**访问的：它从头开始，如果你想走到末尾，你得把带子"倒"到那个位置。
>
> 现在最接近的类比大概是 Netflix 或者任何流媒体服务 —— 有一个进度条，你得从左往右拖。你不能"跳到这儿"或"跳到那儿"。**你没有随机访问（random access）能力。**
>
> 所以文件的问题在于：如果你想边读边写，那么**你（或某个库）必须记录你在文件里的位置**。这样你从顶部开始读、又在底部写了东西，之后想重新从头读，就得 **seek（寻道）回开头**。
>
> 这属于我们课上不会做的事情，它更复杂一些，但绝对可行。**对我们的目的而言，一般建议是：读文件；想改的话，就整个写回去**，而不是试图做各种零敲碎打的修改 —— 当然，如果文件特别巨大、改整个文件在时间上非常昂贵，那另当别论。

**问题二：能在文件里写一段话（paragraph）吗？**

> **Malan**：完全可以。我现在写的是很短的字符串，就名字或者学院。但你**绝对**可以写任意多的文本。

**问题三：用户能自己选 key 吗？比如输入的 key 是 name 还是 code？**

> **Malan**：简短回答，**可以**。我们完全可以写一个程序，提示用户输入名字和老家、名字和老家，然后把这些值写出去。**一会儿我们就来看怎么写 CSV 文件。**
>
> 目前我作为创建 `students.csv` 的程序员，是**假设我知道有哪些列**，所以才相应地给变量命名。

---

## 十七、`csv.DictReader`：把列名写进文件里 [01:09:00]

### 17.1 表头（header）的灵感来源 [01:09:00]

不过这个问题正好引出了**读 CSV 的最后一个特性**：

> 你**不必**依赖"拿到一个列表形式的 row、然后用 `[0]` 或 `[1]`"，也**不必**手动这样解包。我们可以更聪明一点：**直接把列名存进 CSV 文件本身。**

事实上，如果你打开过电子表格文件（Excel、Apple Numbers、Google Spreadsheets 之类），你大概率注意到过：**第一行经常是不一样的**。它有时是**粗体**，或者它装的其实是**下面那些列的名字、那些属性的名字**。

我们也可以这么做。在 `students.csv` 里，我不必一直假设"名字在第一列、老家在第二列"，我可以**把这个信息明确地烤进文件里**，从而降低将来出错的概率。

在文件**第一行**写上：

```
name,home
Harry,"Number Four, Privet Drive"
Ron,The Burrow
Draco,Malfoy Manor
```

> 注意，这里的 `name` 并不是某个人的名字，`home` 也不是某个人的老家 —— 它们**字面就是** `name` 和 `home` 这两个单词，用逗号隔开。

### 17.2 改用 `csv.DictReader` [01:10:01]

现在回 `students.py`，不用 `csv.reader`，改用 **dictionary reader（字典读取器）**：

```python
import csv

students = []

with open("students.csv") as file:
    reader = csv.DictReader(file)
    for row in reader:
        students.append({"name": row["name"], "home": row["home"]})

for student in sorted(students, key=lambda student: student["name"]):
    print(f"{student['name']} is in {student['home']}")
```

- `DictReader` 会从上到下遍历文件，但它把每一行加载为**列的字典**，而不是**列的列表**。
- 我改回 `for row in reader`。
- 之前用 `reader` 时，我用 `[0]` 取第一列、`[1]` 取第二列；而**`reader` 返回列表，`DictReader` 返回字典（一次一个）**。
- 所以现在要取当前行的 name，就写 `row["name"]`；取 home 就写 `row["home"]`。

**我唯一要做的改动，说清楚就是**：在我的 CSV 文件**第一行**加上一点关于"这些列是什么"的小提示。

运行结果不变。

### 17.3 威力展示：把两列顺序对调，代码一行不动 [01:11:00]

现在我的代码对数据的变化**更健壮**了。

假如我在 Excel / Google Spreadsheets / Apple Numbers 里打开这个 CSV，出于某种原因把列的位置换了 —— 也许这个文件你是跟别人共享的，人家就是想左右挪一下列的顺序 —— **以前我的代码会崩**，因为我在假设"name 永远第一、home 永远第二"。

现在我们把文件整个翻转过来（注意：我**小心地同步更新了表头**）：

```
home,name
"Number Four, Privet Drive",Harry
The Burrow,Ron
Malfoy Manor,Draco
```

现在第一列变成了原来的第二列，第二列变成了原来的第一列。

**而我的 Python 代码，我一行都不动**，直接重跑：

```bash
$ python students.py
Draco is in Malfoy Manor
Harry is in Number Four, Privet Drive
Ron is in The Burrow
```

**照样能跑。**

> **讲师的点题**：这也是一个**防御式编程**（coding defensively）的例子。
> 万一有人改了你的 CSV 文件、你的数据文件，怎么办？理想情况下当然不会。但**即使真的改了**，因为我用的是 **dictionary reader**，它会从第一行**自己推断**出每一列叫什么，所以我的代码**继续工作**。这样一来，代码就（可以说是）越来越好了。

### 17.4 学生提问 [01:13:00]

**问题一：CSV 里换行符为什么重要？**

> **Malan**：CSV 里换行符的重要性？这一半是**约定**。在文本文件的世界里，我们人类几十年来就是习惯**一行一行**地存数据。这样**视觉上方便**，从文件里提取也容易 —— 你只要找换行符就行。
>
> 所以换行符只是"把一块数据和另一块数据分开"。我们**也可以**用键盘上任何别的符号，但大家习惯的就是敲一下回车、把数据挪到下一行。**仅仅是约定。**

**问题二：只有 name 和 home 时看着挺好，列变多了怎么办？**

**Malan 现场演示**：比如我们想把 `house` 也加回来。在表头最后加 `house`，然后给 Harry 填 Gryffindor、Ron 填 Gryffindor、Draco 填 Slytherin：

```
home,name,house
"Number Four, Privet Drive",Harry,Gryffindor
The Burrow,Ron,Gryffindor
Malfoy Manor,Draco,Slytherin
```

现在我们有**三列**了 —— 左边是 home，中间是 name，右边是 house，都用逗号分隔，而像 `Number Four, Privet Drive` 这种含逗号的仍然被引号包着。

**注意**：回到 `students.py`，我**一行代码都不改**，直接跑：

```bash
$ python students.py
Draco is in Malfoy Manor
Harry is in Number Four, Privet Drive
Ron is in The Burrow
```

**照样能跑。**

> **讲师的总结**：这就是 **dictionary reader** 如此强大的地方。数据可以随时间变化，可以有越来越多的列，而**你已有的代码不会崩**。
>
> 反过来，如果你在做**假设**（"第一列永远是 name"、"第二列永远是 house"），你的代码会**脆弱得多**（fragile）。一旦这些假设不成立，东西崩得飞快 —— 而在这个例子里，这不成问题。

---

## 十八、写 CSV：`csv.writer` [01:15:01]

### 18.1 先清场 [01:15:00]

除了**读** CSV，我们至少也该瞄一眼怎么**写** CSV。

如果你写的程序想把学生的名字、以及他们的老家存进文件，怎么不断往里加？

先清空 `students.csv`，只留一行简单的表头 `name,home`，以便之后往里插入更多名字和老家：

```
name,home
```

然后到 `students.py`，这次**从头开始写**一个"往外写数据"的版本。

### 18.2 `csv.writer` + `writerow` [01:15:01]

```python
import csv

name = input("What's your name? ")
home = input("Where's your home? ")

with open("students.csv", "a") as file:
    writer = csv.writer(file)
    writer.writerow([name, home])
```

- 仍然 `import csv`。
- 提示用户输入名字：`name = input("What's your name? ")`。
- 提示用户输入老家：`home = input("Where's your home? ")`。
- 打开文件，这次是为了**写**而不是读：`with open("students.csv", "a") as file`。
  - 用 **append（追加）模式**，这样我可以不断往文件里加更多学生和老家，而不是把整个文件覆盖掉。
  - 变量名还是 `file`。
- 给自己一个变量 `writer`，赋值为 `csv` 模块里另一个函数 `csv.writer` 的返回值，这个函数唯一的参数就是那个 `file` 变量。
- 然后：`writer.writerow([name, home])` —— 传给 `writerow` 的是**一个列表**，也就是我想写进文件的那一行的内容。

### 18.3 演示：库自动处理了引号 [01:16:30]

```bash
$ python students.py
What's your name? Harry
Where's your home? Number Four, Privet Drive
```

注意：**这个输入本身是带逗号的**。现在看 CSV 文件：

```
name,home
Harry,"Number Four, Privet Drive"
```

**它被自动加上引号了** —— 这样以后再读这个文件时，就不会把这个逗号误认成 Harry 和他的老家之间那个分隔逗号。

再跑两次：

```bash
$ python students.py
What's your name? Ron
Where's your home? The Burrow

$ python students.py
What's your name? Draco
Where's your home? Malfoy Manor
```

文件现在：

```
name,home
Harry,"Number Four, Privet Drive"
Ron,The Burrow
Draco,Malfoy Manor
```

> 这个库不光按函数名那样**写入了每一行**，它还**处理了转义（escaping）** —— 也就是给任何"本身含逗号"的字符串（比如 Harry 的老家）加上引号。

---

## 十九、写 CSV：`csv.DictWriter` [01:18:00]

### 19.1 为什么要有 DictWriter [01:18:00]

还有另一种实现同一个程序的方式，不必每次都要操心"顺序"、也不必传一个列表进去。

既然我们在意"哪个是 name、哪个是 home"，我们可以用**字典**把这些键和值关联起来。

先把文件里的学生删掉，只留表头 `name,home`。然后改 `students.py`：这次不用 `csv.writer`，改用 **`csv.DictWriter`（字典写入器）**。

```python
import csv

name = input("What's your name? ")
home = input("Where's your home? ")

with open("students.csv", "a") as file:
    writer = csv.DictWriter(file, fieldnames=["name", "home"])
    writer.writerow({"name": name, "home": home})
```

- `DictWriter` 打开文件的方式大体相同。
- 但不是把一行写成 `[name, home]` 这样的列表，而是：
  - 先给出一个真正的**字典**：第一个键是 `"name"`，值是用户输入的名字；再给一个键 `"home"`，值是用户输入的老家。
- **用 `DictWriter` 时我必须给它一个提示：这些列的顺序是什么**，这样写出去之后（即使顺序将来变了）也还能被读回来。
  - 所以我传第二个参数 **`fieldnames`**，等于一个**列表**，列出我知道这个文件里实际存在的列：`["name", "home"]`。
  - 这些要**加引号**，因为它们确实是"列的名字"这种**字符串**。

### 19.2 演示 [01:19:30]

```bash
$ python students.py
What's your name? Harry
Where's your home? Number Four, Privet Drive
```

文件里 Harry 又回来了，而且被正确地转义 / 加了引号。

再跑 Ron / The Burrow、Draco / Malfoy Manor：

```
name,home
Harry,"Number Four, Privet Drive"
Ron,The Burrow
Draco,Malfoy Manor
```

### 19.3 两种 writer 的区别 [01:20:30]

> **讲师的对比**：
> - 用 `csv.writer` 时，**责任在我们**：必须传一个列表，把所有想写的值**从左到右**按顺序列好。
> - 用 **dictionary writer** 时，**这些值在字典里的顺序其实可以是任意的**。实际上我这么写也对：先传 `home` 再传 `name`。
>
> 因为它**是个字典**，所以顺序并不重要 —— 只要**键在、值在**就行。
>
> 而因为我给 `DictWriter` 传了第二个参数 `fieldnames`，就保证了**这个库清楚地知道哪一列装的是 name、哪一列装的是 home**。

### 19.4 学生提问 [01:21:00]

**问题一：什么时候该用单引号、什么时候该用双引号？**

> **Malan**：好问题。在 Python 里，你**一般**用双引号也行、用单引号也行，**无所谓**。
>
> 你只需要**保持自我一致**，这样代码风格全篇看起来统一。
>
> 但有时候**必须交替使用**。比如我之前那个很长的 f-string 外面已经用了双引号，而在 f-string **里面**我用花括号插值了一些变量，那些变量是字典。而**索引一个字典时，你要用方括号加引号** —— 既然外面已经用了双引号，里面一般就该用**单引号**，或者反过来。
>
> 除此之外，我的习惯是**到处都用双引号**；也有人的习惯是**到处都用单引号**。**只有在两者可能被混淆的时候，才有所谓。**

**问题二：一个程序里能用多个 CSV 文件吗？**

> **Malan**：完全可以。你想用多少个 CSV 文件就用多少个。它只是**你可以用来保存数据的格式之一**。

**问题三（很聪明的观察）：`DictReader` 已经返回字典了，那 `students.append(row)` 不行吗？**

> **学生**：当把 CSV 当字典读的时候，你之前……在把字段按名字拆出来。既然你在 `for row in reader` 里，能不能直接 `students.append(row)`，而不用逐个命名字段？
>
> **Malan**：噢，**非常聪明**。简短回答是：**可以** —— 因为 `DictReader` 循环时，一次就返回一个字典，所以 `row` **已经**是个字典了。所以你完全可以这么干，效果在这个例子里真的一样。**观察得很好。**

**问题四（收尾）：读 CSV 时怎么确保没出错？有最佳实践吗？**

> **Malan**：这真是个好问题。总的来说，我会说：**如果你是用代码生成 CSV、用代码读 CSV，而且用的是靠谱的库，理论上就不该出问题** —— 如果库是 100% 正确的，那结果就应该是 100% 正确的。
>
> **问题往往出在你我身上。** 当你让**人类**去碰那个 CSV，或者中间掺和了 Excel、Apple Numbers 之类"未必符合你代码预期"的工具，那事情**确实**可能崩。
>
> 目标嘛 —— 有时候老实说，**解决办法就是手工修**。你进去把 CSV 修好；或者你写**大量的错误检查**；或者你写**大量的 `try` / `except`** 来容忍数据里的错误。
>
> 但总地来说我会说：**如果 CSV（或任何文件格式）只是程序内部用来读写的，你就不该有这方面的顾虑。** 一般来说，**你和我 —— 人类 —— 才是问题所在**，而且往往不是那些程序员，而是那些文件的**使用者**。

---

## 二十、二进制文件与 `PIL`（Pillow） [01:25:00]

### 20.1 从文本文件到二进制文件 [01:24:00]

好，现在提议：**把 CSV 放在一边**，但要注意 CSV 并不是你唯一可以用来读写数据的文件格式。

事实上，CSV 是一种流行格式，纯 `.txt` 文件也是。但你**真的**可以**用任何方式**存数据。我们之所以挑 CSV，是因为它**很有代表性** —— 它展示了如何以**结构化的方式**读写文件：在一个文件里拥有多个键、多个值，而不必诉诸所谓的**二进制文件**（binary file）。

**二进制文件**就是**真的只有 0 和 1** 的文件。这些 0 和 1 可以以任何你想要的方式排列，尤其当你想存的**不是文本信息**，而是**图形、音频或视频**信息时。

而碰巧，Python 的强项之一就是**什么都有库**。事实上有一个流行的库叫 **pillow**，能让你操作图像文件：你可以**加滤镜**（像 Instagram 那样），也可以**做动画**。

所以我们把文本文件先放一放，再做一个演示，这次聚焦在这个库和图像文件上。

### 20.2 目标：自己写个程序生成动图 GIF [01:25:00]

我们来写一个程序，**创建一张动画 GIF**。这东西现在到处都是：meme（表情包）、动画、贴纸之类的。

**动画 GIF 到底是什么？** 它其实就是一个**里面装了很多张图片的图片文件**。你的电脑或手机把这些图片**一张接一张**地放给你看，有时是无限循环。只要图片够多，就产生了**动画的错觉** —— 因为你的大脑和我的大脑会**视觉上自动补上中间的空隙**，并假定"这个东西在动"，哪怕你每秒只看到一帧（或某个序列），看起来也像动画。所以它就是**视频文件的一个简化版**。

### 20.3 素材：两只猫的两个"造型" [01:25:00]

我们先拿**另一门流行编程语言**里的几个"造型"（costume）来用。

打开第一个：

- `costume1.gif`：就是**一张静态的猫的图片**，完全不动。

打开第二个：

- `costume2.gif`：看起来有点不一样。注意 —— 来回切换看 —— **这只猫的腿的位置略有不同**，所以这是第 1 版、那是第 2 版。

> 这两只猫来自 MIT 的一门编程语言叫 **Scratch**，它能让你非常图形化地做动画和更多事情。但我们只用这两张静态图 `costume1` 和 `costume2`，来创作**我们自己的**动画 GIF —— 做完之后你就可以像网上任何 meme 一样，把它发短信 / 发消息给朋友。

### 20.4 写代码：`costumes.py` 第一版 [01:26:30]

```bash
$ code costumes.py
```

我们要写自己的程序，而不是用某个现成下载的应用。程序接收**两个或更多图片文件**作为输入，然后生成一张动画 GIF —— 本质上就是在这两张图之间**无限来回切换**。

假设 `costumes.py` 需要**两个命令行参数**：就是我们想来回动画的那几个造型的文件名。

```python
import sys

from PIL import Image

images = []

for arg in sys.argv[1:]:
    image = Image.open(arg)
    images.append(image)

images[0].save(
    "costumes.gif", save_all=True, append_images=[images[1]], duration=200, loop=0
)
```

逐行解释：

- `import sys`：这样我们就能访问 `sys.argv`。
- `from PIL import Image`：从这个 pillow 库里**专门导入**对图像的支持。注意 **`Image` 的 I 要大写**，这是按库的文档来的。
- `images = []`：给自己一个空列表，用来装一、两或更多张图片。
- `for arg in sys.argv[1:]`：遍历命令行参数里的每一个词。
- `image = Image.open(arg)`：把这个参数传给 pillow 库的 `Image.open` 函数。
  - 这个库本质上是**以"给你很多操作能力（比如做动画）"的方式**打开那张图片。
- `images.append(image)`：把这张图片追加进 `images` 列表。

这个循环的命里任务就是：**遍历命令行参数，并用这个库把这些图片打开。**

### 20.5 最后一行：保存 GIF [01:27:30]

最后一行其实很直白：

- 我取出**第一张**图片（它在我的列表里位于位置 `0`），然后把它**保存到磁盘**上，也就是保存这个文件。
- **过去**我们用 CSV 或文本文件时，我得自己**打开文件**、自己**写文件**、甚至还得自己**关闭文件**。**用这个库我不需要做这些。** pillow 库把**打开、关闭、保存**都替我做了，我只要调 `save` 就行。

因为要传好几个参数、一行写不下，我把 `save` 调用拆到多行：

- `"costumes.gif"`：我想创建的**文件名**，这将是我的动画 GIF 的名字。
- `save_all=True`：告诉这个库，把我传给它的**所有帧**都保存下来 —— 第一个造型、第二个造型，如果我给了更多就更多。
- `append_images=[images[1]]`：把后面那张图**追加**到第一张图（`images[0]`）后面。这里有点小聪明：`images[1]` 就是第二张。
- `duration=200`：每一帧停留 **200 毫秒**。
- `loop=0`：**无限循环**。如果你指定 `loop=0`，意思是"不是循环有限的次数，而是循环无限次"。

### 20.6 关键细节：`sys.argv[1:]` [01:30:01]

还有一件事必须做：

> 回想一下，`sys.argv` 里不只装了"我在程序名后面敲的那些词"，它还装了什么？回想我们讲命令行参数时的讨论 —— 除了我即将敲进去的 `costume1.gif`、`costume2` 这些词，`sys.argv` 里还有什么？

**学生（McKenzie）**：还会有我们想运行的那个程序的**原名**，也就是 `costumes.py`。

**Malan 确认**：

> 正是。我们会拿到程序的原名，在这里是 `costumes.py` —— **它显然不是一个 GIF**。
>
> 所以记住：用 Python 的**切片**（slice）我们可以这么做。如果 `sys.argv` 是个列表，而我想拿到它的一个切片 —— **第一个元素之后的所有东西** —— 就写 `1:`。它的意思是：**从位置 1 开始**（不是 0），**一直切到最后**。
>
> 也就是"给我这个列表里除第一个元素以外的所有东西"，而按 McKenzie 的说法，第一个元素就是**程序的名字**。

### 20.7 运行 [01:31:00]

```bash
$ python costumes.py costume1.gif costume2.gif
```

**代码现在要做什么？** 复述一下：

- 用 `sys` 库访问命令行参数；
- 用 pillow 库把这些文件当作**图片**处理，并拥有这个库提供的全部功能；
- 用 `images` 这个列表**一张张**累加这些图片（从命令行来）；
- 第 7~9 行只是用一个循环遍历所有参数，用库打开它们之后加进列表；
- 最后一步（其实**就是一行代码，为了放得下被拆成了三行**）：保存第一张图，但请库把另一张图也追加到它后面 —— 不是 `[0]` 而是 `[1]`，如果还有更多我也可以照样列出来。
- 我想把所有这些文件**一起**保存；我想在每帧之间**暂停 200 毫秒**（五分之一秒）；我想让它**无限循环**。

**然后一如既往地祈祷，敲回车 —— 什么坏事都没发生，这几乎总是好事。**

```bash
$ code costumes.gif
```

在 VS Code 里打开最终生成的图片。我应该看到的是……**一只非常开心的猫？** 确实。

### 20.8 收尾 [01:32:00]

> 所以现在我们看到了：我们不光能**读写文件**（文本方式的），我们还能读写**由 0 和 1 组成的二进制文件**。
>
> 我们只是**浅尝辄止**。这里用的是 **pillow** 这个库。但这最终会赋予我们**以任意方式读写文件**的能力。
>
> 通过 File I/O，我们学会操作的**不只是**文本文件（TXT 或 CSV），**还有**二进制文件。这里碰巧是图片，但如果再深入一点，我们可以探索**音频、视频，以及更多** —— 一切都靠这些**简单的原语**，也就是这种" somehow 能读写文件"的能力。

---

## 本讲代码速查

```python
# ===== 1. 打开文件（写 / 追加 / 读）=====
file = open("names.txt", "w")   # w = write，写；文件不存在则创建；存在则重建（覆盖！）
file = open("names.txt", "a")   # a = append，追加到末尾
file = open("names.txt", "r")   # r = read，读（默认值，可以省略）
file = open("names.txt")        # 等价于 "r"

file.write(f"{name}\n")         # write 不会自动加换行，要自己写 \n
file.close()                    # 关闭并保存

# ===== 2. with：自动关闭文件 =====
with open("names.txt", "a") as file:
    file.write(f"{name}\n")
# 缩进块结束后，文件自动关闭

# ===== 3. 读文件 =====
with open("names.txt") as file:
    lines = file.readlines()    # 读出所有行，返回一个 list（每行含行尾 \n）

with open("names.txt") as file:
    for line in file:           # 逐行遍历，不用先 readlines()
        print("hello,", line.rstrip())   # rstrip() 去掉行尾空白（含 \n）

# ===== 4. 排序 =====
names = []
with open("names.txt") as file:
    for line in file:
        names.append(line.rstrip())

for name in sorted(names):                  # 正序
    print(f"hello, {name}")

for name in sorted(names, reverse=True):    # 倒序
    print(f"hello, {name}")

for line in sorted(file):                   # 直接对文件对象排序（更紧凑）
    print(line.rstrip())

# ===== 5. 手工解析 CSV =====
with open("students.csv") as file:
    for line in file:
        row = line.rstrip().split(",")      # split 返回 list
        print(f"{row[0]} is in {row[1]}")

with open("students.csv") as file:
    for line in file:
        name, house = line.rstrip().split(",")   # 序列解包，一次赋两个变量
        print(f"{name} is in {house}")

# ===== 6. 列表套字典 + 按字段排序 =====
students = []
with open("students.csv") as file:
    for line in file:
        name, house = line.rstrip().split(",")
        student = {}
        student["name"] = name
        student["house"] = house
        students.append(student)
        # 或一行版：students.append({"name": name, "house": house})

def get_name(student):
    return student["name"]

for student in sorted(students, key=get_name):       # key 传函数名，不加括号
    print(f"{student['name']} is in {student['house']}")

for student in sorted(students, key=get_name, reverse=True):
    ...

# ===== 7. lambda 匿名函数 =====
for student in sorted(students, key=lambda student: student["name"]):
    print(f"{student['name']} is in {student['house']}")

# ===== 8. csv 标准库 =====
import csv

# reader：每行返回 list
with open("students.csv") as file:
    reader = csv.reader(file)
    for row in reader:
        students.append({"name": row[0], "home": row[1]})
    # 或：for name, home in reader: ...

# DictReader：每行返回 dict（依据第一行的表头）
with open("students.csv") as file:
    reader = csv.DictReader(file)
    for row in reader:
        students.append({"name": row["name"], "home": row["home"]})
    # 或：students.append(row)

# writer：写入一行（传 list）
with open("students.csv", "a") as file:
    writer = csv.writer(file)
    writer.writerow([name, home])

# DictWriter：写入一行（传 dict，需指定 fieldnames）
with open("students.csv", "a") as file:
    writer = csv.DictWriter(file, fieldnames=["name", "home"])
    writer.writerow({"name": name, "home": home})

# ===== 9. 二进制 / 图片：PIL (Pillow) =====
import sys
from PIL import Image

images = []
for arg in sys.argv[1:]:        # [1:] 切掉程序名
    image = Image.open(arg)
    images.append(image)

images[0].save(
    "costumes.gif", save_all=True, append_images=[images[1]], duration=200, loop=0
)

# ===== 10. 常用终端命令 =====
# code names.py        在 VS Code 里新建/打开文件
# python names.py      运行程序
# rm names.txt         删除文件
# code names.txt       查看生成的文件
```

---

## 本讲易错点

1. **`"w"` 模式会"重建"文件，不只是"创建"。** 只要你用 `"w"` 打开，旧内容立即被清空。想一次次往里加，必须用 `"a"`（append）。这是本讲第一个翻车：跑了三次只剩最后一个 Ron。

2. **`write()` 不会自动换行，而 `print()` 会。** `print` 默认送给你一个行尾 `\n`（可用 `end=""` 覆盖），但 `file.write("Hermione")` 就只写 `Hermione`。想一行一条就要自己写 `f"{name}\n"`。

3. **读了文件再 `print`，会多出空行。** 因为文件里每行自带 `\n`，`print` 又加一个。经典解法是 `line.rstrip()`；讲师认为这比 `print(..., end="")` 设计上更干净（把文件格式这个"实现细节"剥掉，让 `print` 负责打印真正的名字）。

4. **想排序就不能边读边打印。** 一旦 `for line in file: print(...)`，排序"已经太晚"。必须先把所有数据读进内存（比如 `append` 进一个列表），排好序再输出。

5. **忘记 `close()` 可能损坏文件。** 用 `with open(...) as file:` 让 Python 自动关。注意变量是写在 `as` 后面的（这是语法规定，没有为什么），且操作文件的代码要**缩进**。

6. **按整个英文句子排序，只是"运气好"。** 把 `"Harry is in Gryffindor"` 这种整句塞进列表再排序，之所以结果对，只是因为英文从左往右读。正解是保留结构化数据（字典列表），最后再拼打印语句。

7. **`key=` 后面传的是函数"名字"，不能加括号。** `sorted(students, key=get_name)` 而不是 `key=get_name()`。`sorted` 会替你对列表里每个元素各调用一次这个函数，用它的**返回值**做比较。

8. **`split(",")` 遇到"数据里自带逗号"会崩。** `Number Four, Privet Drive` 会被切成三块，报 `ValueError: too many values to unpack`（因为你只准备了两个变量接）。换成竖线只是把问题推迟 —— 正解是用 `csv` 库，它会正确处理引号。

9. **f-string 里访问字典键要注意引号配对。** 外面用了双引号，里面的键就用单引号：`f"{student['name']} is in {student['house']}"`。字典索引用的是**字符串键**，不是 0/1 这样的数字下标。

10. **硬编码"第 0 列是 name、第 1 列是 home"很脆弱。** 别人（或 Excel）把列顺序一换，代码就崩。在 CSV 第一行写表头 + 用 `csv.DictReader`，代码就能"防御式"地继续工作，将来加列也不影响。

11. **`DictWriter` 必须给 `fieldnames`。** 因为字典本身无序，库需要你明确告诉它列顺序，才能把值写到正确的列上。而 `csv.writer` 则要你传**列表**、自己保证顺序。

12. **`sys.argv[0]` 是程序自己的名字。** 遍历命令行参数时要写 `sys.argv[1:]` 切片跳过它，否则 pillow 会试图把 `costumes.py` 当图片打开。

---

## 自检清单（写完后逐条确认）

- [x] 逐字稿从头到尾都消化了，没有整段跳过
- [x] 每个小标题都有时间标注
- [x] 所有演示代码都在笔记里，且能运行（代码均对照官方 Notes 还原）
- [x] 讲师演示时犯的错 / 强调的坑都写进去了（`"w"` 覆盖、不换行、双重换行、`too many values to unpack`、`row[0]` 难读、按整句排序是运气好）
- [x] 学生提问与回答全部保留（倒序排、限制数量、为何不自动 strip、能否改中间行、key 能否是变量、嵌套字典、lambda 两个问题、可读可写、写段落、用户选 key、换行符重要性、加列、单双引号、多文件、`append(row)`、CSV 出错怎么办）
- [x] 字数达标
- [x] 中文通顺，按中文习惯组织，没有逐句直译
- [x] 有「本讲速览」（主题 + 知识清单 + 时间轴）、「本讲代码速查」、「本讲易错点」
