from pathlib import Path
import pytest
from prettycode.core import assess, discover, replace_if_unchanged, safe_file, validate
from prettycode.cli import main


def test_containment_and_discovery(tmp_path):
    (tmp_path / "one.py").write_text("x=1\n")
    (tmp_path / "old").mkdir()
    (tmp_path / "old" / "ignore.R").write_text("x<-1\n")
    assert discover(tmp_path) == ["one.py"]
    assert safe_file(tmp_path, "one.py").name == "one.py"
    with pytest.raises(ValueError):
        safe_file(tmp_path, "../escape.py")
    assert main(["check", "one.py", "--root", str(tmp_path)]) == 0


def test_python_guard_and_stale_write(tmp_path):
    path = tmp_path / "script.py"
    old = "x=1  # note\nprint(x)\n"
    edited = "# purpose\nx = 1\nprint(x)\n"
    path.write_text(old)
    assert assess(path.name, old, edited)[0]
    assert not assess(path.name, old, "x=2\nprint(x)\n")[0]
    replace_if_unchanged(path, old, edited)
    assert path.read_text() == edited
    with pytest.raises(RuntimeError):
        replace_if_unchanged(path, old, edited)


def test_invalid_syntax_and_free_commands(tmp_path, monkeypatch):
    (tmp_path / "broken.py").write_text("if True print(1)\n")
    assert not validate("broken.py", "if True print(1)\n")[0]
    assert main(["check", "broken.py", "--root", str(tmp_path)]) == 1
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(SystemExit):
        main(["polish", "broken.py", "--model", "example", "--root", str(tmp_path)])


def test_proposal_is_preview_by_default(tmp_path, monkeypatch, capsys):
    import prettycode.cli as cli
    p = tmp_path / "script.py"
    p.write_text("x=1\n")
    monkeypatch.setenv("OPENAI_API_KEY", "mock-key")
    monkeypatch.setattr(cli, "protocol", lambda *args: "Mock local protocol")
    monkeypatch.setattr(cli, "propose", lambda *args: "# documented\nx = 1\n")
    assert cli.main(["polish", "script.py", "--model", "mock-model", "--root", str(tmp_path)]) == 0
    assert p.read_text() == "x=1\n"
    assert "# documented" in capsys.readouterr().out
    assert cli.main(["apply", "script.py", "--root", str(tmp_path)]) == 0
    assert p.read_text().startswith("# documented")


def test_cli_protocol_matches_portable_skill():
    from prettycode.cli import protocol
    skill_refs = Path(__file__).resolve().parent.parent / ".agents" / "skills" / "prettycode" / "references"
    assert protocol(Path.cwd(), "sample.py") == (skill_refs / "pretty-python.md").read_text(encoding="utf-8")
    assert protocol(Path.cwd(), "sample.R") == (skill_refs / "pretty-r.md").read_text(encoding="utf-8")


def test_optional_mcp_server_uses_installed_sdk(tmp_path):
    pytest.importorskip("mcp.server.mcpserver")
    from prettycode.mcp import build_server
    from mcp.server.mcpserver import MCPServer
    assert isinstance(build_server(tmp_path), MCPServer)
