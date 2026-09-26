"""Tiny CLI: check without network, polish with an explicitly requested API call."""
import argparse
from pathlib import Path
import os
import sys
import json
import hashlib
import sysconfig

from .core import assess, discover, replace_if_unchanged, safe_file, show_diff, validate


def protocol(root: Path, name: str) -> str:
    """Read the single authoritative Skill protocol, from checkout or installed package data."""
    lang = "python" if name.endswith(".py") else "r"
    filename = f"pretty-{lang}.md"
    source_checkout = (Path(__file__).resolve().parent.parent / ".agents" /
                       "skills" / "prettycode" / "references" / filename)
    installed = Path(sysconfig.get_path("data")) / "share" / "prettycode" / "protocols" / filename
    for path in (source_checkout, installed):
        if path.is_file():
            return path.read_text(encoding="utf-8")
    raise FileNotFoundError(f"PrettyCode protocol {filename} not installed; reinstall PrettyCode")


def propose(source: str, instructions: str, name: str, model: str) -> str:
    """One paid API request, no retries, no autonomous tool loop."""
    from openai import OpenAI
    response = OpenAI().responses.create(
        model=model,
        instructions=("You edit exactly one source file. Return ONLY the complete revised source text, "
                      "without Markdown fences, commentary, or extra files. Improve comments and "
                      "formatting without changing identifiers, literals, executable operations, "
                      "API calls, imports, logic, side effects, or behavior. "
                      "Do not invent contextual information. When unsure, leave it unchanged. "
                      "Python: preserve all executable tokens including string literals; "
                      "do not add or change docstrings. Follow the language protocol where safe.\n\n" + instructions),
        input=f"FILENAME: {name}\n\nSOURCE:\n{source}",
    )
    return response.output_text


def proposal_path(root: Path, name: str) -> Path:
    digest = hashlib.sha256(name.encode("utf-8")).hexdigest()[:16]
    return root / ".prettycode-proposals" / f"{digest}.json"


def save_proposal(root: Path, name: str, original: str, edited: str) -> Path:
    path = proposal_path(root, name)
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps({"path": name, "original": original, "proposed": edited},
                               ensure_ascii=False), encoding="utf-8")
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Conservative R/Python code polishing")
    parser.add_argument("command", choices=["list", "check", "polish", "apply"])
    parser.add_argument("target", nargs="?", default=".", help="Project-relative source path, or . for list/check")
    parser.add_argument("--root", default=".", help="Authorized project root (default current directory)")
    parser.add_argument("--model", help="OpenAI model ID; required for polish")
    parser.add_argument("--apply", action="store_true", help="Write validated result; without it show diff only")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    if not root.is_dir():
        parser.error("--root must be a directory")
    if args.command == "list":
        for name in discover(root):
            print(name)
        return 0
    try:
        names = discover(root) if args.target == "." else [str(safe_file(root, args.target).relative_to(root))]
    except ValueError as exc:
        parser.error(str(exc))
    if args.command == "apply":
        if args.target == "." or len(names) != 1:
            parser.error("apply requires one file with a saved preview")
        path = proposal_path(root, names[0])
        if not path.exists():
            print("No saved proposal. Run polish first.", file=sys.stderr)
            return 1
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            if payload["path"] != names[0]:
                raise ValueError("Proposal targets a different file")
            target = safe_file(root, names[0])
            print(show_diff(names[0], payload["original"], payload["proposed"]), end="")
            replace_if_unchanged(target, payload["original"], payload["proposed"])
            path.unlink()
            print(f"Applied saved proposal: {names[0]}", file=sys.stderr)
            return 0
        except Exception as exc:
            print(f"No changes applied: {exc}", file=sys.stderr)
            return 1
    if args.command == "check":
        if not names:
            print("No R/Python files found")
        failed = False
        for name in names:
            path = safe_file(root, name)
            ok, message = validate(name, path.read_text(encoding="utf-8"))
            print(f"{'PASS' if ok else 'FAIL'} {name}: {message}")
            failed |= not ok
        return 1 if failed else 0
    if args.target == "." or len(names) != 1:
        parser.error("polish requires exactly one source file (bounded cost and review)")
    if not args.model:
        parser.error("--model is required for polish; one paid API request will be made")
    if not os.environ.get("OPENAI_API_KEY"):
        parser.error("OPENAI_API_KEY must be set; no request was made")
    name = names[0]
    path = safe_file(root, name)
    original = path.read_text(encoding="utf-8")
    ok, reason = validate(name, original)
    if not ok:
        print(f"Original not validated: {reason}. No API request made.", file=sys.stderr)
        return 1
    try:
        instructions = protocol(root, name)
        print(f"Preflight: 1 API request, model={args.model}, file={name}, "
              f"input approximately {(len(original)+len(instructions))//4:,} tokens; "
              "output and cost depend on model. No automatic retries.", file=sys.stderr)
        edited = propose(original, instructions, name, args.model)
        allowed, reason = assess(name, original, edited)
        print(reason, file=sys.stderr)
        if not allowed:
            return 1
        print(show_diff(name, original, edited), end="")
        if args.apply:
            replace_if_unchanged(path, original, edited)
            print(f"\nApplied: {name}; review behavior separately.", file=sys.stderr)
        else:
            saved = save_proposal(root, name, original, edited)
            print(f"\nPreview only: source unchanged. Proposal saved to {saved.relative_to(root)}. "
                  f"Run `prettycode apply {name}` after reviewing (no new API call).", file=sys.stderr)
        return 0
    except Exception as exc:
        print(f"Stopped without applying: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
