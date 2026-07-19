# EnglishError Project Instructions

These instructions apply when working in this repository (`EnglishError`).

## Archived Error Summary Routing

If the user submits the keyword “总结” or “汇总” and asks to summarize, classify, consolidate, or review archived English errors, use the `english-error-summary` skill at `.agents/skills/english-error-summary/SKILL.md`.

- This routing rule takes precedence over the normal root `SKILL.md` analysis workflow.
- Read every Markdown file under the `vaultRoot` configured in `scripts/paths.config.json`.
- Merge errors only when their underlying rule and error cause are substantively the same.
- Include the error type, explanation, and at most 10 original error examples for each merged type.
- Return the complete summary directly in the conversation.
- Do not preserve source files, create staging files, run archive commands, or write the summary to Obsidian.

## When To Apply `SKILL.md`

If the user's request is about English learning, wrong-answer analysis, exam questions (e.g., multiple choice, cloze, reading comprehension, error correction, writing), or producing "错题解析" style output, you must follow the guidance in `SKILL.md` by default (even if the user doesn't explicitly mention it).

If the user's request is unrelated to English error analysis (for example, repo tooling, scripts, git, CI), do not force the `SKILL.md` format.

## Output Requirements (English Error Analysis)

Follow `SKILL.md` for:

- What to analyze (question type specific points)
- The required standard output template (Markdown with sections)

Additional requirements:

- Keep the user's original language preference (Chinese unless they ask otherwise).
- When the user provides multiple questions, output one block per question using the template.
- If key info is missing (e.g., the original question text or options), ask for the minimal missing info and do not invent it.

## Source File Preservation

For every English analysis request that includes or references source files such as images, PDFs, Word documents, or text files:

- Run `python scripts/english_error_archive.py store-source` before analysis and pass every available source path through `--source-files`.
- Store the files under `source/YYYY-MM-DD/HHmmss/`, grouping all files from one request in the same run directory.
- Use the stored project copies for analysis and subsequent metadata, not the original external paths.
- Never overwrite an existing run directory or source file; use the script-generated suffix when a collision occurs.
- Keep all files under `source` permanently, including after failed, cancelled, or successful analysis and archive attempts. Never delete them automatically.
- If any source cannot be copied, report that specific failure accurately and continue with other successfully stored sources when possible.

## Script Configuration

- Read shared paths from `scripts/paths.config.json`; edit that file when the project, source, temporary, or Obsidian Vault location changes.
- Use `scripts/english_error_archive.py` as the only active workflow implementation.
- Use its `store-source` subcommand for source preservation and its `export-note` subcommand for Obsidian export.
- If the Python script fails, report the failure accurately and do not claim that the operation succeeded.

## Obsidian Recording Rules

When the user explicitly asks to save, record, archive, or write an English error analysis to Obsidian, treat the request as both an analysis task and a file-output task.

- Use the `vaultRoot` value from this project's `scripts/paths.config.json` as the fixed archive root.
- Complete question recognition and the full `SKILL.md` analysis before writing the note.
- State the complete recognized error-question list before archiving. Include marked-wrong, blank, unanswered, partially answered, and missing-keyword questions.
- Create one independent Markdown note per analysis request, including requests that contain multiple source images.
- Store notes in a `YYYY-MM-DD` directory based on the analysis execution date.
- Name notes with the next daily numeric index, zero-padded to at least three digits, such as `001.md`.
- Before archiving, write the complete analysis body as a UTF-8 Markdown staging file under the repository's `tmp` directory, never in the repository root.
- Name staging files `tmp/obsidian-analysis-YYYY-MM-DD-HHmmss.md`. If that name exists, append `-02`, `-03`, and so on instead of overwriting it.
- Keep staging files permanently after both successful and failed archive attempts; do not delete them automatically.
- Run `python scripts/english_error_archive.py export-note`; do not manually select or overwrite an archive filename.
- Pass the staging-file path through `--content-path`.
- Pass all recognized question numbers and stored source-file paths through `--question-numbers` and `--source-files` so they appear in YAML metadata.
- Ensure the response, `question_numbers` metadata, and archived analysis contain the same question set.
- Report the exact path only after the script succeeds. If the target is unavailable, permission is denied, or the script fails, report that the note was not archived.
- Because the fixed Vault is outside this repository, request the required filesystem approval before running the archive script when the environment requires it.
