# Analysis — LinkedIn Manager

Source analysed: https://github.com/sergebulaev/linkedin-skills (public, MIT, ~4k stars, Python, v1.1.16).

## What it is

A terminal-native LinkedIn content system for Claude Code, Codex, Claude Desktop, OpenClaw, and Hermes. It is not a bot that posts on a timer. Every write skill drafts, shows the draft, and waits for an explicit approval token (`post` / `yes`) before `lib/publora_client.py` or a custom poster runs.

Twelve skills:

| Skill | Job |
|---|---|
| `linkedin-interviewer` | Builds `references/story-bank.md` from an interview. Start here if there is no post history. |
| `linkedin-post-writer` | Picks a hook formula by goal, drafts 900–1,300 chars, hook inside first 210 chars. |
| `linkedin-humanizer` | Strips AI tells, audit mode, emoji density, detector spread, voice fingerprint. |
| `linkedin-comment-drafter` | First comments on other people's posts, in voice, no product name-drop. |
| `linkedin-reply-handler` | Single reply or whole-thread sweep from a post URL. |
| `linkedin-hook-extractor` | Pulls a reusable formula from a viral post. |
| `linkedin-content-planner` | Week plan. Founder pillar set or general pillar set. |
| `linkedin-profile-optimizer` | Headline, About, banner, experience. |
| `linkedin-repurposer` | Tweet / video / blog → native LinkedIn post. |
| `linkedin-employee-advocacy` | Team amplification playbook. |
| `linkedin-thread-monitor` | Which of your comments got an author reply. |
| `linkedin-engager-analytics` | Likers + commenters, ICP segmentation. |

Root `SKILL.md` is the router (`name: linkedin-marketing`). It points the agent at the skill that matches the request.

## Layout (exact setup preserved)

```
SKILL.md                 router
skills/*/SKILL.md        one contract per skill
references/              shared research + personal templates
lib/                     Python clients, no network until called
scripts/                 check_config, selftest, schedule_post, post_comment
tests/ + evals/          contract and shape tests
.claude/skills/          symlinks so Claude Code discovers skills
.claude-plugin/          Claude marketplace + plugin.json
.codex-plugin/           Codex plugin manifest
.codex-marketplace/      nested package Codex requires
.agents/plugins/         agents marketplace pointer
.env.example             optional Apify / Publora / Pixfaro
```

Codex cannot point a marketplace entry at the repo root the way Claude can. `scripts/sync_codex_marketplace.py` copies the public surface into `.codex-marketplace/linkedin-manager` and refuses to sync a filled `voice-profile.md` or `story-bank.md`.

## Runtime tiers

1. **Tier 0 — draft only.** No keys. Approved draft comes back as a paste block.
2. **Tier 1 — Publora.** `PUBLORA_API_KEY` + `LINKEDIN_PLATFORM_ID`. Posts and comments on approval. Free tier cited as 15 LinkedIn posts/month.
3. **Tier 2 — custom poster.** `LINKEDIN_SKILLS_CUSTOM_POSTER=<command>`.

Read path is optional Apify (`APIFY_TOKEN`): post body, comments, own recent comments, engagers. No cookies, no LinkedIn login in the actors they pin. Image path is optional Pixfaro (`PIXFARO_TOKEN`); without it the skill returns a prompt.

Fetched LinkedIn text is untrusted data. Rule file: `references/untrusted-content.md`. It cannot approve a post or rewrite the skill instructions.

## Voice and research spine

Hard rules in `references/voice-rules.md` and the router: em dash cap, no AI vocabulary (`leverage`, `delve`, `unlock`…), numbers over adjectives, comments 200–350 chars, one insight plus a hook. Personal voice loads only when `references/voice-profile.md` has `filled: yes`. Story material loads from `references/story-bank.md`. Both ship empty on purpose.

Founder layer: `references/founder-topics.md` angles A1–A10, formulas F17–F20, planner pillar swap (Conviction / Building in public / The math / Proof).

## CodesbyFebin operator fit

Default overlay lives in `references/operator-codesbyfebin.md`. It is not auto-loaded. Copy the fingerprint into `references/voice-profile.md` and set `filled: yes` after you confirm it still sounds like you. Intended lane: systems engineer, verifiable compute, evidence over adjectives, Kerala / India operator, no growth-hack voice.

Suggested first session:

1. `python3 scripts/check_config.py`
2. Run `linkedin-interviewer` and fill the story bank (receipts, not slogans).
3. Paste 3–6 real posts into `linkedin-humanizer --mode profile` if you have them.
4. Draft with `linkedin-post-writer`. Audit with `linkedin-humanizer`. Publish only after you say post.

## What this distribution does not add

No unofficial LinkedIn cookie login, no headless browser poster, no autopilot cron. Those were not in the upstream setup, and they are the part that gets accounts restricted.
