# PrettyCode: A Beginner's Guide

**For:** Someone who has never used PrettyCode and may be new to Python, terminals, AI coding assistants, and software projects.  
**Describes:** PrettyCode as distributed in this repository (Windows and macOS).  
**Start here:** Read Sections 1–5, then choose one of the three interfaces in Section 6: Codex Skill, standalone CLI, or MCP server. You can combine the Skill with MCP if desired.

---

## 1. What is PrettyCode?

PrettyCode is a small tool for **polishing existing R and Python scripts**. Its aim is to make code easier for a person to read—principally by improving comments, spacing, and layout—**without changing what the program does**.

Imagine an untidy script that already produces the right results. PrettyCode can propose a more readable version, show you exactly what changed, and (with your approval) save it. PrettyCode is **not** designed to debug the script, modernize its algorithms, rename variables, add features, or automatically make risky refactors.

The project offers **three interfaces** (three ways to access closely related functionality):

1. **Codex Skill:** Supplies Codex with PrettyCode editing instructions for R and Python. Codex can use its normal file tools or, if configured, PrettyCode MCP tools. No Python package or MCP installation is required to use the Skill alone.
2. **Standalone command-line interface (CLI):** Lets you run commands in a terminal. Its `polish` command asks an OpenAI model to propose edits to one file and makes a potentially **paid API request**.
3. **MCP server:** Gives compatible AI clients tools to list, read, validate, preview, and apply code changes. The client supplies the AI model and proposes edits: the server **does not itself call an LLM** or incur model API charges. It does not require the Codex Skill.

**How they work together:** The Skill gives **instructions**; MCP gives **tools**. Codex may use both simultaneously: the Skill guides an edit, and MCP can inspect and apply the proposed code. Other MCP clients can use the tools without the Codex Skill, but MCP does not automatically provide them with the Skill’s editing instructions. The CLI is a separate terminal workflow. All three aim to **improve readability while preserving existing computational behavior**; the CLI and MCP server share underlying file-validation functions.

## 2. Important terms, in plain English

| Term | Meaning in this project |
|---|---|
| **Script** | A text file containing code. PrettyCode accepts Python (`.py`) and R (`.R` or `.r`) scripts. |
| **Working directory / project root** | The folder PrettyCode is allowed to work inside. Usually it is the folder you have navigated to in your terminal. Files outside this folder cannot be edited through PrettyCode's guarded operations. |
| **Terminal** | A window in which you type commands. On Windows, Git Bash is one option; PowerShell is another. |
| **CLI** | *Command-line interface*: commands such as `prettycode list` and `prettycode check`. |
| **AI model / LLM** | A large language model that can suggest wording and formatting edits. PrettyCode does not assume model-generated edits are correct. |
| **API / API key** | An interface used by one program to contact a service, and a secret credential granting access. The standalone `polish` command uses the OpenAI API. Keep your API key secret. |
| **Protocol** | Written rules telling the editor which changes are acceptable for a particular language. The project includes separate protocols for R and Python. |
| **Codex Skill** | A local instruction document that tells Codex how to perform PrettyCode's task. It is *not* another Python program or a separate model. |
| **AI client** | An application such as Codex or Claude Desktop that provides an AI-powered chat or coding interface and can connect to MCP tools when configured. |
| **MCP** | *Model Context Protocol*: a way for compatible AI applications to use tools exposed by other programs. Here those tools operate on files in one authorized directory. |
| **Dependency** | Another package or program required for a feature. The OpenAI Python package, the MCP package, and R are optional according to which features you need. |
| **Virtual environment (`.venv`)** | A private Python package installation for this project, separate from other Python projects. |
| **Syntax check** | A check that a file can be parsed as valid Python or R. It does *not* establish that it runs correctly or produces the same answers. |
| **Token guard** | An additional Python safeguard comparing meaningful Python tokens before and after editing. It allows comments/formatting changes but rejects changes to ordinary code tokens. It is conservative, not a mathematical proof of equivalence. |
| **Diff** | A comparison showing removed lines (typically `-`) and added lines (typically `+`). Review it before accepting edits. |
| **Proposal / preview** | A suggested change you can inspect without touching your original file. In the CLI, previews are saved locally so you can apply them without paying for the same suggestion twice. |
| **Test** | A small automated check that verifies a particular behavior of PrettyCode itself, not necessarily of a script you ask PrettyCode to polish. |
| **Git** | A version-control system that records file changes and lets you recover earlier versions. Strongly recommended before applying proposed edits. |

