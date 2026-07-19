---
name: english-error-analysis
description: 分析英语试卷、练习和图片中的错题、空白题及作答不完整题，按固定格式提供中文讲解；用户要求记录、保存或归档到 Obsidian 时，同时生成独立的错题笔记。
---

## 各题型分析要点

## 先做题目识别，再做讲解

- 必须先按题号顺序逐题检查图片中的作答情况，再开始讲解。
- 只要题目被明确标识为做错，或者该题没有写答案、答案空白、作答不完整，都必须视为错误并讲解。
- 不能只根据打叉、圈错、订正来判断错误；还必须主动检查是否有留空题。
- 连词成句、改写句子、填空题等主观题，只要漏写任一空、任一关键词，或整题未写，视同错误。
- 输出前必须再次核对整页题号，确认所有做错题和空白题都已覆盖，不能遗漏。
- 分析前输出完整原题，如果题目中有特殊符号或格式要求需要保留。

### 选择题
- 逐项分析每个选项为什么对/错
- 如何涉及发音，明确音标区别并举例
- 如果涉及语法，明确语法规则并举例
- 如果涉及词汇辨析，对比近义词的细微差别

### 填空题
- 判断考点：时态、语态、词性转换、固定搭配
- 给出填词依据（上下文线索、固定句型、时间状语等）
- 对词形变化题，列出完整的词形变化表（名词-动词-形容词-副词）

### 阅读理解
- 定位原文：指出答案在文中第几段第几句
- 区分题型：细节题/推断题/主旨题/词义猜测题
- 对推断题，解释推理逻辑链
- 对主旨题，说明如何排除以偏概全的选项

### 完形填空
- 结合上下文解释选择的依据
- 注意前后逻辑关系（因果、转折、并列、递进）
- 关注固定搭配和习惯用法

### 改错题
- 逐行分析错误类型（多词/缺词/错词）
- 解释正确用法的规则

### 阅读问答
- 读取原文：指出文中相关内容
- 分析问题：通过问题，结合原文分析答案
- 结合原文内容和意图，给出建议答案，词汇使用文中的词汇和初中范围词汇，范围不脱离原文内容
- 如果试题可由学生选择短文给出答案，首先按学生选择的问题给出建议答案，再将其他多个答案也给出建议答案
- 对细节型阅读问答题，建议答案优先采用“简洁、贴题、直接回答问题”的标准表达，不必为了显得完整而机械扩写；只要准确覆盖题干要求即可。例如：
  - `It can cause discomfort and make people less active.`
  - `Cold weather can lead to delays.`
  - `People might avoid outdoor activities such as picnics, sports and gardening during rainy days.`
  - `During heavy snowstorms or hurricanes.`
  - `People wear lighter fabrics in hot days and thicker clothes in cold climates.`
- 对动作类问答题（如 `What did ... do ...?`），建议答案优先保留动作发生的完整场景，不要只写最短动作动词；如果原文能明确动作对象或地点，答案应尽量写完整。例如：`She played in the school football team.` 优先于 `She played.`
- 对开放性问答题、推断题、续写式填空题，如果依据原文可以推出多个合理答案，不要只给唯一答案；应先给最贴合原文的建议答案，再补充其他合理表达。多个答案都必须不脱离原文含义，且尽量使用原文词汇或初中范围词汇。例如可接受：`listen to / think about / be more open to others' ideas or opinions or suggestions / make sure everyone enjoys the game / play by fair rules / think about what's fair for all`
- 对综合概括类阅读问答题，建议答案应优先满足题干条件，并允许保留概括性表达，不要求唯一措辞。例如：`To ensure safety and comfort, and to avoid potential disruptions.` 也可接受其他不脱离原文、逻辑成立、覆盖题干要求的答案。
- 对“可选择 story ① / story ② 作答”的阅读问答题，必须先根据学生实际选择的 story 和其作答内容进行分析，指出是否答偏、是否混入了另一则故事的信息，并先给出该同一 story 的建议答案；随后再补充其他未选择 story 的建议答案，供参考对比。
- 对这类“选一个故事并说明原因”的题，建议答案必须包含两层信息：`人物想改变规则的直接原因` + `人物内心的理由或价值判断`，不能只写一句笼统判断。例如可写：
  - `In story ①, the boy wants to change his father's rule because he feels sick after eating what he hates. He thinks the old rule is too strict, and he wants his children to choose what they eat so they don't feel bad like he did.`
  - `In story ②, the girl wants to change the rule because she thinks it's not fair. She believes everyone should be allowed to play in the school team, not just boys.`

### 作文
- 从内容、结构、语言三个维度指出问题
- 给出修改建议和范文参考1，词汇限定在初中词汇范围
- 给出修改建议和范文参考2

## 输出格式要求

### 单个错题的标准输出格式

