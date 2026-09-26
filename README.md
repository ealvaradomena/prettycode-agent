# PrettyCode

PrettyCode improves comments, formatting, and readability in **existing R and Python scripts**. It is not a refactoring, debugging, or code-execution tool. Review every proposed change: syntax validation does not prove identical behavior.

## Three interfaces

PrettyCode offers three interfaces: **Codex Skill**, **standalone CLI**, and **MCP server**. You can use each separately; Codex can also combine its Skill with MCP tools when both are installed.

- **Codex Skill (for Codex users):** install the self-contained `.agents/skills/prettycode/` folder into your personal `~/.agents/skills/prettycode/` directory. It includes `SKILL.md` and both authoritative language protocols in `references/`. Invoke the Skill in any working directory. The CLI and MCP server are not required.
- **CLI (standalone):** install the Python package, then use free `list` / `check` commands or explicitly request a potentially paid `polish` operation. `polish` edits one file per API request, defaults to preview, and saves a proposal for free subsequent `apply`.
- **MCP server (for compatible AI clients):** exposes local tools for listing, reading, validating, previewing, and applying code changes. The AI client supplies the model and proposes edits; the server does not call an AI model. It works independently of the Skill, and Codex can use both together when MCP is configured.

**How they relate:** The Skill supplies editing instructions, while MCP supplies local file tools; MCP alone does **not** load the Skill instructions for other clients. When Codex uses both, the Skill guides its edits and MCP can inspect or apply proposals. When Codex uses the Skill without MCP, its normal file tools remain available, but the CLI/MCP safeguards are not automatically applied.

**One source of truth:** Edit the R and Python protocols only in `.agents/skills/prettycode/references/`. Python packaging ships those same files; there are no runtime GitHub prompt fetches.

## Setup (Windows and macOS)

Requires **Python 3.11+**. Use a terminal in the PrettyCode repository. On macOS, `python3` may be the command for Python; use it instead of `python` if needed.

```bash
python -m venv .venv
```

Activate the environment using **one** command:

- Windows Git Bash: `source .venv/Scripts/activate`
- Windows PowerShell: `.\.venv\Scripts\Activate.ps1`
- macOS: `source .venv/bin/activate`

For the CLI's *free* file operations only:

```bash
python -m pip install -e .
prettycode list
prettycode check examples/example.py
prettycode check examples/example.R  # requires Rscript
```

To enable model-assisted CLI polishing (optional):

```bash
python -m pip install -e '.[agent]'
```

Set `OPENAI_API_KEY` securely and supply a supported model only when you intentionally authorize a paid request:

```bash
prettycode polish path/to/script.py --model YOUR_MODEL_ID  # paid; preview only
prettycode apply path/to/script.py                          # no API request
```

The CLI supports `--root PATH` to target a different project; target paths are relative to that root. A successful preview is saved in that project's ignored `.prettycode-proposals/` folder and contains source code—keep it private. `polish --apply` skips separate human approval; beginners should preview first. The approximate preflight input-token count is **not** a complete cost estimate.

R syntax checks also require an installed `Rscript` available on your `PATH`. **PrettyCode never executes your target scripts.** Python parses both versions and checks executable tokens; R parses both versions but does not have an automatic equivalence guard. Review R diffs especially carefully.

## Included examples

`examples/example.py` and `examples/example.R` are intentionally untidy, valid sample scripts. Both print `2.0`. Use them for free CLI syntax checks and read-only Codex Skill / MCP trials; do not use your own project files for a first test.

## Install the Skill once for all projects

Copy the **entire** `.agents/skills/prettycode/` folder (including `references/`) into your personal `~/.agents/skills/prettycode/` location:

- Windows PowerShell: `New-Item -ItemType Directory -Force "$HOME/.agents/skills"; Copy-Item -Recurse -Force .agents/skills/prettycode "$HOME/.agents/skills/"`
- macOS: `mkdir -p ~/.agents/skills && cp -R .agents/skills/prettycode ~/.agents/skills/`

Run those commands **from this repository root**. Restart Codex if it does not discover the new Skill immediately. Others may download the public repository and copy just that Skill folder: no copy of the full repository is needed in their target project. An update is intentional: copy the folder again when you want newer protocols.

## Optional MCP integration

```bash
python -m pip install -e '.[mcp]'
prettycode-mcp
```

The server exposes five local tools: `list_code_files`, `read_code_file`, `validate_code_file`, `inspect_proposal`, and `apply_proposal`. It serves its **launch working directory** as the authorized project root. Configure your MCP-capable AI client to start `prettycode-mcp` from the *target* working directory with the environment in which PrettyCode is installed. User-level MCP configuration is optional and client-specific; there is no repository-specific `.codex/config.toml` requirement. No hosted server is necessary. After installing or updating MCP, restart your AI client so it can reconnect and discover the tools.

## Verification

```bash
python -m pip install -e '.[test]'
python -m pytest -q
prettycode check examples/example.py
prettycode check examples/example.R  # requires Rscript
```

The tests check specific local safeguards and packaging without making paid API requests. They do **not** certify live model results, R checking without R installed, MCP client compatibility, or equivalence of program behavior. See `PRETTYCODE_BEGINNERS_GUIDE.md` for a plain-language walkthrough.
