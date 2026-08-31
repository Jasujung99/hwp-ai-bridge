from __future__ import annotations

import string
import sys
import unittest
from pathlib import Path


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


if __name__ == "__main__":
    unittest.main()
