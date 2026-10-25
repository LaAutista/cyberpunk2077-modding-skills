#!/usr/bin/env python3
"""Find local CP2077 references and return paths, source URLs, and excerpts."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('query')
    parser.add_argument('--group', help='Collection name or part of its path')
    parser.add_argument('--limit', type=int, default=8)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    terms = args.query.casefold().split()
    if not terms or args.limit < 1:
        parser.error('Supply a nonempty query and a positive limit.')
    catalog = ROOT / 'docs/catalog.json'
    if not catalog.exists():
        parser.error('Run tools/build-doc-index.py first.')
    results = []
    for entry in json.loads(catalog.read_text(encoding='utf-8')):
        path = (ROOT / 'docs' / entry['file']).resolve()
        relative = path.relative_to(ROOT).as_posix()
        if args.group and args.group.casefold() not in (entry['group'] + ' ' + relative).casefold():
            continue
        text = path.read_text(encoding='utf-8',errors='replace').split('# Agent Instructions')[0]
        title = entry['title'].casefold()
        haystack = (title + '\n' + text).casefold()
        if not all(term in haystack for term in terms):
            continue
        score = sum(20 * (term in title) + min(haystack.count(term), 8) for term in terms)
        score += 4 * ('/scripting-cyberpunk/' in relative)
        score += 8 * ('/guides/' in relative)
        score += 8 * (entry['group'] in {'tweakxl-wiki', 'archivexl-wiki', 'codeware-wiki', 'red4ext'})
        lines = text.splitlines()
        candidates = [(sum(term in line.casefold() for term in terms), n, line.strip())
                      for n, line in enumerate(lines, 1)
                      if line.strip() and not line.startswith('> For the complete documentation index,')]
        _, line_no, excerpt = max(candidates, key=lambda row: (row[0], -row[1])) if candidates else (0, 1, '')
        results.append({'title': entry['title'], 'path': str(path), 'line': line_no,
                        'source': entry['url'], 'group': entry['group'],
                        'excerpt': excerpt[:300], 'score': score})
    results.sort(key=lambda row: (-row['score'], row['title']))
    found = results[:args.limit]
    if args.json:
        print(json.dumps({'total': len(results), 'results': found}, indent=2))
    else:
        print(f'{len(results)} matching documents; showing {len(found)}')
        for row in found:
            print(f"\n{row['title']} [{row['group']}]\n{row['path']}:{row['line']}\n{row['excerpt']}\nSource: {row['source']}")

if __name__ == '__main__':
    main()
