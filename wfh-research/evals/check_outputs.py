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


def check(results, overrides=None):
    rows=[]
    for ident in range(1,11):
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
    args=parser.parse_args()
    rows=check(args.results,args.overrides)
    summary={'scope':'ten real saved replies; lexical checks only',
             'checked':len(rows),'passed':sum(r['lexical_passed'] for r in rows),'results':rows}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'checked':summary['checked'],'passed':summary['passed']},ensure_ascii=False))
    raise SystemExit(0 if summary['passed']==10 else 1)
