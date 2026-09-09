# CS50P 作业进度

课程：CS50's Introduction to Programming with Python（哈佛）
Python 基础阶段的正式教材，替代原计划的《Python 编程：从入门到实践》——有作业、有自动判分、有反馈，比单纯读书强。

**开课：2026-09-06（周日）中午。** 到 09-07 为止累计 25 题，全部是两天内新做的。

## 已知问题（待修，2026-09-07 实测）

跑 `tests/cs50p_smoke.py` 对照官方规格发现 3 个会判错的地方：

| 文件 | 现象 | 规格要求 | 修法提示 |
|---|---|---|---|
| `week2/plates.py` | 输入 `A2` 输出 `Valid` | 开头必须**至少两个字母** | 现在只查了 `plate[0]`，要查前两个字符 |
| `week3/taqueria.py` | 只在结束时打印一次总价 | 每输入一项就打印一次累计 | `print` 要挪进循环里 |
| `week3/taqueria.py` | Baja Taco 记成 `4.00` | 2023-10-25 起官方改为 `4.25` | 改菜单字典即可 |

另有两处不影响判分的隐患，顺手可以一起处理：
- `week2/plates.py`：输入空行时 `plate[0]` 会 IndexError（长度校验在前，但取首字符没做保护）。
- `week4/bitcoin.py`：用的是 CoinDesk v1 接口，**该接口已下线**，且现行规格要求 CoinCap v3 + 自己的 API key，需要改。

## 周进度

| 周 | 主题 | 状态 | 作业 |
|---|---|---|---|
| W0 | Functions, Variables | ✅ 完成 | indoor, playback, einstein, tip, faces |
| W1 | Conditionals | ✅ 完成 | deep, bank, extensions, interpreter, meal |
| W2 | Loops | ✅ 完成 | camel, coke, nutrition, plates, twttr |
| W3 | Exceptions | ✅ 完成 | fuel, grocery, outdated, taqueria |
| W4 | Libraries | ✅ 完成 | adieu, bitcoin, emojize, figlet, guessing, professor |
| W5 | Unit Tests | ✅ 完成 | bank, fuel, plates, twttr + 4 个测试文件 |
| W6 | File I/O | ✅ 完成 | lines, pizza, scourgify, shirt |
| W7 | Regular Expressions | ✅ 完成 | numb3rs, response, um, watch, working |
| W8 | Object-Oriented Programming | ✅ 完成 | jar, seasons, shirtificate |
| W9 | Et Cetera | ⬜ 讲座 | 无作业 |

## 目录说明

- `weekN/` —— 该周正式作业，文件名与课程要求一致（英文 snake_case）
- `practice/` —— 随堂练习与自选题，文件名暂用中文，来源明确的之后再归位

## 已提交的作业

**Week 0（Functions, Variables）** — 2026-09-06
- `indoor.py` — 判断是否在室内
- `playback.py` — 把输入里的空格换成三个点
- `einstein.py` — E = mc²
- `tip.py` — 计算小费（支持输入带 % 号）
- `faces.py` — 把 `:)` `:(` 转成 emoji

**Week 1（Conditionals）** — 2026-09-06
- `deep.py` — 生命、宇宙及一切的答案是 42
- `bank.py` — 问候语金额换算
- `extensions.py` — 根据扩展名输出 MIME 类型
- `interpreter.py` — 数学表达式解释器
- `meal.py` — 判断当前是否是用餐时间

**Week 2（Loops）** — 2026-09-07
- `camel.py` — camelCase 转 snake_case
- `coke.py` — 投币找零循环
- `nutrition.py` — 查水果热量
- `plates.py` — 车牌号合法性校验
- `twttr.py` — 去掉元音

**Week 3（Exceptions）** — 2026-09-07
- `fuel.py` — 分数转百分比，含 X/Y 与小数异常处理
- `grocery.py` — 统计清单数量，忽略大小写
- `outdated.py` — 日期格式转换，含月份单词与 9/8 格式
- `taqueria.py` — 点餐计价，忽略无效菜品

