#!/usr/bin/env python3
"""Offline checks of published wfh documents; not an ARS or model-behavior test."""
import argparse
import json
from pathlib import Path
import re
import unittest
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]


class ContractChecks(unittest.TestCase):
    def text(self, relative):
        return (ROOT / relative).read_text(encoding='utf-8')

    def ref(self, name):
        return self.text('wfh-research/references/' + name + '.md')

    def test_manifest_inventory_and_version(self):
        plugin = json.loads(self.text('.claude-plugin/plugin.json'))
        market = json.loads(self.text('.claude-plugin/marketplace.json'))
        entries = [p for p in market['plugins'] if p['name'] == plugin['name']]
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]['skills'], plugin['skills'])
        self.assertEqual(entries[0]['version'], plugin['version'])
        self.assertEqual(set(plugin['skills']), {
            './' + p.parent.name for p in ROOT.glob('wfh*/SKILL.md')})
        self.assertEqual(len(plugin['skills']), 9)

    def test_invocation_boundaries(self):
        for path in ROOT.glob('wfh*/SKILL.md'):
            text = path.read_text(encoding='utf-8')
            header = re.match(r'\A---\n(.*?)\n---', text, re.S)
            self.assertIsNotNone(header, str(path))
            self.assertRegex(header[1], rf'(?m)^name: {re.escape(path.parent.name)}$')
            disabled = bool(re.search(r'^disable-model-invocation: true$', header[1], re.M))
            self.assertEqual(disabled, path.parent.name != 'wfh', str(path))
            if path.parent.name == 'wfh-research':
                self.assertRegex(header[1], r'(?m)^user-invocable: false$')
            else:
                self.assertNotRegex(header[1], r'(?m)^user-invocable: false$')

    def test_live_relative_links_and_fences(self):
        paths = list(ROOT.glob('wfh*/SKILL.md'))
        paths += list((ROOT / 'wfh-research/references').glob('*.md'))
        paths += [ROOT / name for name in ('README.md', 'MIGRATION.md', 'GLOSSARY.md', 'docs/ARS-INTEGRATION.md')]
        for path in paths:
            text = path.read_text(encoding='utf-8')
            self.assertEqual(len(re.findall(r'^```', text, re.M)) % 2, 0, str(path))
            # Sample artifact paths in fenced templates are not package references.
            prose = re.sub(r'^```[^\n]*\n.*?^```[^\n]*$', '', text, flags=re.M | re.S)
            for target in re.findall(r'\[[^\]\n]+\]\(([^)\n]+)\)', prose):
                target = unquote(target.strip().strip('<>')).split('#', 1)[0]
                if not target or re.match(r'^[a-zA-Z][\w+.-]*:', target):
                    continue
                self.assertTrue((path.parent / target).is_file(), f'{path.relative_to(ROOT)} -> {target}')

    def test_advice_and_confirmation_are_separate(self):
        policy = self.ref('decision_classes')
        self.assertIn('实质性', policy)
        self.assertIn('候选与推荐', policy)
        self.assertIn('研究者确认', policy)
        self.assertIn('作者接受建议不等于证据成立', policy)
        for name in ('decision_classes', 'grilling_protocol', 'grilling_tree', 'user_output_protocol'):
            text = self.ref(name)
            for stale in ('❌ 不给建议', '⛔ 这一题没有建议', '即使用户坚持，也不替用户选', '不建议接受或拒绝'):
                self.assertNotIn(stale, text, name)

    def test_mode_contract_has_one_authority(self):
        handoff = self.ref('ars_handoff_protocol')
        self.assertIn('输入要求属于所选模式', handoff)
        self.assertIn('原文为唯一来源', handoff)
        self.assertIn('intake_pending', handoff)
        for name in ('ars_handoff_protocol', 'spec_template', 'spec_examples'):
            text = self.ref(name)
            self.assertNotRegex(text, r'(?:平均\s*[≥>]\s*3\.0|最低\s*[≥>]\s*2|average\s*>=\s*3\.0)')
        self.assertIn('实际由 ARS 生成', handoff)
        self.assertIn('ars-internal', handoff)

    def test_native_socratic_boundary_is_preserved(self):
        for name in ('ars_handoff_protocol', 'grilling_protocol'):
            text = self.ref(name)
            self.assertIn('[SOCRATIC-NON-GENERATION-EXIT: explicit_user_request]', text)
            self.assertRegex(text, r'非生成|non-generation')

    def test_standalone_and_authorized_goal_paths(self):
        dispatch = self.ref('dispatch_protocol')
        execution = self.ref('execution_protocol')
        self.assertIn('不先要求创建课题', dispatch)
        self.assertIn('独立请求', execution)
        self.assertIn('若同一已授权目标需要后续任务', execution)
        self.assertIn('没有清楚目标的“继续”只恢复当前任务', execution)
        self.assertIn('原生必需确认', execution)
        self.assertIn('高级手动入口仍停在指定任务', execution)

    def test_grill_has_no_spec_loading_dependency(self):
        # A manual discussion entry must not acquire a dependency on the
        # separate spec implementation through either entry or shared protocol.
        for relative in ('wfh-grill/SKILL.md',
                         'wfh-research/references/grilling_protocol.md'):
            text = self.text(relative)
            targets = re.findall(r'\[[^\]\n]+\]\(([^)\n]+)\)', text)
            self.assertFalse(any(t.endswith('wfh-spec/SKILL.md') for t in targets), relative)
        intro = self.ref('grilling_protocol').split('## 0.', 1)[1].split('### 0.1', 1)[0]
        self.assertNotRegex(intro, r'(?m)^\| `BRIEF\.md` \|')
        self.assertIn('../wfh-spec/SKILL.md', self.text('wfh/SKILL.md'))

    def test_default_spec_requires_explicit_generation_request(self):
        dispatch = self.ref('dispatch_protocol')
        self.assertIn('### 3.1 方案整理的触发与入口边界', dispatch)
        self.assertIn('默认入口有明确生成请求', dispatch)
        self.assertIn('默认入口只有讨论或确认', dispatch)
        self.assertIn('直接使用高级入口', dispatch)
        for name in ('grilling_protocol', 'flow_details', 'dispatch_protocol',
                     'execution_protocol', 'user_output_protocol'):
            self.assertNotIn('默认入口和单独设计入口共用该规则', self.ref(name), name)
            self.assertNotIn('确认后直接整理并链接“研究方案”', self.ref(name), name)

    def test_each_task_gets_fresh_execution_context(self):
        execution = self.ref('execution_protocol')
        self.assertIn('一任务一上下文', execution)
        self.assertIn('只传指针，不传正文', execution)
        self.assertIn('执行子代理与验收子代理必须是不同上下文', execution)
        self.assertIn('不改任务状态、FLOW', execution)
        self.assertNotIn('输入可容纳时在当前会话完成目标', execution)
        task = self.ref('tickets_template')
        self.assertIn('每条任务一个全新的执行上下文', task)
        self.assertIn('不复用执行子代理', task)
        for name in ('wfh', 'wfh-implement-spec', 'wfh-next', 'wfh-close', 'wfh-tickets'):
            self.assertIn('子代理', self.text(name + '/SKILL.md'), name)

    def test_all_execution_paths_check_existing_work_before_launch(self):
        execution = self.ref('execution_protocol')
        gate = execution.split('### 3.1 所有执行方式共用的启动前恢复检查', 1)[1]
        gate = gate.split('### 3.2', 1)[0]
        self.assertIn('默认子代理、独立会话和当前会话', gate)
        self.assertIn('pending.json', gate)
        self.assertIn('任务与 FLOW 都是 todo', gate)
        self.assertIn('任务为 doing 或存在启动证据时', gate)
        self.assertIn('starting / waiting', gate)
        self.assertIn('宿主不可查、标识缺失或结果仍未知则停止生产', gate)
        self.assertIn('先按状态协议 §6 验收或补未完成的同步', gate)
        self.assertIn('确认旧执行已结束且无写入者', gate)
        default = execution.split('## 默认入口分支', 1)[1].split('## 4.', 1)[0]
        self.assertLess(default.index('先通过 §3.1'), default.index('交给新的执行子代理'))
        self.assertIn('恢复先通过 §3.1', execution)
        self.assertNotIn('独立会话启动时，每次真实启动前先读 pending', execution)
        for name in ('wfh', 'wfh-implement-spec'):
            self.assertIn('§3.1', self.text(name + '/SKILL.md'))
        self.assertIn('已有等待记录与实际执行状态', self.ref('state_protocol'))

    def test_handoff_carries_current_authorization_and_read_limits(self):
        state = self.ref('state_protocol')
        template = state.split('任务：<ID / 标题>', 1)[1].split('```', 1)[0]
        for field in ('本次已授权目标：', '当前限制与授权来源：', '执行边界：'):
            self.assertIn(field, template)
        self.assertIn('本轮授权允许读取的声明输入', template)
        self.assertIn('仅准备时写尚未授权执行', template)
        for text in (state, self.ref('execution_protocol')):
            self.assertIn('执行范围取本次授权与任务范围的交集', text)
            self.assertIn('完成子集不能', text)
        self.assertIn('授权排除的输入不读取', state)
        self.assertIn('先交步骤规划拆分', state)

    def test_standalone_close_reconciles_only_matching_pending(self):
        state = self.ref('state_protocol')
        close = state.split('## 6. close：', 1)[1]
        self.assertIn('task_id、task_file 及工作区', close)
        self.assertIn('是否结束无法确认时，只读复核', close)
        self.assertIn('仅在目标任务和 FLOW 同步成功且一致后', close)
        self.assertIn('partial / blocked 保持未关闭', close)
        self.assertIn('身份或内容自核对后变化', close)
        self.assertIn('恢复只补未完成的收尾', close)
        self.assertIn('不改其他任务的记录', close)
        self.assertIn('按 §6 第9项收尾', self.text('wfh-close/SKILL.md'))
        self.assertIn('状态协议 §6 第1、9项', self.ref('execution_protocol'))

    def test_state_writer_is_unambiguous(self):
        task = self.ref('tickets_template')
        execution = self.ref('execution_protocol')
        self.assertNotIn('状态只由执行会话或', task)
        self.assertIn('执行会话只写声明产出与执行证据', task)
        self.assertIn('不改任务状态、FLOW', execution)
        self.assertIn('发起方', self.ref('state_protocol'))

    def test_types_and_ids_do_not_imply_scientific_content(self):
        task = self.ref('tickets_template')
        spec = self.ref('spec_template')
        self.assertNotIn('T01 必须是 `claim`', task)
        self.assertNotIn('`claim` 六层齐全', task)
        self.assertIn('不适用理由', task)
        self.assertIn('反例', task)
        self.assertIn('可信度', task)
        self.assertIn('decision_key', spec)
        self.assertNotIn('四项都写「不适用（非材料学课题）」', spec)
        self.assertIn('交付完成与主张支持程度分开', self.ref('state_protocol'))

    def test_delivery_checks_reuse_native_evidence(self):
        check = self.ref('integrity_selfcheck')
        self.assertIn('实际产物和报告', check)
        self.assertIn('版本', check)
        self.assertIn('not-applicable', check)
        self.assertIn('未执行', check)
        self.assertIn('必需检查缺失', check)
        for name in ('integrity_selfcheck', 'state_protocol', 'tickets_template', 'tickets_types', 'flow_template'):
            self.assertNotRegex(self.ref(name), r'(?:七项全部 pass|整稿自检 7 项通过)', name)

    def test_eval_cases_cover_positive_and_negative_boundaries(self):
        data = json.loads(self.text('wfh-research/evals/evals.json'))
        self.assertEqual(data['evaluation_kind'], 'protocol-dry-run-with-mocked-ARS')
        self.assertEqual(len({case['id'] for case in data['evals']}), len(data['evals']))
        self.assertGreaterEqual(len(data['evals']), 4)
        self.assertTrue({
            'explicit-default-spec-versus-standalone-grill',
            'default-discussion-confirmation-only',
            'standalone-grill-preserves-existing-brief',
            'standalone-preparation-without-workspace',
            'blocked-recovery-and-next-step-purpose',
            'cancelled-step-review-and-scope-completion',
            'negative-result-with-persistent-reopen-stop',
            'single-pending-record-and-start-sync',
            'explicit-drafts-preserve-confirmation-boundaries',
            'mixed-branches-have-unambiguous-question-ids',
            'todo-dag-and-dependency-proof-inputs',
            'conditional-revision-and-optional-terms',
            'unknown-installation-is-not-proven-absence',
            'standalone-close-reconciles-matching-pending',
            'narrowed-authorization-survives-task-handoff',
            'bare-continue-does-not-authorize-sibling-tasks',
            'default-resume-checks-existing-execution-before-launch',
        }.issubset({case['name'] for case in data['evals']}))
        isolation = next(case for case in data['evals']
                         if case['name'] == 'one-task-one-fresh-execution-context')
        self.assertIn('本轮明确授权', isolation['prompt'])
        for case in data['evals']:
            self.assertTrue(case['prompt'])
            self.assertGreaterEqual(len(case['assertions']), 3)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    ROOT = args.root.resolve()
    unittest.main(argv=['check_contracts'], verbosity=2)
