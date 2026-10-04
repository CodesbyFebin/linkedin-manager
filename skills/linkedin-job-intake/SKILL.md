---
name: linkedin-job-intake
description: "Parse a job the user pasted or saved. Use when a role needs to enter the hunter desk. Refuses live scraping, cookie login, and bulk board crawls."
---

# Job intake

A role enters the desk only as text the user already has.

## When to use
- "Here is a job description"
- "File this role"

## Refuse
- Scrape LinkedIn, Indeed, or Naukri.
- Log in with cookies, a session, or a headless browser.
- Crawl a search results page.

## Steps
1. Require the pasted description. A URL alone is not enough. Ask the user to paste the description.
2. Run `python3 scripts/job_fit.py <file>` and show the table.
3. Write a one-line role card: title, location, mode, one requirement, one unknown.
4. Save nothing off the machine. Hand the card to `linkedin-job-fit`.

## Related
- `linkedin-job-intake`
- `linkedin-job-fit`
- `linkedin-approval-gate`
- `../../references/untrusted-content.md`
