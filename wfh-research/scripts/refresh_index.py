#!/usr/bin/env python3
"""Generate/check navigation from explicit ARS root and sibling wfh skills (stdlib)."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
from urllib.parse import quote

WFH_SUPPORT = {
    'wfh': ('dispatch_protocol.md', 'user_output_protocol.md', 'ars_intent_map.md'),
    'wfh-grill': ('grilling_protocol.md', 'decision_classes.md', 'terms_template.md',
                  'mdr_template.md', 'reopen_template.md'),
    'wfh-spec': ('spec_template.md', 'ars_handoff_protocol.md'),
    'wfh-tickets': ('tickets_template.md', 'flow_template.md', 'spec_template.md'),
    'wfh-ask': ('routing_protocol.md', 'skills_index.md', 'state_protocol.md', 'flow_template.md'),
    'wfh-next': ('state_protocol.md', 'tickets_template.md', 'ars_handoff_protocol.md'),
    'wfh-close': ('state_protocol.md', 'flow_template.md', 'tickets_template.md',
                  'ars_handoff_protocol.md', 'reopen_template.md'),
    'wfh-implement-spec': ('state_protocol.md', 'tickets_template.md', 'ars_handoff_protocol.md'),
}


def metadata(text):
    """Read only top-level scalar name/description; reject unsupported YAML forms."""
    match = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)', text, re.S)
    if not match:
        raise ValueError('missing frontmatter')
    result = {}
    for key in ('name', 'description'):
        value = re.search(r'^' + key + r':\s*(.+)$', match[1], re.M)
        if not value or value[1].strip() in ('|', '>', '|-', '>-'):
            raise ValueError('missing/unsupported scalar ' + key)
        result[key] = value[1].strip().strip('\"\'')
    return result


def registry_rows(text):
    """Read every mode table under each skill heading; never cap at 35."""
    rows, section, table = [], None, False
    for line in text.splitlines():
        if line.startswith('## '):
            section = re.match(r'## ([a-z][a-z-]+)\s+\(', line)
            section = section[1] if section else None
            table = False
        if section and line.startswith('| Mode |'):
            table = True
            continue
        if table and line.startswith('|') and not re.match(r'^\|\s*-', line):
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            if len(cells) != 5:
                raise ValueError('unrecognized registry row: ' + line)
            rows.append((section, cells[0].strip('`'), cells[2], cells[4]))
    if not rows:
        raise ValueError('registry contains no mode rows')
    if len({(r[0], r[1]) for r in rows}) != len(rows):
        raise ValueError('duplicate skill/mode')
    # Headers may lag; expose mismatch, do not discard actual rows.
    declared = re.search(r'\*\*(\d+) modes\*\*', text)
    diagnostics = []
    if declared and int(declared[1]) != len(rows):
        diagnostics.append(f'INDEX_INVALID: declared {declared[1]} modes, actual {len(rows)}')
    headings = re.findall(r'^## ([a-z][a-z-]+)\s+\(([^\n]+)\)', text, re.M)
    for skill, counts in headings:
        expected = sum(map(int, re.findall(r'\b\d+\b', counts)))
        actual = sum(r[0] == skill for r in rows)
        if expected != actual:
            diagnostics.append(f'INDEX_INVALID: {skill} declared {expected}, actual {actual}')
    return rows, diagnostics


def build(skills, ars, output):
    sources, diagnostics = {}, []

    def logical(path):
        if path == Path(__file__).resolve():
            return 'generator/refresh_index.py'
        # Check ARS first: an explicitly supplied root may be inside the suite.
        if ars is not None and path.is_relative_to(ars):
            return 'ars/' + path.relative_to(ars).as_posix()
        if path.is_relative_to(skills):
            return 'wfh/' + path.relative_to(skills).as_posix()
        return 'generator/' + path.name

    def read(path):
        try:
            data = path.read_bytes()
            sources[path] = data
            return data.decode('utf-8')
        except (OSError, UnicodeError) as exc:
            reason = exc.strerror if isinstance(exc, OSError) else 'invalid UTF-8'
            diagnostics.append(f'INDEX_INVALID: {logical(path)}: {reason}')
            return None

    def manifest(path):
        text = read(path)
        try:
            data = json.loads(text) if text is not None else None
            if not isinstance(data, dict):
                raise ValueError('expected manifest object')
            return data
        except (ValueError, TypeError) as exc:
            diagnostics.append(f'INDEX_INVALID: {logical(path)}: {exc}')
            return {}

    def link(path, label):
        # Suite references stay relative so the package can move together. ARS
        # locations are written relative to the recorded root, never as links to
        # a versioned cache path.
        return f'[{label}]({quote(os.path.relpath(path, output.parent), safe="/.-_")})'

    def ars_path(path):
        return f'`{path.relative_to(ars).as_posix()}`'

    def cell(text):
        return text.replace('|', '\\|').replace('\n', ' ')

    package = skills / 'wfh-research'
    plugin = manifest(skills / '.claude-plugin/plugin.json')
    market = manifest(skills / '.claude-plugin/marketplace.json')
    entries = market.get('plugins', [])
    candidates = [p for p in entries if isinstance(p, dict) and p.get('name') == plugin.get('name')] if isinstance(entries, list) else []
    if len(candidates) != 1 or candidates[0].get('skills') != plugin.get('skills'):
        diagnostics.append('INDEX_INVALID: plugin and marketplace skill lists differ')
    declared = plugin.get('skills', [])
    if not isinstance(declared, list):
        diagnostics.append('INDEX_INVALID: skills must be a list')
        declared = []
    valid = [p for p in declared if isinstance(p, str) and re.fullmatch(r'\./[a-z][a-z0-9-]*', p)]
    if len(valid) != len(declared) or len(set(valid)) != len(valid):
        diagnostics.append('INDEX_INVALID: invalid or duplicate skill directory')
    names = sorted({p[2:] for p in valid})
    actual = {p.parent.name for p in skills.glob('wfh*/SKILL.md')}
    if set(names) != actual:
        diagnostics.append('INDEX_INVALID: manifest and skill directories differ')
    if 'wfh' not in names or 'wfh-research' not in names:
        diagnostics.append('INDEX_INVALID: default entry or shared package missing')
    wfh = [n for n in names if n != 'wfh-research']
    wfh_rows = []
    for name in wfh:
        path = skills / name / 'SKILL.md'
        text = read(path)
        try:
            data = metadata(text) if text is not None else None
            if data and data['name'] != name:
                raise ValueError('frontmatter name differs from directory')
            if data:
                header = text.split('---', 2)[1]
                disabled = bool(re.search(r'^disable-model-invocation:\s*true\s*$', header, re.M))
                if (name == 'wfh' and disabled) or (name != 'wfh' and not disabled):
                    raise ValueError('default/advanced invocation role differs from manifest role')
        except ValueError as exc:
            diagnostics.append(f'INDEX_INVALID: {logical(path)}: {exc}')
            data = None
        support = []
        for ref in WFH_SUPPORT.get(name, ('user_output_protocol.md',)):
            ref_path = package / 'references' / ref
            if ref_path.is_file():
                support.append(link(ref_path, ref.removesuffix('.md')))
            else:
                diagnostics.append(f'INDEX_INVALID: missing shared reference {logical(ref_path)}')
                support.append('MISSING ' + ref)
        wfh_rows.append(f'| {name} | /{name} | {cell(data["description"]) if data else "UNAVAILABLE"} | '
                        f'{link(path, "SKILL") if data else "UNAVAILABLE"} | {"、".join(support)} |')
    # Shared contracts and generator are fingerprinted; never read settings/env.
    shared = read(package / 'SKILL.md')
    try:
        if shared is None or metadata(shared)['name'] != 'wfh-research':
            raise ValueError('shared package name differs from directory')
        header = shared.split('---', 2)[1]
        if not re.search(r'^user-invocable:\s*false\s*$', header, re.M):
            raise ValueError('shared package must not be user-invocable')
    except ValueError as exc:
        diagnostics.append('INDEX_INVALID: ' + str(exc))
    read(Path(__file__).resolve())
    for path in sorted((package / 'references').glob('*.md')):
        if path.name != 'skills_index.md' and path.resolve() != output:
            read(path)
    rows, command_map = [], {}
    ars_identity = '未提供'
    available = ars is not None and (ars / 'MODE_REGISTRY.md').is_file()
    if not available:
        diagnostics.append('ARS_NOT_AVAILABLE: pass --ars-root from a verified current installation')
    else:
        ars_manifest = manifest(ars / '.claude-plugin/plugin.json')
        ars_name = ars_manifest.get('name', '')
        ars_version = ars_manifest.get('version', '')
        if not isinstance(ars_name, str) or not re.fullmatch(r'[a-z][a-z0-9-]*', ars_name) or not isinstance(ars_version, str) or not re.fullmatch(r'[0-9A-Za-z.+-]+', ars_version):
            diagnostics.append('INDEX_INVALID: invalid ARS plugin identity')
        else:
            ars_identity = f'{ars_name}@{ars_version}'
        registry = read(ars / 'MODE_REGISTRY.md')
        try:
            rows, problems = registry_rows(registry or '')
            diagnostics.extend(problems)
        except ValueError as exc:
            diagnostics.append('INDEX_INVALID: ' + str(exc))
        # Read source documents only, in the explicit installation. Changes in mode
        # support files invalidate the cache even when registry descriptions do not.
        for directory in ['shared'] + list(dict.fromkeys(r[0] for r in rows)):
            for path in sorted((ars / directory).rglob('*.md')):
                read(path)
        for path in sorted((ars / 'commands').glob('*.md')):
            text = read(path)
            if text is None:
                continue
            try:
                data = metadata(text)
            except ValueError as exc:
                diagnostics.append(f'INDEX_INVALID: {logical(path)}: {exc}')
                continue
            target = re.search(r'skill:\s*"(?:academic-research-skills|wfh-science-skills):([a-z-]+)"', text)
            if not target:
                continue
            skill = target[1]
            desc_mode = re.search(r'`([^`]+)`', data['description'])
            mode = desc_mode[1] if desc_mode else '(pipeline)' if skill == 'academic-pipeline' else None
            if mode:
                if (skill, mode) not in {(r[0], r[1]) for r in rows}:
                    diagnostics.append(f'INDEX_INVALID: command {path.name} targets absent mode {skill}:{mode}')
                command_map.setdefault((skill, mode), []).append((data['name'], path))

    ars_rows, support_rows = [], []
    for skill in dict.fromkeys(r[0] for r in rows):
        path = ars / skill / 'SKILL.md'
        text = read(path)
        try:
            data = metadata(text) if text is not None else None
            if data and data['name'] != skill:
                raise ValueError('frontmatter name differs from registry')
        except ValueError as exc:
            diagnostics.append(f'INDEX_INVALID: {logical(path)}: {exc}')
            data = None
        navigation = [ars_path(path)] if data else ['UNAVAILABLE']
        for name in ('references', 'agents'):
            if (ars / skill / name).is_dir():
                navigation.append(f'`{skill}/{name}/`')
        support_rows.append(f'| {skill} | {"；".join(navigation)} |')
        for _, mode, description, triggers in (r for r in rows if r[0] == skill):
            commands = command_map.get((skill, mode), [])
            slash = '、'.join(f'`/{n}`（{ars_path(p)}）' for n, p in commands) or '无；用技能名 + mode 请求'
            ars_rows.append(f'| {skill} | `{mode}` | {cell(description)}；{cell(triggers)} | '
                            f'{ars_path(path) if data else "UNAVAILABLE"} | {slash} |')

    digest = hashlib.sha256()
    for path, content in sorted(sources.items(), key=lambda item: logical(item[0])):
        digest.update(logical(path).encode() + b'\0' + content + b'\0')
    lines = ['# ARS + wfh 路由索引（生成文件）', '',
             '仅定位，不证明已读取、已加载、已验证或研究已执行。推荐前读取目标 SKILL 与模式要求的支持文件。', '',
             f'- 来源 ARS：`{ars_identity}`；运行时显式提供当前根，不保存安装路径。',
             f'- ARS 状态：{"LOCATED（宿主加载状态另查）" if available else "ARS_NOT_AVAILABLE"}',
             f'- 实际 ARS 模式记录：{len(rows)}；wfh 执行入口：{len(wfh)}（默认 1，高级 {max(0, len(wfh)-1)}）；可读入口：{sum("UNAVAILABLE" not in r for r in wfh_rows)}',
             f'- 来源指纹 SHA-256：`{digest.hexdigest()}`；输入文件：{len(sources)}',
             '- 刷新 / 只读检查：[路由协议](routing_protocol.md)；工具：[refresh_index.py](../scripts/refresh_index.py)',
             '', '## 诊断', '', *(diagnostics or ['OK：已按当前来源生成；每次咨询仍需 --check。']), '',
             f'## {len(wfh)} 个 wfh 执行入口（一个默认入口）', '', '| 名称 | slash | frontmatter 描述 | 路径 | 主要支持协议 |',
             '|---|---|---|---|---|', *wfh_rows, '', '## ARS 模式', '',
             '路径均相对上方 ARS 根；升级或迁移后重新 refresh，索引不把旧缓存路径当默认安装。',
             '下列 slash 只列当前 commands 文件中可核对的映射。无 slash 的行可用「请使用 academic-research-skills:<技能>，mode=<模式>，<请求>」。',
             '`(pipeline)` 是编排入口而非命名模式；`resume_from_passport=<hash>` 是恢复参数，使用前须读其 opt-in 协议。', '',
             '| Skill | mode / 入口 | 注册表产出与触发 | 路径 | 真实 slash 命令文件 |',
             '|---|---|---|---|---|', *ars_rows, '', '## 支持文件导航', '',
             '导航指向真实目录；具体 mode 所需文件从 SKILL 对应分支读取，目录存在不等于模式契约已核验。', '',
             '| Skill | 支持协议定位 |', '|---|---|', *support_rows, '',
             'wfh 支持协议见 [共享总览](../SKILL.md)。ARS 路由以当前根下 shared/references/routing_core.md 与 intent_clarification_protocol.md 为准。', '']
    return '\n'.join(lines), diagnostics


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ars-root', type=Path, help='Explicit verified plugin root (no cache guessing)')
    parser.add_argument('--skills-root', type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument('--output', type=Path)
    parser.add_argument('--check', action='store_true', help='Read-only comparison; exit 1 if stale')
    args = parser.parse_args()
    skills = args.skills_root.expanduser().resolve()
    ars = args.ars_root.expanduser().resolve() if args.ars_root else None
    output = (args.output or skills / 'wfh-research/references/skills_index.md').expanduser().resolve()
    content, diagnostics = build(skills, ars, output)
    for message in diagnostics:
        print(message, file=sys.stderr)
    previous = output.read_text() if output.is_file() else None
    if args.check:
        print('INDEX_CURRENT' if previous == content else 'INDEX_STALE: refresh required; no files written')
        return 2 if diagnostics else int(previous != content)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content)
    print(f'INDEX_REFRESHED: {output}')
    return 2 if diagnostics else 0


if __name__ == '__main__':
    sys.exit(main())
