#!/usr/bin/env python3
"""Regression checks for evaluation tooling, without model calls or real research."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).with_name('check_outputs.py').resolve()
spec = importlib.util.spec_from_file_location('check_outputs_under_test', SCRIPT)
outputs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(outputs)


class OutputChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='wfh-eval-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def reply(self, ident, text='已核对现有材料，尚未执行研究。', root=None):
        path = (root or self.root) / f'eval-{ident:02}' / 'with_skill/outputs/response.md'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')
        return path

    def manifest(self, ids):
        path = self.root / 'evals.json'
        path.write_text(json.dumps({'evals': [{'id': ident} for ident in ids]}),
                        encoding='utf-8')
        return path

    def test_discovers_every_saved_case_including_eleventh(self):
        for ident in range(1, 12):
            self.reply(ident, 'frontier' if ident == 11 else '已核对材料。')
        rows = outputs.check(self.root)
        self.assertEqual(len(rows), 11)
        self.assertFalse(rows[-1]['lexical_passed'])
        self.assertEqual(rows[-1]['eval_id'], 11)

    def test_manifest_keeps_missing_replies_visible(self):
        self.manifest([1, 11])
        self.reply(1)
        rows = outputs.check(self.root)
        self.assertEqual([r['eval_id'] for r in rows], [1, 11])
        self.assertTrue(rows[-1]['missing_reply'])

    def test_explicit_cases_can_live_outside_results(self):
        cases = self.manifest([2, 12])
        results = self.root / 'results'
        self.reply(2, root=results)
        rows = outputs.check(results, cases=cases)
        self.assertEqual([r['eval_id'] for r in rows], [2, 12])
        self.assertFalse(rows[-1]['reply_exists'])

    def test_extra_case_not_hidden_by_manifest(self):
        self.manifest([1])
        self.reply(1)
        self.reply(11, 'INDEX_INVALID')
        rows = outputs.check(self.root)
        self.assertEqual([r['eval_id'] for r in rows], [1, 11])
        self.assertFalse(rows[-1]['lexical_passed'])

    def test_partial_overrides_keep_other_original_results(self):
        self.manifest([1, 2])
        self.reply(1, 'frontier')
        self.reply(2, 'INDEX_INVALID')
        overrides = self.root / 'rerun'
        self.reply(1, root=overrides)
        rows = outputs.check(self.root, overrides)
        self.assertTrue(rows[0]['lexical_passed'])
        self.assertFalse(rows[1]['lexical_passed'])

    def test_no_cases_is_an_error(self):
        with self.assertRaisesRegex(ValueError, 'No evaluation cases'):
            outputs.check(self.root)

    def test_duplicate_ids_are_rejected(self):
        self.manifest([1, 1])
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            outputs.check(self.root)

    def test_cli_success_depends_on_actual_case_count(self):
        self.manifest([1, 2])
        self.reply(1)
        self.reply(2)
        report = self.root / 'report.json'
        result = subprocess.run([sys.executable, '-I', str(SCRIPT), '--results',
                                 str(self.root), '--output', str(report)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(report.read_text(encoding='utf-8'))
        self.assertEqual(data['checked'], 2)
        self.assertEqual(data['passed'], 2)
        self.assertNotIn('real saved', data['scope'])

    def test_paths_still_require_chinese_explanation(self):
        self.reply(1, 'BRIEF.md\n')
        row = outputs.check(self.root)[0]
        self.assertFalse(row['lexical_passed'])
        self.assertIn('BRIEF.md', row['files_without_chinese_explanation'])
        self.reply(1, 'BRIEF.md（研究方案）\n')
        self.assertTrue(outputs.check(self.root)[0]['lexical_passed'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
