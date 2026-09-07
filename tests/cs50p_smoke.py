# -*- coding: utf-8 -*-
"""CS50P 作业冒烟测试。

用法（在 D:\\llm-journey 下）：
    .venv\\Scripts\\python.exe tests\\cs50p_smoke.py

只验证「程序行为是否符合官方规格」，不验证写法好不好。
判定方式：expect 里给的每一行必须按顺序出现在 stdout 中。
"""

import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable

# (题目, 相对路径, stdin, 期望依次出现的行, 命令行参数, 是否跳过)
CASES = [
    # ---------------- Week 0 ----------------
    ("W0 einstein", "cs50p/week0/einstein.py", "1\n", ["E: 90000000000000000"]),
    ("W0 faces", "cs50p/week0/faces.py", "Hello :)\n", ["Hello 🙂"]),
    ("W0 indoor", "cs50p/week0/indoor.py", "HELLO\n", ["hello"]),
    ("W0 playback", "cs50p/week0/playback.py", "This is CS50\n", ["This...is...CS50"]),
    ("W0 tip", "cs50p/week0/tip.py", "50.00\n15%\n", ["Leave $57.50"]),

    # ---------------- Week 1 ----------------
    ("W1 bank", "cs50p/week1/bank.py", "Hello\n", ["$0"]),
    ("W1 bank-h", "cs50p/week1/bank.py", "Hi there\n", ["$20"]),
    ("W1 bank-other", "cs50p/week1/bank.py", "What's up?\n", ["$100"]),
    ("W1 deep", "cs50p/week1/deep.py", "forty two\n", ["Yes"]),
    ("W1 deep-no", "cs50p/week1/deep.py", "50\n", ["No"]),
    ("W1 extensions", "cs50p/week1/extensions.py", "happy.gif\n", ["image/gif"]),
    ("W1 extensions-x", "cs50p/week1/extensions.py", "file.bin\n", ["application/octet-stream"]),
    ("W1 interpreter", "cs50p/week1/interpreter.py", "5 / 2\n", ["2.5"]),
    ("W1 meal", "cs50p/week1/meal.py", "7:30\n", ["breakfast time"]),
    ("W1 meal-no", "cs50p/week1/meal.py", "11:11\n", []),

    # ---------------- Week 2 ----------------
    ("W2 camel", "cs50p/week2/camel.py", "firstName\n", ["first_name"]),
    ("W2 camel-plain", "cs50p/week2/camel.py", "name\n", ["name"]),
    ("W2 coke", "cs50p/week2/coke.py", "25\n25\n", ["Change Owed: 0"]),
    ("W2 nutrition", "cs50p/week2/nutrition.py", "apple\n", ["Calories: 130"]),
    ("W2 nutrition-2", "cs50p/week2/nutrition.py", "sweet cherries\n", ["Calories: 100"]),
    ("W2 plates-CS50", "cs50p/week2/plates.py", "CS50\n", ["Valid"]),
    ("W2 plates-CS05", "cs50p/week2/plates.py", "CS05\n", ["Invalid"]),
    ("W2 plates-CS50P", "cs50p/week2/plates.py", "CS50P\n", ["Invalid"]),
    ("W2 plates-dot", "cs50p/week2/plates.py", "PI3.14\n", ["Invalid"]),
    ("W2 plates-H", "cs50p/week2/plates.py", "H\n", ["Invalid"]),
    ("W2 plates-long", "cs50p/week2/plates.py", "OUTATIME\n", ["Invalid"]),
    ("W2 plates-A2", "cs50p/week2/plates.py", "A2\n", ["Invalid"]),   # 开头必须两个字母
    ("W2 plates-AA", "cs50p/week2/plates.py", "AA\n", ["Valid"]),
    ("W2 twttr", "cs50p/week2/twttr.py", "Twitter\n", ["Output: Twttr"]),

    # ---------------- Week 3 ----------------
    ("W3 fuel", "cs50p/week3/fuel.py", "3/4\n", ["75%"]),
    ("W3 fuel-E", "cs50p/week3/fuel.py", "1/100\n", ["E"]),
    ("W3 fuel-F", "cs50p/week3/fuel.py", "99/100\n", ["F"]),
    ("W3 fuel-retry", "cs50p/week3/fuel.py", "4/3\n1/2\n", ["50%"]),
    ("W3 grocery", "cs50p/week3/grocery.py", "apple\nbanana\napple\n",
     ["2 APPLE", "1 BANANA"]),
    ("W3 outdated-slash", "cs50p/week3/outdated.py", "9/8/1636\n", ["1636-09-08"]),
    ("W3 outdated-word", "cs50p/week3/outdated.py", "September 8, 1636\n", ["1636-09-08"]),
    ("W3 taqueria-run", "cs50p/week3/taqueria.py", "Taco\nTaco\n",
     ["Total: $3.00", "Total: $6.00"]),   # 每加一项都要打印累计
    ("W3 taqueria-menu", "cs50p/week3/taqueria.py", "baja taco\nTortilla Salad\n",
     ["Total: $4.25", "Total: $12.25"]),  # Baja Taco 2023 起为 4.25

    # ---------------- Week 4 ----------------
    ("W4 adieu-1", "cs50p/week4/adieu.py", "Liesl\n", ["Adieu, adieu, to Liesl"]),
    ("W4 adieu-3", "cs50p/week4/adieu.py", "Liesl\nFriedrich\nLouisa\n",
     ["Adieu, adieu, to Liesl, Friedrich, and Louisa"]),
    ("W4 bitcoin", "cs50p/week4/bitcoin.py", None, None, None, "需 CoinCap v3 API key"),
    ("W4 emojize", "cs50p/week4/emojize.py", ":1st_place_medal:\n", ["Output: 🥇"]),
    ("W4 figlet-ok", "cs50p/week4/figlet.py", "CS50\n", None, ["-f", "slant"], "人工看"),
    ("W4 figlet-bad", "cs50p/week4/figlet.py", "CS50\n", ["Invalid usage"],
     ["-f", "nosuchfont"]),
    ("W4 guessing", "cs50p/week4/guessing.py",
     "10\n" + "".join(f"{i}\n" for i in range(1, 11)), ["Just right!"]),
    ("W4 professor", "cs50p/week4/professor.py", "1\n" + "999\n" * 30, ["Score: 0/10"]),
]


