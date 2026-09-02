"""Validate public HWP AI Bridge documentation and integration examples."""

from __future__ import annotations

import json
import re
import sys
import tomllib
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
INTEGRATIONS = ROOT / "integrations"
REQUIRED_CLIENTS = ("claude-code", "codex", "cursor", "gemini", "grok-build")
REQUIRED_MODES = ("direct", "safe", "hybrid")


def fail(message: str) -> None:
    raise ValueError(message)


def validate_safe_server(
    path: Path, name: str, server: dict[str, object], *, toml: bool
) -> None:
    """Keep hub examples aligned with the safe engine's distributed examples."""

    if server.get("command") != "hwp-live-safe":
        return
    expected_name = "hwp_live_safe" if toml else "hwp-live-safe"
    if name != expected_name:
        fail(f"{path.relative_to(ROOT)}: safe server must be named {expected_name}")

    relative_parts = path.relative_to(INTEGRATIONS).parts
    if relative_parts[0] == "codex":
        required = {
            "startup_timeout_sec": 30,
            "tool_timeout_sec": 90,
            "enabled": True,
            "default_tools_approval_mode": "prompt",
        }
        for key, expected in required.items():
            if server.get(key) != expected:
                fail(f"{path.relative_to(ROOT)}: safe server requires {key} = {expected!r}")
        environment = server.get("env")
        if not isinstance(environment, dict):
            fail(f"{path.relative_to(ROOT)}: safe server requires an env table")
        for key in ("PYTHONUTF8", "PYTHONDONTWRITEBYTECODE"):
            if environment.get(key) != "1":
                fail(f"{path.relative_to(ROOT)}: safe server requires {key} = '1'")
    elif relative_parts[0] == "grok-build":
        if server.get("startup_timeout_sec") != 30:
            fail(f"{path.relative_to(ROOT)}: safe server requires startup_timeout_sec = 30")


def validate_mode_matrix() -> None:
    for client in REQUIRED_CLIENTS:
        client_dir = INTEGRATIONS / client
        if not client_dir.is_dir():
            fail(f"Missing integration directory: integrations/{client}")
        names = {path.name.split(".", 1)[0] for path in client_dir.glob("*.example")}
        missing = set(REQUIRED_MODES) - names
        if missing:
            fail(f"integrations/{client}: missing modes: {', '.join(sorted(missing))}")


def validate_json_examples() -> int:
    files = sorted(INTEGRATIONS.rglob("*.json.example"))
    if not files:
        fail("No JSON MCP examples were found")

    for path in files:
        data = json.loads(path.read_text(encoding="utf-8"))
        servers = data.get("mcpServers")
        if not isinstance(servers, dict) or not servers:
            fail(f"{path.relative_to(ROOT)}: mcpServers must be a non-empty object")
        for name, server in servers.items():
            if not isinstance(server, dict) or not isinstance(server.get("command"), str):
                fail(f"{path.relative_to(ROOT)}: {name} is missing a string command")
            if not isinstance(server.get("args", []), list):
                fail(f"{path.relative_to(ROOT)}: {name}.args must be an array")
            validate_safe_server(path, name, server, toml=False)
    return len(files)


def validate_toml_examples() -> int:
    files = sorted(INTEGRATIONS.rglob("*.toml.example"))
    if not files:
        fail("No TOML MCP examples were found")

    for path in files:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        servers = data.get("mcp_servers")
        if not isinstance(servers, dict) or not servers:
            fail(f"{path.relative_to(ROOT)}: mcp_servers must be a non-empty table")
        for name, server in servers.items():
            if not isinstance(server, dict) or not isinstance(server.get("command"), str):
                fail(f"{path.relative_to(ROOT)}: {name} is missing a string command")
            if not isinstance(server.get("args", []), list):
                fail(f"{path.relative_to(ROOT)}: {name}.args must be an array")
            validate_safe_server(path, name, server, toml=True)
    return len(files)


SENSITIVE_PATTERNS = {
    "Windows drive-absolute path": re.compile(
        r"(?i)(?<![A-Za-z0-9])[A-Z]:[\\/]"
    ),
    "Windows UNC path": re.compile(
        r"(?<![A-Za-z0-9:/\\])[\\/]{2}(?![.?\\/])"
    ),
    "Windows PC name": re.compile(r"(?i)\bDESKTOP-[A-Z0-9]{5,}\b"),
    "OpenAI-style secret": re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    "bearer token": re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._-]{16,}\b"),
}

