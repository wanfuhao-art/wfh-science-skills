#!/usr/bin/env python3
"""Check actual saved replies for leaked internal terms; not a semantic grader."""
import argparse
import json
from pathlib import Path
import re

INTERNAL = re.compile(
    r'frontier|\btickets?\b|claim\s+ledger|tracer\s+bullet|expand[–-]contract|'
    r'\bSchema\b|\bPassport\b|回执|错误码|blocked\s+by|\bMDR\b|\bclaim\b|\bBrief\b|任务|'
    r'\b[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+\b', re.I)
FILES = re.compile(r'(?<![\w.-])(?:[\w.-]+/)*[\w.-]+\.(?:md|csv|json|png|pdf|docx)\b', re.I)


def case_ids(results, overrides=None, cases=None):
    """Use declared cases plus saved directories; never silently cap the sample."""
    ids = set()
    manifest = cases if cases is not None else results / 'evals.json'
    if cases is not None or manifest.is_file():
        data = json.loads(manifest.read_text(encoding='utf-8'))
        entries = data.get('evals') if isinstance(data, dict) else None
        if not isinstance(entries, list) or not entries:
            raise ValueError('Case manifest must contain a nonempty evals list')
        for entry in entries:
            ident = entry.get('id') if isinstance(entry, dict) else None
            if type(ident) is not int or ident <= 0:
                raise ValueError('Case ids must be positive integers')
            if ident in ids:
                raise ValueError(f'duplicate case id: {ident}')
            ids.add(ident)
    for root in (results, overrides):
        if root is None:
            continue
        for path in root.glob('eval-*'):
            match = re.fullmatch(r'eval-([0-9]+)', path.name)
            if not path.is_dir() or not match:
                continue
            ident = int(match[1])
            if ident <= 0 or path.name != f'eval-{ident:02}':
                raise ValueError(f'Noncanonical case directory: {path.name}')
            ids.add(ident)
    if not ids:
        raise ValueError('No evaluation cases found; provide --cases or eval-NN directories')
    return sorted(ids)


def check(results, overrides=None, cases=None):
    rows=[]
    for ident in case_ids(results, overrides, cases):
        case=results/f'eval-{ident:02}'
        source=case
        candidate=overrides/f'eval-{ident:02}' if overrides else None
        if candidate and (candidate/'with_skill/outputs/response.md').is_file():
            source=candidate
        path=source/'with_skill/outputs/response.md'
        if not path.is_file():
            rows.append({'eval_id':ident,'reply_exists':False,'lexical_passed':False,'missing_reply':True})
            continue
        text=path.read_text()
        # File names are compatible internal paths, allowed with a Chinese explanation.
        leaks=INTERNAL.findall(FILES.sub('',text))
        missing=[]
        for found in FILES.finditer(text):
            # Accept a Chinese explanation in the same line, before or after the path.
            line_start=max(0, text.rfind('\n', 0, found.start())+1)
            line_end=text.find('\n', found.end())
            if line_end==-1:
                line_end=len(text)
            sentence=text[line_start:line_end]
            sentence=sentence[:found.start()-line_start]+sentence[found.end()-line_start:]
            if not re.search(r'[一-鿿]', sentence):
                missing.append(found.group())
        rows.append({'eval_id':ident,'reply_exists':True,'source':str(path),
                     'leaked_terms':leaks,'files_without_chinese_explanation':missing,
                     'lexical_passed':not leaks and not missing,
                     'semantic_behavior':'requires artifact and human review; not implied by lexical pass'})
    return rows


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--results',required=True,type=Path)
    parser.add_argument('--overrides',type=Path)
    parser.add_argument('--output',required=True,type=Path)
    parser.add_argument('--cases',type=Path,
                        help='Expected-case manifest; defaults to results/evals.json if present')
    args=parser.parse_args()
    try:
        rows=check(args.results,args.overrides,args.cases)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    summary={'scope':'saved replies; lexical checks only; no claim of real execution',
             'checked':len(rows),'passed':sum(r['lexical_passed'] for r in rows),'results':rows}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'checked':summary['checked'],'passed':summary['passed']},ensure_ascii=False))
    raise SystemExit(0 if summary['checked'] and summary['passed']==summary['checked'] else 1)