## 3. How the working directory is organized

Open the PrettyCode repository folder (for example, `prettycode-agent/`). Its `prettycode/` subfolder contains the Python application; `.agents/skills/prettycode/` contains the independently installable Codex Skill.

```text
prettycode-agent/                      Project root
|-- README.md                          Quick start
|-- PRETTYCODE_BEGINNERS_GUIDE.md       This guide
|-- pyproject.toml                     Python package and dependencies
|-- .gitignore                         Local/generated files Git ignores
|-- examples/                          Two included starter scripts
|   |-- example.py                     Intentionally untidy valid Python
|   `-- example.R                      Intentionally untidy valid R
|-- prettycode/                        Python application
|   |-- __init__.py
|   |-- cli.py                         list, check, polish, apply
|   |-- core/__init__.py               Validation and safe file writing
|   `-- mcp/__init__.py                Optional MCP server
|-- .agents/skills/prettycode/         Standalone, portable Codex Skill
|   |-- SKILL.md                       Skill behavior
|   `-- references/                    ONE authoritative protocol per language
|       |-- pretty-python.md
|       `-- pretty-r.md
`-- tests/test_core.py                  Local checks
```

**Why are some folders named `prettycode`?** The **outer folder** (`prettycode-agent`) is the complete project, whereas the **inner** `prettycode/` is its importable Python application. A Codex Skill also happens to have a `prettycode/` folder under `.agents/skills/`; that folder contains instructions, not the application.

**What are the leading dots?** On many systems, folders beginning with a dot, such as `.agents/`, `.venv/`, and `.prettycode-proposals/`, are treated as hidden. Enable hidden-file display in your file explorer if you cannot see them.

### Files and folders that appear later

These are generated locally after installation or use, rather than maintained project source files:

- `.venv/`: your locally created Python virtual environment. Do not edit it manually or commit it to Git.
- `.prettycode-proposals/`: locally saved CLI suggestions. It appears after a successful `prettycode polish` preview. Its JSON files include **the original and proposed source**, so treat them as potentially sensitive. `prettycode apply` deletes the corresponding proposal after successfully applying it.
- `.pytest_cache/`, `__pycache__/`, or `*.egg-info/`: routine Python-generated files or folders, usually safe to ignore.
- Your own `scripts/` or other working folders: optional; you create them. They are not required by PrettyCode.

**Included examples:** `examples/example.py` and `examples/example.R` are small, deliberately untidy scripts. Both print `2.0`. They are safe starting points for practicing syntax checks and read-only Codex Skill / MCP workflows.

**Important:** `prettycode list` searches for R/Python files under the current project root. This includes PrettyCode's *own* application and test files if you run it from this repository; it does not magically find scripts in unrelated RStudio projects. To edit another project, see the `--root` example below.

## 4. A mental model: what happens to one script?

Here is the recommended **CLI** path:

```text
Your existing script
        |
        v
[1] Validate original syntax (no code execution)
        |
        v
[2] Read the appropriate local R/Python editing protocol
        |
        v
[3] Send that protocol + one script to the specified OpenAI model
        |    (ONE new, potentially paid API request; no automatic retry)
        v
[4] Receive proposed complete script
        |
        v
[5] Validate proposed syntax; run the extra token guard for Python
        |
        +---- fails? --> Reject; do not write changes
        |
        v
[6] Print a line-by-line diff and save a local proposal
        |    (your original file is still unchanged)
        v
[7] YOU read the diff and decide whether to apply
        |
        v
[8] Apply the saved proposal locally (no additional API request)
        |    only if the source file has not changed meanwhile
        v
