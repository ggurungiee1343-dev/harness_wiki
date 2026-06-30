---
description: 'Harness safety & compliance checker (vault version). Executes binary
  questions against the Hermes environment and returns per‑dimension scores. Stored
  in the Obsidian vault for easy reference.

  '
name: harness-check-vault
tags: []
version: 0.1.0
---
## Overview
Implements the binary‑question evaluation pattern from *Ask, Don’t Judge*. Checks process safety, routing integrity, meta‑doc timestamps, and prompt length.

## Binary Questions
Implemented in `scripts/check.py` (see the vault folder). Each question returns `(bool, explanation)`.

## Usage
```bash
hermes skill run harness-check-vault
```

## Development
- Uses `hermes_tools` for shell commands and file reads.
- All paths are absolute and respect `constitution.local.md`.
- Read‑only; no side effects.

## Future Extensions
- Nightly cron job.
- `--fix` flag to auto‑apply safe fixes.

## References
- Cho et al., *Ask, Don’t Judge* (2026).
- MJ님 `constitution.local.md` – path rules, single instance, routing.

## License
MIT

---
*최종 업데이트: 2026-06-30 22:45*