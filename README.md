# EnglishError

- EnglishError 是一个面向中学生的英语错题整理与解析的本地工作流项目。它用于保存题目来源文件、按项目约定生成错题解析，并在需要时导出 Markdown笔记到指定目录，如Obsidian。
- 通过识别英语试卷错题等图片，对错题进行分析和讲解，生成原题、错误答案、正确答案、错误原因分析、知识点讲解、解题步骤、辅助记忆；针对不同题型有不同的重点分析。
- 根据提示词是否有“记录、保存、归档、Obsidian”关键词，生成markdown笔记到指定目录，文件按生成日期分类，三位序号文件文档。后续可以继续使用skill对记录进行汇总分析，形成复习材料。
- 原错题图片等保存在source目录，过程中文件保存在tmp目录，用户根据情况进行清理。
-根据提示词是否有“汇总/总结”关键词，对指定目录的归档文件，进行总结分析，按错误类型进行归类汇总，做二次分析。分析结果直接展现，不再归档。

## 核心功能

- **错题识别**：逐题检查学生作答，识别明确做错、答案空白、整题未答、漏写和作答不完整的题目。
- **规范讲解**：按照根目录 `SKILL.md` 的题型规则，生成原题、学生答案、正确答案、错误原因、知识点、解题步骤和辅助记忆等内容。
- **来源保留**：将图片等来源文件复制到项目的 `source` 目录，并长期保留。
- **Obsidian 归档**：每次分析生成一篇独立 Markdown 笔记，按执行日期和当日递增序号保存到配置的 Vault 目录。
- **错题汇总**：用户提交“总结”或“汇总”时，读取错题库中的全部 Markdown 笔记，将底层规则和错误原因相同的错题合并，直接输出分类复习材料。

## 工作流程

### 错题分析与归档

1. 使用 `scripts/english_error_archive.py store-source` 将本次来源文件保存到 `source/YYYY-MM-DD/HHmmss/`。
2. 使用保存后的项目副本识别题目，并按照根目录 `SKILL.md` 完成分析和讲解。
3. 在对话中显示本次完整错题分析及识别到的题号。
4. 用户明确要求保存、记录、归档或写入 Obsidian 时，将完整分析写入 `tmp` 中的 Markdown 中间文件。
5. 使用 `scripts/english_error_archive.py export-note` 创建 Obsidian 笔记，并返回实际保存路径。

一次分析请求只生成一篇 Obsidian 笔记，即使本次请求包含多个来源文件。归档笔记采用 `YYYY-MM-DD/001.md`、`002.md` 等结构，当日序号由脚本自动计算。

`source` 中的来源文件和 `tmp` 中的中间文件在成功、失败或取消后都不会自动删除。

### 错题库总结

当用户使用“总结”或“汇总”并要求统计、分类、合并或复盘已经归档的英语错题时，`AGENTS.md` 会将任务路由到独立的 `english-error-summary` Skill。该流程会：

1. 递归读取 `scripts/paths.config.json` 中 `vaultRoot` 下的全部 Markdown 文件。
2. 按底层语法规则、知识点和实际错误原因归类。
3. 只合并本质上属于同一种错误的题目。
4. 为每个错误类型输出讲解，并列出最多 10 个原错误例句。
5. 将完整总结直接显示在对话中，不创建来源副本、中间文件或新的 Obsidian 笔记。

单张试卷解析或新增错题归档仍使用根目录 `SKILL.md`，不会调用汇总 Skill。

## 环境要求

- Python 3.11 或更高版本
- Python 标准库
- Git，用于项目版本管理

项目当前使用 Python 脚本执行，归档是指定路径，Obsidian不是必须软件。

## 路径配置

首次使用时，将 `scripts/paths.config.example.json` 复制为 `scripts/paths.config.json`，然后根据本机目录修改配置：

```json
{
  "projectRoot": "..",
  "sourceDirectory": "source",
  "tempDirectory": "tmp",
  "vaultRoot": "C:\\Users\\your-name\\Obsidian Vault\\raw\\10_English错题本"
}
```

