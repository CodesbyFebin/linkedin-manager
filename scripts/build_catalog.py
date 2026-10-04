#!/usr/bin/env python3
"""Generate linked human and machine skill catalogs. --check refuses stale outputs."""
from __future__ import annotations
import argparse
import html
import json
import re
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
REPO = 'https://github.com/CodesbyFebin/linkedin-manager'
SITE = 'https://codesbyfebin.github.io/linkedin-manager/'


def outputs() -> dict[str, str | bytes]:
    manifest = json.loads((ROOT / '.codex-plugin/plugin.json').read_text())
    skills = []
    for path in sorted((ROOT / 'skills').glob('*/SKILL.md')):
        data = yaml.safe_load(path.read_text().split('---', 2)[1])
        skills.append({'name': data['name'], 'description': data['description'],
                       'path': str(path.relative_to(ROOT)),
                       'url': f'{REPO}/blob/main/{path.relative_to(ROOT)}'})
    catalog = {'name': manifest['name'], 'version': manifest['version'],
               'repository': REPO, 'license': manifest['license'],
               'skill_count': len(skills), 'skills': skills}
    markdown = f'# Skill index\n\n{len(skills)} skills. Generated from YAML frontmatter with `python3 scripts/build_catalog.py`.\n\n'
    markdown += '\n'.join(f"- [{s['name']}]({s['path']}) - {s['description']}" for s in skills) + '\n'
    cards = '\n'.join(f'<li><h3><a href="{s["url"]}">{html.escape(s["name"])}</a></h3><p>{html.escape(s["description"])}</p></li>' for s in skills)
    summary = f'{len(skills)} agent skills for LinkedIn, X, Instagram, YouTube, and WhatsApp. Draft, audit, approve. Optional APIs; publishing requires approval.'
    schema = {'@context': 'https://schema.org', '@type': 'SoftwareSourceCode',
              'name': 'LinkedIn Manager', 'codeRepository': REPO,
              'url': SITE, 'programmingLanguage': 'Python',
              'version': manifest['version'], 'license': 'https://opensource.org/licenses/MIT',
              'author': {'@type': 'Person', 'name': 'Febin Francis',
                         'url': 'https://github.com/CodesbyFebin'}, 'description': summary}
    page = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>LinkedIn Manager by CodesbyFebin | 40 Agent Skills</title>