```markdown
---

### 第X题 【题型名称】

**📝 题目原文**
[完整题目内容；如果有划线部分，必须用 <u>...</u> 标出，并使用斜体。若无法确认划线内容，写明：图片中划线部分无法确认。]

**❌ 你的答案**：[错误答案]  
**✅ 正确答案**：[正确答案]

**🔍 错误原因分析**
[类型：知识型/理解型/技巧型]
[具体原因说明，2-4句话解释清楚为什么会错]

**📖 知识点讲解**
[详细的知识点说明，搭配例句]

**🧭 解题步骤**
1. 第一步...
2. 第二步...
3. 第三步...

**💭 帮你记住**
[一句话口诀、对比表格、或额外例句]

---
```

## 输出前自检清单

- 我是否先按题号顺序检查了图片中的每一道题？
- 我是否识别了所有打叉、圈错、订正、空白、漏写的题目？
- 我是否把“空白未答”也当作错误进行了讲解？
- 主观题中，我是否检查了是否存在“部分作答但答案不完整”的情况？
- 最终输出的题号，是否与图片里所有错误题号一一对应？
- 最终输出的题目，是否与原题完全一致？

## Obsidian 归档规则

- 仅当用户明确要求“保存”“记录”“归档”或“写入 Obsidian”时执行归档；普通错题分析只在对话中输出。
- 固定归档根目录使用本项目目录 `scripts/paths.config.json` 文件中的 `vaultRoot` 值。
- 使用本次分析执行日期建立 `YYYY-MM-DD` 子目录，不使用图片拍摄日期或试卷日期代替。
- 每次分析请求生成一篇独立 Markdown 文件；同一请求包含多张图片时，仍只生成一篇文件。
- 文件名使用当日递增的三位序号：`001.md`、`002.md`、`003.md`。先扫描日期目录中的纯数字 Markdown 文件，再从最大序号加一。
- 归档前先明确列出本次识别到的全部错题题号。打叉、圈错、订正、答案空白、整题未答、漏写任一空或关键词、作答不完整的题目都必须计入。
- 对话中讲解的题号集合、归档元数据中的 `question_numbers` 和归档正文中的题目必须完全一致。
- 归档正文必须保存完整分析，不得改写成摘要；正文继续使用本文件规定的单题标准输出格式。
- 从 `scripts/paths.config.json` 读取项目及 Obsidian 路径；路径变化时只修改该配置文件。
- 使用 `python scripts/english_error_archive.py export-note` 完成目录创建、序号分配、YAML frontmatter 生成和文件写入，不手工拼接目标文件名。
- 调用脚本前，将只包含完整分析正文的 UTF-8 Markdown 中间文件写入项目 `tmp` 目录，不得写在项目根目录或 Obsidian 目标目录。
- 中间文件命名为 `tmp/obsidian-analysis-YYYY-MM-DD-HHmmss.md`；如果同名文件已经存在，在时间戳后追加 `-02`、`-03` 等递增序号，禁止覆盖已有文件。
- 将该中间文件通过 `--content-path` 传入脚本，并通过 `--question-numbers` 传入全部错题题号，通过 `--source-files` 传入 `source` 目录中的来源副本路径。
- 无论 Obsidian 归档成功或失败，都保留 `tmp` 中间文件，不自动删除，便于核查和重新归档。
- 脚本成功后向用户报告实际保存的绝对路径。脚本失败、目录不可访问或写入未获授权时，明确报告未归档，不得声称已保存。

## 来源文件保存规则

- 用户提供或指定的图片、PDF、Word、文本及其他题目来源文件，必须先复制到项目 `source` 目录，再进行识别、分析或归档。
- 从 `scripts/paths.config.json` 读取项目及来源目录路径；路径变化时只修改该配置文件。
- 使用 `python scripts/english_error_archive.py store-source` 保存来源文件，并通过 `--source-files` 传入全部来源路径；不手工决定目标目录或覆盖同名文件。
- 按本次执行日期和时间保存到 `source/YYYY-MM-DD/HHmmss/`。同一请求的多个来源文件放在同一个时间目录中。
- 如果时间目录已存在，在目录名后追加 `-02`、`-03` 等递增序号；同一批次出现同名文件时，在文件名后追加递增序号，禁止覆盖。
- 保存后使用项目 `source` 中的副本进行后续分析，并将副本绝对路径写入 Obsidian 笔记的 `source` 元数据。
- 来源文件与 `tmp` 中间文件一样永久保留。无论分析或 Obsidian 归档成功、失败或取消，都不得自动删除。
- 如果来源文件无法读取或复制，明确报告未保存的文件，不得声称来源已经归档；可读取的其他文件仍可继续保存。

## 脚本执行规则

- 正式流程只使用 `scripts/english_error_archive.py`，通过 `store-source` 和 `export-note` 两个子命令完成原有功能。
- Python 脚本执行失败时明确报告错误，不得声称操作已经成功。
- 脚本功能、路径配置、文件保留策略、命名规则和 Obsidian 元数据格式保持不变。
