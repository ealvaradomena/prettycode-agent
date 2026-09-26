"""Optional MCP adapter over the same deterministic core; no API calls."""
from pathlib import Path
from ..core import assess, discover, replace_if_unchanged, safe_file, show_diff, validate


def build_server(root: Path):
    from mcp.server.mcpserver import MCPServer
    root = Path(root).resolve()
    server = MCPServer("prettycode")

    @server.tool()
    def list_code_files() -> list[str]:
        """List editable R/Python files under the authorized project root."""
        return discover(root)

    @server.tool()
    def read_code_file(path: str) -> str:
        """Read an existing R/Python source file."""
        return safe_file(root, path).read_text(encoding="utf-8")

    @server.tool()
    def validate_code_file(path: str) -> dict:
        """Check syntax, without executing target code or guaranteeing behavior."""
        file = safe_file(root, path)
        ok, reason = validate(path, file.read_text(encoding="utf-8"))
        return {"passed": ok, "details": reason}

    @server.tool()
    def inspect_proposal(path: str, proposed: str) -> dict:
        """Assess proposed code and return a diff, without changing files."""
        file = safe_file(root, path)
        before = file.read_text(encoding="utf-8")
        passed, reason = assess(path, before, proposed)
        return {"passed": passed, "details": reason,
                "diff": show_diff(path, before, proposed)}

    @server.tool()
    def apply_proposal(path: str, expected_original: str, proposed: str) -> str:
        """Write only when explicitly called and source has not changed; inspect first."""
        file = safe_file(root, path)
        replace_if_unchanged(file, expected_original, proposed)
        return f"Updated {path}; syntax guards do not prove behavior preservation"

    return server


def main():
    build_server(Path.cwd()).run(transport="stdio")


if __name__ == "__main__":
    main()