def run(rel, stdin, args=None):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    p = subprocess.run(
        [PY, os.path.join(ROOT, rel)] + (args or []),
        input=(stdin or "").encode("utf-8"),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        env=env, timeout=60, cwd=ROOT,
    )
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")


def main():
    passed = failed = skipped = 0
    failures = []

    for case in CASES:
        name, rel, stdin, expect = case[0], case[1], case[2], case[3]
        args = case[4] if len(case) > 4 else None
        note = case[5] if len(case) > 5 else None

        if note:
            print(f"  -  {name:<20} 跳过（{note}）")
            skipped += 1
            continue

        try:
            rc, out, err = run(rel, stdin, args)
        except subprocess.TimeoutExpired:
            print(f"  ✗  {name:<20} 超时")
            failed += 1
            failures.append((name, "超时（可能在等输入）", ""))
            continue
        except Exception as e:                                  # noqa: BLE001
            print(f"  ✗  {name:<20} 运行异常: {type(e).__name__}")
            failed += 1
            failures.append((name, f"{type(e).__name__}", ""))
            continue

        # sys.exit("...") 写的是 stderr，所以要在 stdout+stderr 里一起找
        haystack = out + "\n" + err
        idx = 0
        ok = True
        for line in (expect or []):
            pos = haystack.find(line, idx)
            if pos < 0:
                ok = False
                break
            idx = pos + len(line)

        if ok and err.strip() and "EEE" not in err:
            pass  # 允许有 stderr（只要输出对）

        if ok:
            print(f"  ✓  {name}")
            passed += 1
        else:
            want = " / ".join(expect or [])
            got = out.strip().replace("\n", " ⏎ ")[:110]
            print(f"  ✗  {name:<20} 期望 [{want}]  实得 [{got}]")
            failed += 1
            failures.append((name, want, got))

    print()
    print(f"通过 {passed} / 失败 {failed} / 跳过 {skipped}")
    if failures:
        print()
        print("失败明细：")
        for n, w, g in failures:
            print(f"  {n}\n      期望: {w}\n      实得: {g}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
