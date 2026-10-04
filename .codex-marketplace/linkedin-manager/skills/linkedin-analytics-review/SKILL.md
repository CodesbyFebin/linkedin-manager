---
name: linkedin-analytics-review
description: "Read pasted LinkedIn analytics and say what to repeat. Use when the user pastes impressions, comments, or a screenshot transcription. Not for scraping."
---

# Analytics review

Interpret numbers the user already has. Do not fetch private analytics.

## When to use
- "Here are last month's posts, what worked"
- "Impressions dropped, read this export"

## Steps
1. Accept pasted rows or a transcription. If the paste is empty, ask for it.
2. Rank posts by comments, then saves, then impressions. Say which signal you used.
3. Name the pattern: hook type, length, day, proof vs opinion.
4. Recommend three next drafts. Point each at `linkedin-post-writer` or `linkedin-case-receipt`.
5. Do not publish anything from this skill.

## Hard rules
- Do not invent a baseline the paste does not contain.
- Do not tell the user to buy reach.

## Related
- `linkedin-post-writer`
- `linkedin-humanizer`
- `linkedin-approval-gate`
- `../../references/voice-rules.md`
- `../../references/operator-codesbyfebin.md`
