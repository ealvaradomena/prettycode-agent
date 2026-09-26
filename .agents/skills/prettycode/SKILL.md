---
name: prettycode
description: Improve existing R and Python script documentation and formatting while conservatively preserving computational behavior.
---

# PrettyCode

1. Read the requested source file and the matching instruction file **inside this Skill**: `references/pretty-r.md` for R or `references/pretty-python.md` for Python. These are the authoritative PrettyCode language protocols. Work only on files the user authorizes.
2. Improve source-supported comments, formatting, and readability without changing executable operations, identifiers, strings, APIs, side effects, or behavior. Do not invent context or silently fix bugs. For Python, preserve executable tokens and docstrings unchanged. If protocol suggestions conflict with these restrictions, preserve the original code.
3. Use ordinary Codex file tools; MCP is **optional**. When PrettyCode MCP tools are already available, you may use `read_code_file`, `inspect_proposal`, and (only after authorization) `apply_proposal`. Do not launch a separate OpenAI API request through the PrettyCode CLI just to use this Skill.
4. Show or describe the diff before applying changes when feasible. Validate Python syntax with parsing, or R syntax with `Rscript` parsing if available, without executing target scripts. Without MCP, Codex's edits do not automatically pass the CLI's Python token guard.
5. Report changed files, checks actually performed, and unresolved behavior concerns. Syntax checks and token preservation do not prove semantic equivalence. Never execute target scripts without explicit authorization.
