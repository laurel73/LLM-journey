# LLM-journey

季秋的学习仓库：从 Python 基础 → 深度学习 → 大模型工程师。

主线排期见《LLM 学习执行手册-零基础落地版》，完整书单与课程体系见《LLM 职业化学习路线图》。

## 目录

| 目录 | 内容 |
|---|---|
| `cs50p/` | CS50's Introduction to Programming with Python（哈佛 Python 课）作业，按周归档 |
| `week01/` | 《动手学深度学习》配套练习（d2l 第 2 章预备知识） |
| `log/` | 每周学习日志（`YYYY-WW.md`） |
| `tests/` | 作业自测脚本（在电脑上跑，手机上跑不了） |
| `.venv/` | Python 虚拟环境（已 gitignore，不入库） |

## 当前进度

- **Python 基础**：CS50P Week 0 ~ Week 5 已完成（25 题 + 4 个测试文件）
  - 2026-09-06 中午开课，两天做到 Week 4，节奏很快
- **深度学习地基**：d2l 第 2 章（09-05 才排进计划，尚未开始）

## 作业归档流程（手机 → 电脑）

1. 手机上写完作业，打包成 `cs50p_weekN.zip` 之类的压缩包，传到电脑桌面。
2. 说一句「整理桌面作业」，我负责：解压 → 按周归档到对应目录 → 更新进度 → `git add` / `commit` / `push`。
3. 原始压缩包保留在桌面不动，作为备份。

压缩包命名约定：`cs50p_weekN.zip`（N 是周次）。换课之后照此推广，比如 `d2l_week2.zip`。

## 自测

手机上写完没法真正运行，所以在电脑上跑一遍：

```
.venv\Scripts\python.exe tests\cs50p_smoke.py
```

覆盖 CS50P W0–W4 全部 25 题、44 个用例，对照官方规格校验输出。
官方的 `check50` 在 Windows 上装不起来（依赖 Unix 的 `termios`），所以这个脚本是替代品。