Your updated script -- still review/test its real-world behavior
```

For R scripts, both the original and the proposed text must pass the R syntax parser, but PrettyCode does **not** have an R equivalent of its Python token guard. R changes consequently need particularly careful human inspection.

A proposal that fails a check, or makes no changes, will not be saved as an acceptable preview. A model response can still be awkward or undesirable even when it passes the checks.

## 5. First-time setup (Windows and macOS)

You need **Python 3.11 or newer**. The Codex Skill needs **no Python installation** when used alone; the following setup is for the standalone CLI or optional MCP server.

### Step A: Open the repository folder

Open Git Bash or PowerShell on Windows, or Terminal on macOS. Navigate to your PrettyCode repository (replace the example path with your own):

```bash
cd ~/Documents/GitHub/prettycode-agent
pwd
```

Confirm that `README.md`, `pyproject.toml`, `prettycode/`, and `.agents/skills/prettycode/` exist. On macOS, use `python3` instead of `python` in the following commands if that is how Python is installed.

### Step B: Create and activate a Python virtual environment

All operating systems create the environment with:

```bash
python -m venv .venv
```

Then activate it using the command for your terminal:

| Terminal | Activation command |
|---|---|
| Windows Git Bash | `source .venv/Scripts/activate` |
| Windows PowerShell | `.\.venv\Scripts\Activate.ps1` |
| macOS Terminal | `source .venv/bin/activate` |

PowerShell may require an adjustment to its script-execution policy. After activation you should normally see `(.venv)` in your prompt.

### Step C: Install only the features you plan to use

To install the basic CLI for offline `list` and `check`:

```bash
python -m pip install -e .
```

The following are **optional** and can be installed later: `python -m pip install -e '.[agent]'` for the OpenAI-powered CLI, `python -m pip install -e '.[mcp]'` for the MCP server, or `python -m pip install -e '.[test]'` to run included tests. The `-e` means editing PrettyCode's source files in this checkout updates the installed development version.

To check R code, also install R separately and ensure `Rscript` is on your system's `PATH` (the directories searched for commands). A separate R package or R configuration file is not required.

### Step D: Try two free commands

```bash
prettycode list
prettycode check examples/example.py
prettycode check examples/example.R  # requires Rscript
```

Neither command invokes an AI model, changes source files, or runs the script being checked. If you installed the optional test dependencies, you can also run `python -m pytest -q` to check PrettyCode's local safeguards. Both example scripts print `2.0` if *you* choose to run them; syntax validation itself never runs scripts.

## 6. Choose ONE way to use PrettyCode

### Route A — The standalone CLI (simplest when working without Codex)

The CLI's four main commands are:

| Command | What it does | New model request? | Changes source? |
|---|---|---:|---:|
| `prettycode list` | Lists supported source files under the root. | No | No |
| `prettycode check PATH` | Checks Python or R syntax; never runs your script. | No | No |
| `prettycode polish PATH --model MODEL_ID` | Requests one edited version, validates it, prints a diff, and saves a preview if accepted. | **Yes** | **No, by default** |
| `prettycode apply PATH` | Applies an existing valid, still-current saved proposal. | No | **Yes** |

Suppose you have a Python file called `scripts/example.py` inside a separate RStudio or code project, say `~/Documents/GitHub/my-analysis`. You can run PrettyCode from any working directory after installation. Here, explicitly designate the **other project** as the authorized root:

```bash
prettycode list --root ~/Documents/GitHub/my-analysis
prettycode check scripts/example.py --root ~/Documents/GitHub/my-analysis
```

Paths following commands are interpreted **relative to `--root`**. You may alternatively run commands from the target project's directory and omit `--root`, assuming PrettyCode was installed in your active environment. The protocols are bundled with PrettyCode at installation; the target project does not need its own copy of those protocols.

**Paid step — only when you intentionally choose to use the OpenAI API:** first configure a valid API key securely in your environment and select a model ID your account supports. On macOS Terminal or Windows Git Bash, a temporary environment variable uses `export OPENAI_API_KEY=...`; on Windows PowerShell, use `$env:OPENAI_API_KEY = "..."`; avoid pasting or storing a real key in code, README files, screenshots, or Git. Setting a key alone does not send a request.

```bash
prettycode polish scripts/example.py --root ~/Documents/GitHub/my-analysis --model YOUR_MODEL_ID
```

Before contacting the model, PrettyCode reports one planned API request and an **approximate input-token count**. It does **not** provide a guaranteed total price, and it does not ask for an interactive final confirmation. **Running this command is your authorization to make the request.** The default behavior is to preview; review the printed diff and the script itself before accepting.

If you like the result:

```bash
prettycode apply scripts/example.py --root ~/Documents/GitHub/my-analysis
```

This uses the saved preview and costs **no new model request**. It also refuses to replace the script if that script's contents have changed since the preview. If you do not like the proposal, simply do not apply it. You may delete its saved JSON from the target root's `.prettycode-proposals/` directory when no longer needed.

**Avoid initially:** `prettycode polish ... --apply` requests and immediately writes the accepted suggestion. It does print the diff, but you do not get a separate human approval step between seeing the diff and the write. Prefer preview and separate `apply`.

**R usage:** The same CLI commands accept `.R` and `.r` files, provided `Rscript` is installed and discoverable. Make sure to review the diff especially carefully because there is no automatic R token-equivalence guard.

### Route B — The Codex Skill (when editing inside Codex)

For a first read-only exercise, ask Codex: “Use the PrettyCode Skill to propose documentation improvements for `examples/example.py` without editing it or using MCP.”

The file `.agents/skills/prettycode/SKILL.md` is a short set of instructions for a Codex-capable environment that recognizes project skills. It tells Codex to read the appropriate authoritative protocol **inside the Skill**, at `references/pretty-python.md` or `references/pretty-r.md`, and preserve executable behavior.

Install the Skill **once per user** by copying the entire `.agents/skills/prettycode/` directory (including `references/`) from the PrettyCode repository into `~/.agents/skills/prettycode/`. You can then use it across projects without copying PrettyCode into each one. From the PrettyCode repository root:

| Terminal | One-time installation |
|---|---|
| Windows Git Bash | `mkdir -p ~/.agents/skills && cp -R .agents/skills/prettycode ~/.agents/skills/` |
| Windows PowerShell | `New-Item -ItemType Directory -Force "$HOME/.agents/skills"; Copy-Item -Recurse -Force .agents/skills/prettycode "$HOME/.agents/skills/"` |
| macOS Terminal | `mkdir -p ~/.agents/skills && cp -R .agents/skills/prettycode ~/.agents/skills/` |

If a prior copy exists, remove that *personal Skill copy* before reinstalling to avoid leftover files. Restart Codex if needed. Other people can copy just this folder from the public repository without installing the CLI. The normal workflow is **open your target project in Codex → invoke PrettyCode for one R/Python file → review its diff → authorize writes**.

The Skill can work using Codex's ordinary file-editing tools. When an MCP connection is configured, Codex can use its tools to inspect and apply a proposal while following the Skill’s instructions. MCP does not automatically enforce those instructions. The MCP connection is *not* needed merely to use the Skill, and you should not have the Skill call the standalone paid API unnecessarily. Codex access or subscription may have separate limits or costs.

**Important:** The Skill instructions and the CLI share an editing goal, but Codex is not automatically running the CLI's exact token guard when it uses ordinary file tools. Ask for the diff and validation report; use version control and your own judgment before accepting changes.

### Route C — The optional MCP server (for compatible AI clients)

MCP is a tool bridge and a distinct third interface; it is **not** a second editing model. For example, Codex can follow the PrettyCode Skill and call MCP tools, while another compatible AI client can use MCP on its own. The client is responsible for generating proposed edits. PrettyCode's MCP server exposes five tools that a compatible client may call:

| MCP tool | Purpose |
|---|---|
| `list_code_files` | List R/Python files within the configured project root. |
| `read_code_file` | Read one permitted source file. |
| `validate_code_file` | Perform a syntax check on a permitted source file. |
| `inspect_proposal` | Validate a proposed complete script and return a diff without writing. |
| `apply_proposal` | Write a proposed script, guarded by validation and by checking that the original file has not changed. |

To start the server after installing the MCP extra (`mcp` version 2.x):

```bash
prettycode-mcp
```

**Important difference:** Unlike the CLI's `--root` flag, this MCP server sets its authorized root to the **current working directory at the moment it starts**. Configure the AI client to launch `prettycode-mcp` with that directory as its working directory, using the Python environment where the optional MCP dependency is installed. Optional MCP client settings belong to each user/client; PrettyCode does not require a project-level `.codex/config.toml`. Restart the AI client after installing or updating the server so it reconnects and discovers its tools.

For a first read-only MCP exercise, ask your connected client: “Use PrettyCode MCP to validate `examples/example.py` and list the available tools. Do not modify files.” This confirms tool discovery and communication, not just local installation.

MCP communication uses **stdio**, meaning the client communicates with the server through its standard input and output streams rather than through a website. Running the command directly in an ordinary terminal does **not** provide a user-friendly interactive chat; it normally waits for an MCP client.

The MCP tools do not make model calls or automatically load the Codex Skill and its language protocols. Your chosen client may use an AI model to write the proposal it passes to `inspect_proposal`; without the Skill, supply appropriate editing instructions in that client. The `apply_proposal` tool can write when invoked: keep write permissions under your control, and inspect changes before use.

## 7. Safeguards—and what they do NOT guarantee

PrettyCode is deliberately conservative:

- It accepts only existing `.py`, `.R`, or `.r` files within the authorized project root through its guarded file operations. Its discovery excludes common environment/cache folders and any folder named `old`.
- It checks syntax without executing the target script. Python uses Python's parser; R uses `Rscript` to parse without evaluation.
- For **Python**, it also rejects a proposal if its meaningful code tokens differ. It is intended to preserve variables, executable statements, strings, and other code tokens while allowing comments and layout changes.
- It shows a diff before the normal CLI apply step. It checks that the original file remains unchanged before writing to avoid accidentally overwriting subsequent work.
- The standalone CLI makes **at most one new model request per `polish` invocation** and performs no automatic retries.

These safeguards have limits. **Passing validation does not prove identical behavior**, especially with R. A syntax-valid script can still be logically wrong; a token-preserving Python edit can still deserve human scrutiny. PrettyCode does not run unit tests of your target project, execute your scripts, confirm output equality, or silently repair bugs.

Before applying to valuable work, commit your current project in Git or make a backup. Afterward, inspect the diff, run your normal project tests or workflow yourself, and compare outputs when the results matter.

## 8. Troubleshooting common beginner problems

| Problem | Likely explanation and next step |
|---|---|
| `prettycode: command not found` | Activate the virtual environment and install the package with `python -m pip install -e '.[agent]'` (for polishing) or `python -m pip install -e .` (for free commands). Check that you are using the same terminal environment. |
| `No R/Python files found` | Check your current folder (`pwd`) or supply `--root` for the folder containing your scripts. `list` will not search outside that root. |
| `Target must be an existing R/Python file within the project root` | Check the spelling, extension, and relationship between the target path and `--root`. Paths outside the root are intentionally rejected. |
| `Rscript not on PATH` | Install R and configure your operating system so the `Rscript` command is available. Python checking works without R. |
| `OPENAI_API_KEY must be set` | The paid CLI feature needs a valid API key available in the environment. Free `list`/`check` do not need one. |
| `--model is required` | Specify a supported OpenAI model ID when intentionally calling `polish`. |
| `Python executable tokens differ` | The model suggested changes broader than PrettyCode permits. The proposal is rejected. Review manually rather than bypassing the safeguard blindly. |
| `No changes proposed` | The model returned exactly the original text; no preview is saved. This is acceptable if the script already meets your needs. |
| `No saved proposal` | Run a successful `polish` preview first, for that exact file and root. |
| `File changed since inspection` | You or another tool modified the source after the preview. Review the latest version and generate a new proposal if still needed. |
| The MCP command appears to hang | MCP expects a compatible client over stdio; it is not a human-oriented terminal app. Also check the folder from which it was launched. |
| R code passes syntax but looks substantively different | Do not apply it. R lacks PrettyCode's Python token guard; manual diff review is essential. |

## 9. What to read or edit—and what to leave alone

- **Start with this guide**, then consult `README.md` for the compact technical reference.
- **Read `.agents/skills/prettycode/references/`** to see the one authoritative editing protocol for each language. The standalone CLI bundles these exact versions at installation; runtime GitHub downloads are not used.
- **Read `.agents/skills/prettycode/SKILL.md`** if you use Codex. It explains the Skill's editing constraints.
- **Read `prettycode/cli.py`** only when you want to understand the CLI implementation. **Read `prettycode/core/__init__.py`** for the shared safety checks and **`prettycode/mcp/__init__.py`** for MCP-specific tooling.
- **Use `tests/test_core.py`** when changing PrettyCode itself and wanting to catch regressions in the selected behaviors it tests.
- **Do not routinely edit** `.venv/`, cached Python folders, or `.prettycode-proposals/*.json`. In particular, proposal JSON is working data, not an editing interface.

### One important distinction

**Using PrettyCode to polish your own script** is different from **developing PrettyCode itself**. For ordinary usage, work with your script, its diff, and the application commands; you generally do **not** need to change anything inside `prettycode/`. If you later extend the tool, use the tests, edit its source deliberately, and verify that safeguards still behave as expected.

## 10. A sensible first exercise (no charges)

Create a disposable Python file in a separate test folder or inside a throwaway project:

```python
x=1 # a value
print(x)
```

Then, from your activated environment, try `prettycode list` and `prettycode check` with the correct `--root` and path. Confirm that you understand which folder is authorized and that `check` **does not** rewrite the file. If you decide to try model-assisted `polish` afterward, do so only after reviewing the cost implications and preparing a Git commit or backup. Start with **one small, non-sensitive script**, inspect the proposal, and apply it separately only if acceptable.

**The guiding principle:** PrettyCode is a controlled readability assistant. You—not the model—decide whether an edit should become part of your project.
