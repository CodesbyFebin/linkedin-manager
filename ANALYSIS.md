# CodesbyFebin agent desk

Public brand is CodesbyFebin only. Install id is `linkedin-manager`.

## What other social skill repos do

The common pattern across X, Instagram, and YouTube skill bundles is the same loop: parse a URL, draft in a voice file, wait for an explicit yes, then call a publisher. Scraping repos sit on the other side of that line. They log in, crawl, and post. Those get accounts restricted. This repo keeps the loop and drops the crawl.

## This tree

- LinkedIn skills draft and gate.
- Job hunter skills take a paste. They do not apply.
- Four agent desks cover X, Instagram, YouTube, and WhatsApp with the same yes-token.
- `scripts/approval_gate.py` and `scripts/job_fit.py` are local. No network.

Nothing in this repo sends until the operator types post or yes.
