"""
Collects demo and exercise code from each lesson folder into one long text file.
For each folder (00_Introduction, 01_Regular_Data, ...): writes folder name,
then all code from demo (including subfolders), then README from exercise,
then all code from exercise.
"""

from pathlib import Path

# Directory to skip when walking (deps, build artifacts, etc.)
SKIP_DIRS = {"node_modules", "elm-stuff", ".git", "__pycache__", ".cursor"}

# Extensions treated as code/source (and included in output)
CODE_EXTENSIONS = {
    ".py", ".c", ".h", ".java", ".js", ".ts", ".go", ".hs", ".elm",
    ".fut", ".scala", ".exs", ".yaml", ".yml", ".nix", ".html", ".sh",
    ".md", ".json", ".qnt", ".properties",
}

# Files without extension that we include (e.g. Makefile)
CODE_NAMES = {"Makefile", "Dockerfile"}

# Files we skip even if extension matches
SKIP_FILES = {"flake.lock", "package-lock.json"}


def is_code_file(path: Path) -> bool:
    if path.name in SKIP_FILES:
        return False
    if path.name in CODE_NAMES:
        return True
    return path.suffix.lower() in CODE_EXTENSIONS


def read_file_safe(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return f"[Could not read: {path}]\n"


def collect_dir(base: Path, dir_path: Path, lines: list[str], skip_names: set[str] | None = None) -> None:
    """Recursively collect all code files under dir_path into lines."""
    if not dir_path.is_dir():
        return
    skip_names = skip_names or set()
    items = sorted(dir_path.iterdir(), key=lambda p: (p.is_file(), p.name))
    for item in items:
        if item.name in SKIP_DIRS or item.name in skip_names:
            continue
        rel = item.relative_to(base)
        if item.is_file():
            if is_code_file(item):
                lines.append(f"\n--- {rel}\n")
                lines.append(read_file_safe(item))
        else:
            collect_dir(base, item, lines, skip_names)


def main(
    root_dir: str | None = None,
    output_file: str = "all_demos_and_exercises.txt",
) -> None:
    if root_dir is None:
        root_dir = Path(__file__).resolve().parent
    else:
        root_dir = Path(root_dir)
    root = Path(root_dir)
    out_lines: list[str] = []

    # Find all lesson-like folders (have demo and exercise subdirs)
    candidates = [p for p in root.iterdir() if p.is_dir() and not p.name.startswith(".")]
    lesson_folders = []
    for p in candidates:
        if (p / "demo").is_dir() and (p / "exercise").is_dir():
            lesson_folders.append(p)
    lesson_folders.sort(key=lambda p: p.name)

    for folder in lesson_folders:
        name = folder.name
        out_lines.append("\n")
        out_lines.append("=" * 80 + "\n")
        out_lines.append(f"FOLDER: {name}\n")
        out_lines.append("=" * 80 + "\n")

        # Demo: all subfolders and code
        demo_path = folder / "demo"
        out_lines.append("\n--- DEMO ---\n")
        collect_dir(demo_path, demo_path, out_lines)

        # Exercise: README first, then all code
        ex_path = folder / "exercise"
        readme = ex_path / "README.md"
        out_lines.append("\n--- EXERCISE README ---\n")
        if readme.is_file():
            out_lines.append(read_file_safe(readme))
        else:
            out_lines.append("[No README.md]\n")

        out_lines.append("\n--- EXERCISE CODE ---\n")
        collect_dir(ex_path, ex_path, out_lines, skip_names={"README.md"})

    output_path = root / output_file
    output_path.write_text("".join(out_lines), encoding="utf-8")
    print(f"Written: {output_path}")


if __name__ == "__main__":
    main()
