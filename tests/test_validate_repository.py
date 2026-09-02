from __future__ import annotations

import string
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import validate_repository  # noqa: E402


class SensitivePathPatternTests(unittest.TestCase):
    def test_all_drive_letters_and_both_separators_are_rejected(self) -> None:
        for letter in string.ascii_letters:
            for separator in (chr(92), "/"):
                example = letter + ":" + separator + "workspace" + separator + "config.toml"
                with self.subTest(letter=letter, separator=separator):
                    self.assertIn(
                        "Windows drive-absolute path",
                        validate_repository.detected_sensitive_labels(example),
                    )

    def test_unc_path_is_rejected(self) -> None:
        example = chr(92) * 2 + "fileserver" + chr(92) + "share" + chr(92) + "config.toml"

        self.assertIn(
            "Windows UNC path",
            validate_repository.detected_sensitive_labels(example),
        )

    def test_repository_style_values_are_not_paths(self) -> None:
        examples = (
            "https://github.com/Jasujung99/hwp-live-safe",
            "hwp-live-safe",
            "integrations/codex/safe.config.toml.example",
            "mcp_servers.hwp_live_safe",
            "C:",
        )

        for example in examples:
            with self.subTest(example=example):
                labels = validate_repository.detected_sensitive_labels(example)
                self.assertNotIn("Windows drive-absolute path", labels)
                self.assertNotIn("Windows UNC path", labels)


class IntegrationContractTests(unittest.TestCase):
    def test_codex_safe_server_requires_approval_timeouts_and_utf8_env(self) -> None:
        path = validate_repository.INTEGRATIONS / "codex" / "safe.config.toml.example"
        with self.assertRaisesRegex(ValueError, "default_tools_approval_mode"):
            validate_repository.validate_safe_server(
                path,
                "hwp_live_safe",
                {
                    "command": "hwp-live-safe",
                    "startup_timeout_sec": 30,
                    "tool_timeout_sec": 90,
                    "enabled": True,
                    "env": {"PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1"},
                },
                toml=True,
            )

    def test_safe_server_name_is_stable_by_config_format(self) -> None:
        path = validate_repository.INTEGRATIONS / "grok-build" / "safe.config.toml.example"
        with self.assertRaisesRegex(ValueError, "hwp_live_safe"):
            validate_repository.validate_safe_server(
                path,
                "hwp-live-safe",
                {"command": "hwp-live-safe", "startup_timeout_sec": 30},
                toml=True,
            )

    def test_mode_matrix_requires_all_three_examples(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for client in validate_repository.REQUIRED_CLIENTS:
                directory = root / client
                directory.mkdir()
                for mode in validate_repository.REQUIRED_MODES:
                    if client == "gemini" and mode == "safe":
                        continue
                    (directory / f"{mode}.json.example").write_text("{}", encoding="utf-8")
            with patch.object(validate_repository, "INTEGRATIONS", root):
                with self.assertRaisesRegex(ValueError, "gemini: missing modes: safe"):
                    validate_repository.validate_mode_matrix()


if __name__ == "__main__":
    unittest.main()
