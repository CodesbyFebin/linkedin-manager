---
name: linkedin-first-comment
description: "Draft the first comment that holds the link for an approved post. Use after a post is approved and needs a URL out of the body."
---

# First comment

The link lives here, not in the post.

## Steps
1. Require the approved post and the URL. If either is missing, ask.
2. Draft one comment under 200 characters that names the artifact and carries the URL.
3. Run `python3 scripts/approval_gate.py --format comment` on it. A URL is expected in this comment, so ignore the link FAIL and say so.
4. Show it. Wait. Do not post the comment until the user says post.

## Related
- `linkedin-approval-gate`
- `linkedin-humanizer`
- `../../references/voice-rules.md`