<meta name="description" content="SUMMARY">
<meta name="author" content="Febin Francis">
<meta property="og:title" content="LinkedIn Manager by CodesbyFebin">
<meta property="og:description" content="SUMMARY">
<meta property="og:image" content="SITEassets/social-preview.png">
<meta property="og:image:width" content="1280">
<meta property="og:image:height" content="640">
<meta property="og:image:alt" content="LinkedIn Manager by CodesbyFebin: draft, audit, approve">
<meta property="og:url" content="SITE">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="LinkedIn Manager by CodesbyFebin">
<meta name="twitter:description" content="SUMMARY">
<meta name="twitter:image" content="SITEassets/social-preview.png">
<link rel="canonical" href="SITE">
<link rel="alternate" type="application/json" href="skills.json" title="Skill catalog">
<script type="application/ld+json">SCHEMA</script>
<style>
:root{color-scheme:dark;font-family:system-ui,sans-serif;background:#0b1010;color:#e8f0ed}
*{box-sizing:border-box}body{margin:0}main{max-width:1100px;margin:auto;padding:48px 24px}
a{color:#6cefa7;text-underline-offset:4px}a:focus-visible{outline:2px solid #6cefa7;outline-offset:5px}
h1{font-size:clamp(2.3rem,7vw,4.8rem);line-height:1.05;letter-spacing:-.05em;margin:20px 0}
h2{margin-top:48px}p{line-height:1.7;max-width:78ch}.eyebrow{font-family:monospace;color:#6cefa7}
nav{display:flex;gap:24px;flex-wrap:wrap}code{overflow-wrap:anywhere;color:#6cefa7}
ul.catalog{padding:0;list-style:none;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:16px}
.catalog li{padding:20px;border:1px solid #294039;border-radius:12px;background:#111a17}.catalog h3{margin:0;font-size:1rem;overflow-wrap:anywhere}.catalog p{font-size:.9rem;color:#bdcec6;margin-bottom:0}
footer{margin-top:48px;border-top:1px solid #294039;padding-top:24px;color:#bdcec6}
</style>
</head>
<body><main>
<p class="eyebrow">CODESBYFEBIN / OPEN SOURCE / VERSION</p>
<h1>Draft. Audit. Approve.</h1>
<p>LinkedIn Manager is a desk of 40 agent skills for writing, reviewing, planning, and career workflows across LinkedIn, X, Instagram, YouTube, and WhatsApp.</p>
<nav aria-label="Project resources"><a href="REPO">GitHub repository</a><a href="#skills">Browse 40 skills</a><a href="skills.json">JSON catalog</a><a href="llms.txt">Machine summary</a></nav>
<h2>Start with a draft</h2>
<p>In Claude Code, add the marketplace with <code>/plugin marketplace add CodesbyFebin/linkedin-manager</code>, then install <code>/plugin install linkedin-manager</code>. For Codex and other supported agents, follow the repository installation guide.</p>
<p>No API key is needed to draft. Optional Apify reads retrieve public post data; Publora schedules or publishes approved content; Pixfaro creates visuals. These services can charge for usage. X, Instagram, YouTube, WhatsApp, and job application desks draft material for you to review and send.</p>
<h2>What does approval mean?</h2>
<p>The agent presents the complete action and target for review. The scheduling CLI requires interactive confirmation or <code>--approved</code> after prior explicit approval of the exact draft, account, and schedule. Low-level Python API clients expect the caller to enforce approval; they do not provide an authorization boundary.</p>
<h2 id="skills">The complete skill desk</h2>
<ul class="catalog">CARDS</ul>
<h2>Does this guarantee ranking or reach?</h2>
<p>No. Metadata and linked catalogs help readers and crawlers understand the project. They cannot guarantee indexing, citations, stars, forks, or engagement. Examples and recorded fixtures are not live platform qualification.</p>
<footer>MIT licensed. Built by <a href="https://github.com/CodesbyFebin">Febin Francis / CodesbyFebin</a>. <a href="REPO/blob/main/SECURITY.md">Security policy</a> · <a href="REPO/blob/main/CITATION.cff">Citation</a></footer>
</main></body></html>
'''
    for token, value in [('SUMMARY', html.escape(summary, quote=True)), ('SITE', SITE),
                          ('SCHEMA', json.dumps(schema)), ('VERSION', manifest['version']),
                          ('REPO', REPO), ('CARDS', cards)]:
        page = page.replace(token, value)
    llms = f'''# LinkedIn Manager
> {summary}

Version: {manifest['version']}
License: MIT
Maintainer: Febin Francis (CodesbyFebin)

## Documentation
- [Repository]({REPO}): Installation, supported APIs, approval workflow, and limitations.
- [Skill index]({REPO}/blob/main/SKILLS.md): All {len(skills)} skills with full descriptions and source links.
- [JSON catalog]({SITE}skills.json): Names, paths, descriptions, version, and source URLs.
- [Root workflow]({REPO}/blob/main/SKILL.md): Routing and shared rules.
- [Security]({REPO}/blob/main/SECURITY.md): Credential handling and reporting.

## Boundaries
No API key is needed for drafting. Optional Apify reads, Publora writes, and Pixfaro images require separate service accounts and may be billed.
The scheduling CLI prompts for approval unless --approved attests prior approval of the exact action. Low-level library callers must enforce approval themselves.
Other platform desks and job application skills produce drafts, not automated sends or applications.
Metadata does not guarantee indexing, answer-engine citations, engagement, stars, or forks.
'''
    serialized = json.dumps(catalog, ensure_ascii=False, indent=2) + '\n'
    return {'SKILLS.md': markdown, 'skills.json': serialized, 'llms.txt': llms,
            'docs/index.html': page, 'docs/skills.json': serialized, 'docs/llms.txt': llms,
            'docs/assets/social-preview.png': (ROOT / 'assets/social-preview.png').read_bytes(),
            'docs/.nojekyll': '',
            'docs/sitemap.xml': f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{SITE}</loc></url></urlset>\n'}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    stale = []
    for name, value in outputs().items():
        path = ROOT / name
        expected = value if isinstance(value, bytes) else value.encode('utf-8')
        if not path.is_file() or path.read_bytes() != expected:
            stale.append(name)
            if not args.check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(expected)
    if args.check and stale:
        print('Stale catalog outputs: ' + ', '.join(stale))
        return 1
    print('Catalog verified.' if args.check else 'Catalog generated.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
