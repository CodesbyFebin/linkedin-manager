---
name: linkedin-approval-gate
description: "Run a pre-publish checklist on a draft. Use before any post, comment, or reply goes out. Blocks publish language until the user says post."
---

# Approval gate

Last desk before anything leaves the machine.

## When to use
- "Check this before I post"
- "Is this safe to approve"

## Checklist
1. Hook inside 210 characters.
2. Length in range for the format (post 900 to 1,300, comment 200 to 350, invite note under 200).
3. No banned filler: leverage, delve, unlock, harness, thrilled, game-changer.
4. Em dashes at or under one per 100 words.
5. Every number traces to the user or the story bank. Flag orphans.
6. No secret, token, customer name, or private log line.
7. Link placement: body has none, first comment holds the URL.
8. Approval token is absent until the user types post or yes.

## Output
A pass/fail table, then the draft unchanged. This skill does not call `lib.publish`. If it fails, point at `linkedin-humanizer`.

## Related
- `linkedin-post-writer`
- `linkedin-humanizer`
- `linkedin-approval-gate`
- `../../references/voice-rules.md`
- `../../references/operator-codesbyfebin.md`
