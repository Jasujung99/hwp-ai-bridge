# Changelog

## Unreleased

- No unreleased changes.

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
