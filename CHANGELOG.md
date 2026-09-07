# Changelog

## Unreleased

- Added a version-scoped direct-mode edit-review workflow for hwpctl's explicit
  formatting-mark command; preserved safe ownership/approval boundaries and
  distinguished internal HWPX formatting inspection from public live editing.

- Documented the behavioral boundary between `hwp-live-safe v0.3.0-rc.1` and
  the coexistence/safety fixes in main commit `384f84e`.
- Added concrete hybrid-mode rebinding, close, restart, and cross-engine Undo
  rules for `hwpctl` and `hwp-live-safe`.
- Aligned Codex safe-mode approval, timeout, and UTF-8 settings with the engine
  example and made TOML server naming consistent.
- Replaced the global editable `hwpctl` install with isolated source-checkout
  `uv tool` installation guidance for both engines.
- Added Gemini CLI direct, safe, and hybrid examples plus validation coverage.

## 0.1.0 — 2026-09-02

- Recorded the verified Hancom Office 2022 native safe-mode environment for
  [`hwp-live-safe v0.3.0-rc.1`](https://github.com/Jasujung99/hwp-live-safe/releases/tag/v0.3.0-rc.1).
- Linked the safe-engine pre-release and clarified that its initial
  distribution is a tagged GitHub source checkout, not PyPI.
- Released the documentation and configuration hub without expanding the
  separately scoped `hwpctl` direct-mode or hybrid-mode support claims.
- Published the `hwpctl` direct-mode and `hwp-live-safe` safe-mode selection
  guide with Codex, Claude Code, Cursor, and Grok Build examples.
- Added direct, safe, and hybrid architecture diagrams and made the absence of
  automatic transfer, shared locking, and shared Undo explicit.
- Added Windows validation for JSON/TOML examples, links, Mermaid blocks,
  absolute Windows/UNC paths, and token-like values.
- Enabled Discussions routing, private vulnerability reporting, protected
  `main`, monthly Dependabot updates, and the `0.1`/`0.2`/`0.3` milestones.

## Release policy

HWP AI Bridge versions its documentation and configuration hub independently.
`v0.1.0` is distributed through its GitHub Release; this repository does not
publish a package to PyPI. Engine versions, installation methods, and verified
combinations remain independent and are recorded in `docs/compatibility.md`.
