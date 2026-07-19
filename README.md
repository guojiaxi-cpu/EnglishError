# EnglishError

EnglishError 是一个面向英语错题整理与解析的本地工作流项目。它用于保存题目来源文件、按项目约定生成错题解析，并在需要时导出 Markdown 笔记到 Obsidian。

## 功能

- 保存图片、PDF、文档等错题来源文件到本地 `source/` 目录。
- 按 `SKILL.md` 中的格式要求生成英语错题解析。
- 通过脚本将解析内容导出为 Obsidian Markdown 笔记。
- 使用配置文件管理项目路径、临时目录和 Obsidian Vault 路径。

## 环境要求

- Python 3.11 或更高版本
- Git

## 配置

首次使用前，复制示例配置文件：

```powershell
Copy-Item scripts\paths.config.example.json scripts\paths.config.json
```

然后编辑 `scripts\paths.config.json`，把 `vaultRoot` 改成你自己的 Obsidian 归档目录。

`scripts\paths.config.json` 包含本机路径，默认不会提交到 Git。

## 使用

保存来源文件：

```powershell
python scripts\english_error_archive.py store-source --source-files path\to\source.jpg
```

导出 Obsidian 笔记：

```powershell
python scripts\english_error_archive.py export-note --content-path tmp\analysis.md --question-numbers 1 2 --source-files source\2026-07-19\120000\example.jpg
```

## 开源注意事项

不要提交真实错题图片、临时文件、本机路径配置或私人 Obsidian Vault 路径。默认 `.gitignore` 已排除这些内容。

## License

This project is licensed under the MIT License.
