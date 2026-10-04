# Repository review and upgrade

Reviewed baseline: `2667ec446d086ff320487b80fb0eff8024396fdf` (main, 2026-10-04).
Upgrade manifest version: 1.4.3. A versioned manifest is not a published release.

## Findings and fixes

| Finding | Effect | Upgrade |
|---|---|---|
| 40 source skills, but contributor rules and interface text still said 12 | Incorrect installation and maintenance guidance | Aligned counts, rules, interface description, README, and citation |
| Plugin manifests said 1.4.1 while citation said 1.4.2 | Different consumers saw different versions | Aligned release metadata at 1.4.3 |
| Template restoration used `.codex-marketplace/linkedin-skills` after package rename | Generated installations silently lost Voice Profile and Story Bank | Restore pristine tracked templates from the current path, bootstrap from tracked root, fail if unavailable or filled |
| Packaged license and social card were stale | Codex installation differed from repository source | Regenerated the package; CI now checks drift |
| Three existing instruction tests failed | New skills lacked routing and shared-rule references | Repaired descriptions and hard-rule references without weakening those tests |
| Scheduling CLI did not ask for approval | A direct CLI invocation could schedule immediately | Full preview, account display, interactive confirmation, prior-approval flag, EOF refusal |
| Schedule used host timezone | Cloud servers could schedule at the wrong local hour | Default Asia/Kolkata; configurable IANA timezone |
| Publora POSTs retried on ambiguous failures | Duplicate posts/comments possible after server acceptance | Send POST once; caller must reconcile outcome before retrying |
| Credential detector matched the words token, secret, and password | Technical writing was falsely blocked | Match credential assignments and recognizable token prefixes; detector remains a heuristic |
| Skill index extracted descriptions incompletely at escaped quotes | Broken discovery text for several established skills | Parse YAML, generate complete linked Markdown and JSON catalogs |
| Pages index had minimal content and no mobile viewport | Weak browsing and discovery surface | Responsive complete skill catalog, canonical Pages URL, OG/Twitter metadata, schema, local social asset, llms.txt, sitemap |
| Selftest --offline still fetched actor schemas | Offline flag did not prevent all network access | Skip remote schema validation in offline mode; preserve explicit skipped status |
| Selftest compared filenames rather than generated contents | Previously modified generated files could conceal drift | Compare content hashes and check sync exit status |
| Selftest omitted 28 newer desks | Incomplete capability reporting | Map all 40 workflows explicitly |

## Validation

- 136 offline unit tests pass, including approval refusal/confirmation, dry-run, timezone handling, non-replayed POST failures, catalog fidelity, manifest parity, symlink targets, and template privacy.
- Library import smoke test, byte compilation, frontmatter, Markdown reference validation, catalog freshness, credential wiring in offline mode, tracked secret scan, and selftest --offline pass.
- Social preview asset is 1280 × 640, 34,810 bytes. This validates the repository file, not GitHub's social-preview upload endpoint.
- Remote Apify schema validation passes: five intercepted calls across four actors, with all supplied keys declared and required keys set. This validates public input schemas, not live account behavior.

## Remaining boundaries

- GitHub Pages activation and the repository social-preview setting require separate configuration. Committing `/docs` does not enable either setting.
- No live Apify, Publora, or Pixfaro accounts were configured here. Live reads, scheduling, images, and platform permissions remain unqualified.
- `--approved` is an operator attestation. Low-level `lib.publish` and client methods still require approval enforcement by their caller; they are not an authorization boundary.
- Other platform desks and job application workflows remain drafting tools, not automated sends or applications.
- Existing claims about conversion improvements, viral formulas, and preferred engagement windows require empirical evidence. Offline correctness tests do not measure content quality or platform ranking.
- Optional Apify and Pixfaro clients also contain retry policies around billed calls. Provider-supported idempotency and billing reconciliation should be assessed before claiming exactly-once execution across all integrations.
- Search indexing, answer-engine citations, stars, forks, and community adoption are external outcomes. Metadata and community-health files cannot guarantee them.

## Reproduction

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/build_catalog.py --check
python3 scripts/sync_codex_marketplace.py
python3 scripts/check_frontmatter.py
python3 scripts/check_markdown_references.py
python3 scripts/check_no_secrets.py
python3 scripts/check_config.py --offline
python3 -m unittest discover -s tests
python3 scripts/selftest.py --offline
```
