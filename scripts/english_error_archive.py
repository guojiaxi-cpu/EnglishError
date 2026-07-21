from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Iterable


DEFAULT_CONFIG_PATH = Path(__file__).with_name("paths.config.json")
DEFAULT_TAGS = ("英语", "错题本")


def configured_path(value: str, base_path: Path) -> Path:
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = base_path / path
    return path.resolve()


def load_paths(config_path: str | Path) -> dict[str, Path]:
    resolved_config = Path(config_path).expanduser().resolve(strict=True)
    with resolved_config.open("r", encoding="utf-8") as config_file:
        config = json.load(config_file)

    project_root = configured_path(config["projectRoot"], resolved_config.parent)
    return {
        "project_root": project_root,
        "source_root": configured_path(config["sourceDirectory"], project_root),
        "temp_root": configured_path(config["tempDirectory"], project_root),
        "vault_root": configured_path(config["vaultRoot"], resolved_config.parent),
    }


def parse_date(value: str | None) -> datetime:
    if value is None:
        return datetime.now().astimezone()

    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        parsed = parsed.astimezone()
    return parsed


def available_file_path(directory: Path, file_name: str) -> Path:
    candidate = directory / file_name
    if not candidate.exists():
        return candidate

    source_name = Path(file_name)
    suffix = 2
    while True:
        candidate = directory / f"{source_name.stem}-{suffix:02d}{source_name.suffix}"
        if not candidate.exists():
            return candidate
        suffix += 1


def create_run_directory(source_root: Path, run_date: datetime) -> Path:
    date_directory = source_root / run_date.strftime("%Y-%m-%d")
    date_directory.mkdir(parents=True, exist_ok=True)
    run_name = run_date.strftime("%H%M%S")
    suffix = 1

    while True:
        directory_name = run_name if suffix == 1 else f"{run_name}-{suffix:02d}"
        run_directory = date_directory / directory_name
        try:
            run_directory.mkdir()
            return run_directory
        except FileExistsError:
            suffix += 1


def store_source_files(
    source_files: Iterable[str], source_root: Path, run_date: datetime
) -> list[Path]:
    readable_sources: list[Path] = []
    for source_file in source_files:
        try:
            resolved_source = Path(source_file).expanduser().resolve(strict=True)
            if not resolved_source.is_file():
                raise ValueError("path is not a file")
            readable_sources.append(resolved_source)
        except (OSError, ValueError) as error:
            print(f"WARNING: source file was skipped: {source_file} ({error})", file=sys.stderr)

    if not readable_sources:
        raise RuntimeError("No readable source files were provided.")

    run_directory = create_run_directory(source_root, run_date)
    stored_paths: list[Path] = []
    for source_path in readable_sources:
        destination = available_file_path(run_directory, source_path.name)
        try:
            shutil.copy2(source_path, destination)
            stored_paths.append(destination.resolve())
        except OSError as error:
            print(f"WARNING: source file was skipped: {source_path} ({error})", file=sys.stderr)

    if not stored_paths:
        raise RuntimeError("No source files were stored.")
    return stored_paths


def yaml_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def yaml_list(values: Iterable[str]) -> str:
    items = [yaml_quote(str(value)) for value in values]
    return "[" + ", ".join(items) + "]"


def next_note_index(date_directory: Path, date_prefix: str) -> int:
    prefix = f"{date_prefix}-"
    indexes = [
        int(path.stem.removeprefix(prefix))
        for path in date_directory.glob("*.md")
        if path.is_file()
        and path.stem.startswith(prefix)
        and path.stem.removeprefix(prefix).isdigit()
    ]
    return max(indexes, default=0) + 1


def export_note(
    content_path: Path,
    vault_root: Path,
    run_date: datetime,
    question_numbers: Iterable[str],
    source_files: Iterable[str],
    tags: Iterable[str],
    title: str | None,
) -> Path:
    resolved_content = content_path.expanduser().resolve(strict=True)
    if resolved_content.suffix.lower() != ".md":
        raise ValueError(f"Content path must be a Markdown file: {resolved_content}")

    body = resolved_content.read_text(encoding="utf-8").strip()
    if not body:
        raise ValueError(f"The Markdown content file is empty: {resolved_content}")

    date_text = run_date.strftime("%Y-%m-%d")
    date_prefix = run_date.strftime("%Y%m%d")
    date_directory = vault_root / date_text
    date_directory.mkdir(parents=True, exist_ok=True)
    note_index = next_note_index(date_directory, date_prefix)

    while True:
        index_text = f"{note_index:03d}"
        note_title = title.strip() if title and title.strip() else (
            f"英语错题分析 {date_text} #{index_text}"
        )
        frontmatter = "\n".join(
            (
                "---",
                f"title: {yaml_quote(note_title)}",
                f"date: {yaml_quote(date_text)}",
                f"created: {yaml_quote(run_date.isoformat(timespec='seconds'))}",
                f"index: {yaml_quote(index_text)}",
                f"source: {yaml_list(source_files)}",
                f"question_numbers: {yaml_list(question_numbers)}",
                f"tags: {yaml_list(tags)}",
                "---",
                "",
            )
        )
        note_path = date_directory / f"{date_prefix}-{index_text}.md"

        try:
            with note_path.open("x", encoding="utf-8", newline="\n") as note_file:
                note_file.write(frontmatter + "\n" + body + "\n")
            return note_path.resolve()
        except FileExistsError:
            note_index += 1
        except OSError:
            note_path.unlink(missing_ok=True)
            raise


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Store English exercise sources or export an analysis note to Obsidian."
    )
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH))
    subparsers = parser.add_subparsers(dest="command", required=True)

    store_parser = subparsers.add_parser("store-source")
    store_parser.add_argument("--source-files", nargs="+", required=True)
    store_parser.add_argument("--source-root")
    store_parser.add_argument("--date")

    export_parser = subparsers.add_parser("export-note")
    export_parser.add_argument("--content-path", required=True)
    export_parser.add_argument("--vault-root")
    export_parser.add_argument("--date")
    export_parser.add_argument("--question-numbers", nargs="*", default=[])
    export_parser.add_argument("--source-files", nargs="*", default=[])
    export_parser.add_argument("--tags", nargs="*", default=list(DEFAULT_TAGS))
    export_parser.add_argument("--title")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    paths = load_paths(args.config)
    run_date = parse_date(args.date)

    if args.command == "store-source":
        source_root = (
            Path(args.source_root).expanduser().resolve()
            if args.source_root
            else paths["source_root"]
        )
        for stored_path in store_source_files(args.source_files, source_root, run_date):
            print(stored_path)
        return 0

    vault_root = (
        Path(args.vault_root).expanduser().resolve()
        if args.vault_root
        else paths["vault_root"]
    )
    note_path = export_note(
        content_path=Path(args.content_path),
        vault_root=vault_root,
        run_date=run_date,
        question_numbers=args.question_numbers,
        source_files=args.source_files,
        tags=args.tags,
        title=args.title,
    )
    print(note_path)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError, KeyError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
