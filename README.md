# EnglishError

- EnglishError 是一个面向中学生的英语错题整理与解析的本地工作流项目。它用于保存题目来源文件、按项目约定生成错题解析，并在需要时导出 Markdown 笔记到 Obsidian。
- 通过识别英语试卷错题等图片，对错题进行分析和讲解，生成原题、错误答案、正确答案、错误原因分析、知识点讲解、解题步骤、辅助记忆；针对不同题型也有不同的分析模式。
- 根据提示词是否有“记录、保存、归档、Obsidian”关键词，生成markdown笔记到指定目录，文件按生成日期分类，三位序号文件文档。后续可以继续使用skill对记录进行汇总分析，形成复习材料。
- 原错题图片等保存在source目录，过程中文件保存在tmp目录，用户根据情况进行清理。

## 功能

- 保存图片等错题来源文件到本地 `source/` 目录。
- 按 `SKILL.md` 中的格式要求生成英语错题解析。
- 通过脚本将解析内容导出为 Obsidian Markdown 笔记。
- 使用配置文件管理项目路径、临时目录和 Obsidian Vault 路径。

## 环境要求

- Python 3.11 或更高版本
- Git

## 配置

首次使用前，复制示例配置文件：

```path
Copy-Item scripts\paths.config.example.json scripts\paths.config.json
```

然后编辑 `scripts\paths.config.json`，把 `vaultRoot` 改成你自己的 Obsidian 归档目录。

`scripts\paths.config.json` 包含本机路径，默认不会提交到 Git。

## 使用

按结构配置后，只需要通过提示词对话自动完成分析，归档。如：
“你是一名英语老师。请根据图片逐题检查学生作答，识别所有明确做错、答案空白、整题未答、漏写以及作答不完整的题目。严格按照本项目 SKILL.md 进行分析和讲解。
完成后，将本次完整错题分析显示出来，并且归档到Obsidian。每次分析生成一篇独立笔记，按照执行日期和当日递增序号保存。归档成功后告诉我识别到的错题题号和实际保存路径。” 

其他说明：

保存来源文件：

```python
python scripts\english_error_archive.py store-source --source-files path\to\source.jpg
```

导出 Obsidian 笔记：

```python
python scripts\english_error_archive.py export-note --content-path tmp\analysis.md --question-numbers 1 2 --source-files source\2026-07-19\120000\example.jpg
```

## 开源注意事项

不要提交真实错题图片、临时文件、本机路径配置或私人 Obsidian Vault 路径。默认 `.gitignore` 已排除这些内容。

## License

This project is licensed under the MIT License.

## 分析讲解摘要