TEXT_SUFFIXES = {
    "",
    ".example",
    ".json",
    ".md",
    ".ps1",
    ".py",
    ".toml",
    ".txt",
    ".yml",
    ".yaml",
}


def public_text_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() in TEXT_SUFFIXES or path.name in {"CODEOWNERS", "LICENSE"}:
            files.append(path)
    return sorted(files)


def detected_sensitive_labels(content: str) -> set[str]:
    """Return the public-repository policy labels matched by *content*."""

    return {
        label
        for label, pattern in SENSITIVE_PATTERNS.items()
        if pattern.search(content)
    }


def validate_sensitive_content() -> int:
    files = public_text_files()
    for path in files:
        content = path.read_text(encoding="utf-8")
        for label, pattern in SENSITIVE_PATTERNS.items():
            match = pattern.search(content)
            if match:
                line = content.count("\n", 0, match.start()) + 1
                fail(f"{path.relative_to(ROOT)}:{line}: detected {label}")
    return len(files)


MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
MERMAID_BLOCK = re.compile(r"```mermaid\s*\n(.*?)```", re.DOTALL)
MERMAID_STARTS = ("flowchart ", "graph ", "sequenceDiagram", "stateDiagram", "classDiagram")


def validate_markdown() -> tuple[int, int]:
    markdown_files = sorted(ROOT.rglob("*.md"))
    checked_links = 0
    mermaid_blocks = 0

    for path in markdown_files:
        text = path.read_text(encoding="utf-8")
        for raw_target in MARKDOWN_LINK.findall(text):
            target = raw_target.strip().strip("<>")
            if target.startswith(("https://", "http://", "mailto:", "#")):
                if target.startswith(("http://", "https://")) and " " in target:
                    fail(f"{path.relative_to(ROOT)}: malformed external link: {target}")
                checked_links += 1
                continue

            local_target = unquote(target.split("#", 1)[0])
            if not local_target:
                checked_links += 1
                continue
            resolved = (path.parent / local_target).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError as exc:
                raise ValueError(
                    f"{path.relative_to(ROOT)}: local link escapes repository: {target}"
                ) from exc
            if not resolved.exists():
                fail(f"{path.relative_to(ROOT)}: missing local link target: {target}")
            checked_links += 1

        blocks = MERMAID_BLOCK.findall(text)
        if text.count("```mermaid") != len(blocks):
            fail(f"{path.relative_to(ROOT)}: unclosed Mermaid code fence")
        for block in blocks:
            first_line = next((line.strip() for line in block.splitlines() if line.strip()), "")
            if not first_line.startswith(MERMAID_STARTS):
                fail(f"{path.relative_to(ROOT)}: unsupported or empty Mermaid block")
        mermaid_blocks += len(blocks)

    if len(MERMAID_BLOCK.findall((ROOT / "README.md").read_text(encoding="utf-8"))) < 1:
        fail("README.md must contain the current connection diagram")
    architecture = (ROOT / "docs" / "architecture.md").read_text(encoding="utf-8")
    if len(MERMAID_BLOCK.findall(architecture)) < 3:
        fail("docs/architecture.md must contain current, sequence, and future diagrams")

    return checked_links, mermaid_blocks


def validate_required_urls() -> None:
    combined = "\n".join(
        [
            (ROOT / "README.md").read_text(encoding="utf-8"),
            (ROOT / "docs" / "architecture.md").read_text(encoding="utf-8"),
        ]
    )
    for url in (
        "https://github.com/Jasujung99/hwpctl",
        "https://github.com/Jasujung99/hwp-live-safe",
    ):
        if url not in combined:
            fail(f"Missing public engine URL: {url}")


def main() -> int:
    try:
        validate_mode_matrix()
        json_count = validate_json_examples()
        toml_count = validate_toml_examples()
        scanned_count = validate_sensitive_content()
        link_count, mermaid_count = validate_markdown()
        validate_required_urls()
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError, tomllib.TOMLDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(
        "Repository validation passed: "
        f"JSON {json_count}, TOML {toml_count}, scanned files {scanned_count}, "
        f"local/external links {link_count}, Mermaid blocks {mermaid_count}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
