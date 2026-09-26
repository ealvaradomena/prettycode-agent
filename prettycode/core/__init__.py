"""Shared conservative file operations; no LLM, MCP, or paid dependencies."""
from __future__ import annotations

import difflib
import io
from pathlib import Path
import shutil
import subprocess
import tempfile
import tokenize
import ast

SUPPORTED = {".py": "python", ".R": "r", ".r": "r"}


def safe_file(root: Path, name: str) -> Path:
    root = Path(root).resolve()
    path = (root / name).resolve()
    if not path.is_relative_to(root) or path.suffix not in SUPPORTED or not path.is_file():
        raise ValueError("Target must be an existing R/Python file within the project root")
    return path


def discover(root: Path) -> list[str]:
    root = Path(root).resolve()
    excluded = {".git", ".venv", "venv", "renv", "__pycache__", ".Rproj.user", "old"}
    return sorted(str(p.relative_to(root)) for p in root.rglob("*")
                  if p.is_file() and p.suffix in SUPPORTED
                  and not any(part in excluded for part in p.relative_to(root).parts)
                  and p.resolve().is_relative_to(root))


def validate(name: str, source: str) -> tuple[bool, str]:
    """Syntax only: never execute the target script."""
    language = SUPPORTED.get(Path(name).suffix)
    if language == "python":
        try:
            ast.parse(source, filename=name)
            return True, "Python syntax valid (not a behavior test)"
        except (SyntaxError, ValueError) as exc:
            return False, str(exc)
    if language == "r":
        if not shutil.which("Rscript"):
            return False, "Rscript not on PATH; cannot validate R syntax"
        # Parse stdin without evaluating R code, avoiding quoting and temporary files.
        result = subprocess.run(
            ["Rscript", "--vanilla", "-e", "parse(file('stdin'))"],
            input=source, text=True, capture_output=True, check=False, timeout=30,
        )
        return result.returncode == 0, (result.stderr.strip() or "R syntax valid (not a behavior test)")
    return False, "Unsupported file type"


def python_tokens_unchanged(before: str, after: str) -> bool:
    """A narrow guard: Python executable tokens, including string literals, unchanged.

    Ignores comments, layout and indent widths. Does not prove runtime equivalence.
    """
    def tokens(text: str) -> list[tuple[int, str]]:
        result = []
        for t in tokenize.generate_tokens(io.StringIO(text).readline):
            if t.type in {tokenize.COMMENT, tokenize.NL, tokenize.NEWLINE,
                          tokenize.ENCODING, tokenize.ENDMARKER}:
                continue
            result.append((t.type, "" if t.type in {tokenize.INDENT, tokenize.DEDENT} else t.string))
        return result
    try:
        return tokens(before) == tokens(after)
    except (tokenize.TokenError, IndentationError):
        return False


def assess(name: str, before: str, after: str) -> tuple[bool, str]:
    if after == before:
        return False, "No changes proposed"
    valid_before, msg_before = validate(name, before)
    if not valid_before:
        return False, f"Original syntax invalid or unchecked: {msg_before}"
    valid_after, msg_after = validate(name, after)
    if not valid_after:
        return False, f"Proposed syntax invalid or unchecked: {msg_after}"
    if Path(name).suffix == ".py" and not python_tokens_unchanged(before, after):
        return False, "Python executable tokens differ; review manually; no write"
    return True, ("Python token guard and syntax passed; behavior unproven" if
                  Path(name).suffix == ".py" else
                  "R syntax passed; no automatic behavioral equivalence check")


def show_diff(name: str, before: str, after: str) -> str:
    return "".join(difflib.unified_diff(before.splitlines(keepends=True),
                    after.splitlines(keepends=True), fromfile=f"a/{name}", tofile=f"b/{name}"))


def replace_if_unchanged(path: Path, original: str, replacement: str) -> None:
    """Refuse stale writes; replace atomically and keep original file mode."""
    if path.read_text(encoding="utf-8") != original:
        raise RuntimeError("File changed since inspection; refusing overwrite")
    allowed, message = assess(path.name, original, replacement)
    if not allowed:
        raise ValueError(message)
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="", dir=path.parent,
                                     prefix=".prettycode-", delete=False) as temp:
        temp.write(replacement)
        temp_path = Path(temp.name)
    try:
        temp_path.chmod(path.stat().st_mode)
        # Second stale-write check reduces the interval for concurrent overwrites.
        if path.read_text(encoding="utf-8") != original:
            raise RuntimeError("File changed during write; refusing overwrite")
        temp_path.replace(path)
    finally:
        temp_path.unlink(missing_ok=True)
