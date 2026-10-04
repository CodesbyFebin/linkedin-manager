---
name: linkedin-carousel-writer
description: "Turn one claim into a LinkedIn document or carousel script. Use when the user wants slides, a PDF post, or a swipe deck. Not for a single text post (use linkedin-post-writer)."
---

# Carousel writer

Build a document post as a sequence of claims, not a blog pasted onto slides.

## When to use
- "Make a carousel from this note"
- "Turn this post into slides"
- "Script a LinkedIn document"

Not for a single text post. Hand that to `linkedin-post-writer`.

## Steps
1. Read `../../references/voice-profile.md` only if `filled: yes`. Read `../../references/story-bank.md` the same way. Never invent a number.
2. Pull one claim. If the note has three claims, ask which one leads.
3. Write 7 to 10 slides. Slide 1 is the hook, under 12 words. Last slide is one action, not a logo dump.
4. Each middle slide is one sentence plus one receipt (a number, a name, a failed attempt).
5. Show the deck as a numbered list. Wait. Do not publish until the user says post.
6. On approval, publish the caption via `lib.publish` only if the user also approved the caption. The slide file itself is returned for upload. This skill does not invent a file host.

## Hard rules
- No emoji. No hashtag block.
- No "swipe to learn" filler.
- Caption hook in the first 210 characters.
- External link goes in the first comment, not the caption.

## Related
- `linkedin-post-writer`
- `linkedin-humanizer`
- `linkedin-approval-gate`
- `../../references/voice-rules.md`
- `../../references/operator-codesbyfebin.md`
