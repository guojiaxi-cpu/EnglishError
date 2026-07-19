from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


PROJECT_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "scripts" / "paths.config.json"
QUESTION_HEADING = re.compile(
    r"^###\s*第\s*(?P<number>[^\s【]+?)\s*题\s*(?:【(?P<type>[^】]+)】)?\s*$",
    re.MULTILINE,
)


def configured_path(value: str, base_path: Path) -> Path:
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = base_path / path
    return path.resolve()


def load_vault_root(config_path: Path) -> Path:
    resolved_config = config_path.expanduser().resolve(strict=True)
    with resolved_config.open("r", encoding="utf-8") as config_file:
        config = json.load(config_file)
    return configured_path(config["vaultRoot"], resolved_config.parent)


def split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    normalized = text.lstrip("\ufeff")
    if not normalized.startswith("---\n"):
        return {}, normalized

    end = normalized.find("\n---", 4)
    if end < 0:
        return {}, normalized

    metadata: dict[str, str] = {}
    for line in normalized[4:end].splitlines():
        key, separator, value = line.partition(":")
        if separator:
            metadata[key.strip()] = value.strip()
    return metadata, normalized[end + 4 :].lstrip("\r\n")


def question_records(
    relative_path: str,
    metadata: dict[str, str],
    body: str,
) -> Iterable[dict[str, Any]]:
    matches = list(QUESTION_HEADING.finditer(body))
    if not matches:
        yield {
            "kind": "note",
            "relative_path": relative_path,
            "metadata": metadata,
            "content": body.strip(),
        }
        return

    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        block = body[match.start() : end].strip()
        block = re.sub(r"\n---\s*$", "", block).strip()
        yield {
            "kind": "question",
            "relative_path": relative_path,
            "metadata": metadata,
            "question_number": match.group("number"),
            "question_type": (match.group("type") or "").strip(),
            "content": block,
        }


def markdown_files(vault_root: Path) -> list[Path]:
    return sorted(
        (
            path
            for path in vault_root.rglob("*")
            if path.is_file() and path.suffix.lower() == ".md"
        ),
        key=lambda path: str(path.relative_to(vault_root)).casefold(),
    )


def collect(vault_root: Path) -> tuple[int, int, int]:
    files = markdown_files(vault_root)
    record_count = 0
    warning_count = 0

    for note_path in files:
        try:
            text = note_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            warning_count += 1
            print(f"WARNING: could not read {note_path}: {error}", file=sys.stderr)
            continue

        metadata, body = split_frontmatter(text)
        relative_path = str(note_path.relative_to(vault_root))
        for record in question_records(relative_path, metadata, body):
            print(json.dumps(record, ensure_ascii=False))
            record_count += 1

    return len(files), record_count, warning_count


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Read archived English-error Markdown notes and emit JSONL records."
    )
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH))
    parser.add_argument("--vault-root")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    config_path = Path(args.config)
    vault_root = (
        Path(args.vault_root).expanduser().resolve()
        if args.vault_root
        else load_vault_root(config_path)
    )

    if not vault_root.is_dir():
        raise NotADirectoryError(f"Vault root is not a directory: {vault_root}")

    file_count, record_count, warning_count = collect(vault_root)
    print(
        f"Collected {file_count} Markdown files, {record_count} records, "
        f"{warning_count} warnings from {vault_root}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, KeyError, ValueError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