**Week 4（Libraries）** — 2026-09-07
- `adieu.py` — 告别名单（`inflect.join` 自动处理 and / 牛津逗号）
- `bitcoin.py` — 调 CoinCap API 查询比特币价格
- `emojize.py` — `:code:` 转 emoji
- `figlet.py` — ASCII 艺术字体
- `guessing.py` — 猜数字
- `professor.py` — 从 YouTube 链接提取视频 ID

> Week 4 依赖 `emoji` `pyfiglet` `inflect` 三个第三方库，已在 `D:\llm-journey\.venv` 装好（2026-09-07）。

**Week 5（Unit Tests）** — 2026-09-07
把前面几题重构成可测试的纯函数，再为它们写测试：

- `bank.py` / `test_bank.py`
- `fuel.py` / `test_fuel.py`
- `plates.py` / `test_plates.py`
- `twttr.py` / `test_twttr.py`

> 本机补装了 `pytest`。跑法：`.venv\Scripts\python.exe -m pytest cs50p/week5 -q`
> 实测 15 passed。
> ⚠️ `plates.py` 的「开头必须两个字母」这条仍未修（`cs50p/README.md` 已知问题表），
> 自己的 `test_plates.py` 也没覆盖这个用例，所以测试全绿但规格仍不满足。

**Week 6（File I/O）** — 2026-09-08

- `lines.py` — 统计 .py 文件的有效代码行数（跳过空行与注释行）
- `pizza.py` — 读 CSV 菜单，用 `tabulate` 输出 grid 表格
- `scourgify.py` — 把 `name` 列拆成 `first` / `last` 两列并写出新 CSV
- `shirt.py` — 用 `PIL` 把衬衫图叠到人像上（`ImageOps.fit` + `paste`）

> 本机补装了 `tabulate`（`pizza.py` 依赖）。
> `shirt.py` 需要 `shirt.png` 和一张人像照片，这两个资源官方只在 codespace 里提供，
> 本地没有，所以这题在本机跑不起来——不是代码问题。

**Week 7（Regular Expressions）** — 2026-09-09

- `numb3rs.py` — 校验 IPv4 地址（四段 0–255）
- `response.py` — 用 `validators` 校验邮箱格式
- `um.py` — 统计独立单词 "um" 的出现次数（词边界，非子串）
- `watch.py` — 从 YouTube 链接提取视频 ID，还原成 `youtu.be/<id>` 短链
- `working.py` — 解析 "9 AM to 5 PM" 这类时间区间，换算成 24 小时制

> 本机补装了 `validators`（`response.py` 依赖）。

**Week 8（Object-Oriented Programming）** — 2026-09-09

- `jar.py` — `Jar` 类：容量校验、`deposit` / `withdraw` 抛 `ValueError`、`@property` 暴露属性、`__str__` 输出 🍪
- `seasons.py` — 输入出生日期，输出活了多少分钟（`datetime` 相减 + `inflect` 拼英文数字）
- `shirtificate.py` — 用 `fpdf` 生成 CS50 衬衫证书 PDF

> 本机补装了 `fpdf2`（导入名是 `fpdf`）。
> `shirtificate.png` 已从 CS50 官网取回放进 `week8/`，配上 `fpdf2` 后这题在本机可以跑通了。
> ⚠️ 本人自述这题大比例借助 AI 完成、没有自己收尾——代码逻辑未逐行核对，回头有空再看。

**结课自测 · TinySearch** — 2026-09-09

- `practice/tinysearch.py` — 一个 60 行左右的迷你文本检索器，纯标准库（`math` / `re`）
- 流程：分词 → 建词表 → 词袋向量化 → 余弦相似度 → 取 top-3
- `practice/结课自测-TinySearch.md` — 完整任务说明
- `practice/tinysearch_v1.py` — 我整理的对照版（同功能，仅作参考）

> 跑法：`.venv\Scripts\python.exe practice\tinysearch.py`，输入一句中文即可
> 自评：练习目的不在算法而在手感——dict 编号、list 装数字、函数要 `return 值`、`enumerate` 出对偶
> 进度：Steps 1/2/3 + 主流程完成，class 封装（Vec / Doc / TinySearch）**主动延后**——
> 他自评「Class 是啥我也会写，但前面这些函数的变量不知道怎么串起来」，等真到了
> 「散装函数太多串不起来」再回来包 class，比硬上更划算
