# Attribution

This repository is a fresh CodesbyFebin distribution of the LinkedIn skill bundle.

| | |
|---|---|
| Upstream | [sergebulaev/linkedin-skills](https://github.com/sergebulaev/linkedin-skills) |
| Upstream version mirrored | v1.1.16 (tree SHA `2f00424615b9853e8b1aa003d8752179bbeabb09`, 2026-10-03) |
| Upstream copyright | Copyright (c) 2026 Sergey Bulaev |
| License | MIT. The original notice in `LICENSE` is retained. |
| This distribution | CodesbyFebin / Febin Francis |
| Plugin id | `linkedin-manager` |
| Repo | https://github.com/CodesbyFebin/linkedin-manager |

What was kept identical:

- 12 skill directories and their `SKILL.md` contracts
- `lib/` clients (`url_parser`, `apify_client`, `publora_client`, `pixfaro_client`, `backend_selector`, `approval`)
- `references/` research files (hooks, algorithm heuristics, founder angles, voice rules)
- `scripts/` selftest, config check, schedule/comment helpers
- `tests/`, `evals/`, requirements pins
- Draft → show → wait for explicit approval before any publish call

What this distribution changes:

- Install coordinates (`CodesbyFebin/linkedin-manager`, plugin `linkedin-manager`)
- Marketplace and plugin manifests (author/maintainer, brand color `#00ff00`)
- Nested Codex package path `.codex-marketplace/linkedin-manager`
- `references/operator-codesbyfebin.md` operator overlay (not auto-loaded; copy into `voice-profile.md` to activate)
- `ANALYSIS.md` architecture notes

Do not strip the upstream copyright if you redistribute.