- `projectRoot`：项目根目录，相对于配置文件所在目录解析。
- `sourceDirectory`：来源文件保存目录，可使用相对于项目根目录的路径。
- `tempDirectory`：归档前 Markdown 中间文件目录。
- `vaultRoot`：Obsidian 英语错题库根目录，也是汇总 Skill 的读取范围。

`scripts/paths.config.json` 包含本机绝对路径，不应提交到公共仓库。

## 使用方式

### 对话中分析并归档

项目提供了 [prompt_run.md](prompt_run.md)，其中保存了推荐的完整提示词。提交题目图片或其他来源文件后，可以要求 Codex 完成错题识别、讲解并归档到 Obsidian。

常用提示词示例：

```text
你是一名英语老师。根据本次图片逐题检查学生作答，识别所有明确做错、答案空白、整题未答、漏写以及作答不完整的题目。严格按照本项目 SKILL.md 进行分析和讲解。完成后，将本次完整错题分析显示出来并归档到 Obsidian。
```
### 对话中汇总错题库

```text
总结全部英语错题，按错误类型归类并合并相同错误。
```

或：

```text
汇总错题本，输出每类错误的讲解和最多 10 个原错误例句。
```

汇总结果只在当前对话中显示，不会自动写回 Obsidian。

### 手工运行 Python 脚本

保存一个或多个来源文件：

```text
python scripts/english_error_archive.py store-source --source-files "C:\path\paper.jpg" "C:\path\questions.pdf"
```

将已经生成的 Markdown 中间文件归档到 Obsidian：

```text
python scripts/english_error_archive.py export-note --content-path "tmp\obsidian-analysis-2026-07-19-120000.md" --question-numbers 36 37 47 --source-files "source\2026-07-19\120000\paper.jpg"
```

收集错题库内容供汇总 Skill 分析：

```text
python .agents/skills/english-error-summary/scripts/collect_archived_errors.py --config scripts/paths.config.json
```

收集脚本以 JSONL 输出笔记内容，通常由 Codex 根据汇总 Skill 自动调用，不需要手工执行。

## 项目结构

```text
EnglishError/
|-- .agents/
|   `-- skills/
|       `-- english-error-summary/
|           |-- SKILL.md
|           |-- agents/
|           |   `-- openai.yaml
|           `-- scripts/
|               `-- collect_archived_errors.py
|-- scripts/
|   |-- english_error_archive.py
|   |-- paths.config.json
|-- source/
|   `-- YYYY-MM-DD/HHmmss/
|-- Tmp/
|-- AGENTS.md
|-- SKILL.md
|-- prompt_advice.md
|-- README.md
|-- .gitignore
`-- LICENSE
```

- `.agents/skills/english-error-summary/`：独立的错题库汇总 Skill，包含执行规范、界面元数据和只读收集脚本。
- `scripts/english_error_archive.py`：活动工作流的唯一执行脚本，负责保存来源文件和导出 Obsidian 笔记。
- `scripts/paths.config.json`：本机实际路径配置；示例文件用于初始化配置。
- `source/`：按请求保存原始图片、PDF、Word 等来源文件，不自动删除。
- `Tmp/`：保存归档前的完整 Markdown 中间文件。配置中使用 `tmp`，Windows 文件系统不区分目录名大小写。
- `AGENTS.md`：项目级路由和执行规则，决定何时使用普通错题分析或独立汇总 Skill。
- `SKILL.md`：单次英语题目识别、错误判定、讲解内容和输出格式规范。
- `prompt_advice.md`：可复用的完整错题分析与归档提示词。

## 数据与安全

- 项目不会自动删除 `source` 或 `tmp` 下的文件。
- 汇总流程只读取 `vaultRoot`，不会修改原有错题笔记。
- Obsidian Vault 位于项目目录之外时，运行环境可能要求用户批准文件系统访问。
- 对外发布前，请检查 `scripts/paths.config.json`、来源文件和中间文件中是否包含个人路径或隐私信息。

## License

本项目使用 [MIT License](LICENSE)。
