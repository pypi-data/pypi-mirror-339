# /// script
# dependencies = [
#   "cyclopts",
#   "pyyaml"
# ]
# ///

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from textwrap import dedent

import cyclopts
import yaml

app = cyclopts.App()


@app.default()
def run(runbook_path: str, /) -> None:
    path = Path(runbook_path)
    content = path.read_text()
    if content.startswith("#! "):
        content = content.split("\n", 1)[1]

    config = {}
    if content.startswith("---\n"):
        front_matter, content = re.split(r"\n---\n", content, maxsplit=1)
        config = yaml.safe_load(front_matter)

    prompt = dedent(
        """\
        The following is a runbook that you should follow.

        When in doubt, a human can be prompted for more clarity/info.

        <runbook>
        {content}
        </runbook>
        """
    ).format(content=content)

    exec_dir = Path("~/.claude/books", path.name).expanduser()
    exec_dir.mkdir(exist_ok=True, parents=True)
    os.chdir(exec_dir)

    # MCP support
    if mcp := config.get("mcp"):
        Path(".mcp.json").write_text(json.dumps({"mcpServers": mcp}))

    # Find `claude` binary
    claude_path = shutil.which("claude")
    if not claude_path:
        sys.stderr.write(
            "Error: 'claude' executable not found in PATH. Is it installed? https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview\n"
        )
        sys.exit(1)

    # Write prompt to file (so we can use stdin to avoid cmdline overflow)
    prompt_file = exec_dir / "prompt.txt"
    prompt_file.write_text(prompt)

    with prompt_file.open() as stdin:
        sys.exit(subprocess.call([claude_path], stdin=stdin))  # noqa: S603


if __name__ == "__main__":
    app()
