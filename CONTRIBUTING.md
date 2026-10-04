# Contributing

Skills are contracts. A change that publishes without an explicit yes is rejected.

1. Add a folder under `skills/<name>/` with `SKILL.md`. `name` must match the folder.
2. Frontmatter needs `name` and `description`. The description must not use an unescaped apostrophe inside single quotes. This repo uses double quotes.
3. Point `.claude/skills/<name>` at `../../skills/<name>`.
4. Update the leading number in `.claude-plugin/plugin.json` description. `scripts/check_frontmatter.py` fails if it does not match the folder count.
5. Run `python3 scripts/sync_codex_marketplace.py`.
6. Run `python3 scripts/check_no_secrets.py` and `python3 scripts/check_frontmatter.py`.

Do not commit `.env`, filled voice profiles, or story banks that contain private numbers.
