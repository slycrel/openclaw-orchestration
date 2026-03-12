import os
import subprocess
from pathlib import Path


def _run(tmp_path, *args):
    env = os.environ.copy()
    env["OPENCLAW_WORKSPACE"] = str(tmp_path)
    return subprocess.run(["python3", "src/cli.py", *args], cwd=Path(__file__).resolve().parents[1], env=env, capture_output=True, text=True)


def test_cli_init_next_done_report(tmp_path):
    r = _run(tmp_path, "init", "demo", "Ship", "it", "--priority", "2")
    assert r.returncode == 0
    r = _run(tmp_path, "next", "--project", "demo")
    assert "Define success criteria" in r.stdout
    r = _run(tmp_path, "done", "demo")
    assert r.returncode == 0
    out = tmp_path / "report.md"
    r = _run(tmp_path, "report", "--project", "demo", "--out", str(out))
    assert r.returncode == 0
    assert out.exists()
