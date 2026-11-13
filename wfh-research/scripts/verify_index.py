#!/usr/bin/env python3
"""Exercise relocation, inventory failures and read-only checks; stdlib only."""
import argparse
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).with_name('refresh_index.py').resolve()
SUITE = SCRIPT.parents[2]
spec = importlib.util.spec_from_file_location('refresh_index_under_test', SCRIPT)
index = importlib.util.module_from_spec(spec)
spec.loader.exec_module(index)


def copy_suite(destination):
    shutil.copytree(SUITE / '.claude-plugin', destination / '.claude-plugin')
    for path in SUITE.glob('wfh*'):
        if (path / 'SKILL.md').is_file():
            shutil.copytree(path, destination / path.name, ignore=shutil.ignore_patterns('__pycache__'))


def copy_ars(source, destination):
    # Read documents as data; never import or run anything from the ARS root.
    for path in source.rglob('*.md'):
        if path.parts[len(source.parts)] in ('shared', 'commands', 'deep-research', 'academic-paper', 'academic-paper-reviewer', 'academic-pipeline', 'sr-screener') or path.name == 'MODE_REGISTRY.md':
            target = destination / path.relative_to(source)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)
    target = destination / '.claude-plugin/plugin.json'
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source / '.claude-plugin/plugin.json', target)


class NavigationChecks(unittest.TestCase):
    ars_root = None

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='wfh-index-')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.suite = self.base / 'suite'
        copy_suite(self.suite)
        self.output = self.suite / 'wfh-research/references/skills_index.md'

    def build(self, suite=None, ars=None):
        suite = suite or self.suite
        return index.build(suite, self.ars_root if ars is None else ars,
                           suite / 'wfh-research/references/skills_index.md')

    def test_ars_relocation_including_nested_root(self):
        before, problems = self.build()
        self.assertFalse(problems)
        moved = self.suite / 'audit-copy'
        copy_ars(self.ars_root, moved)
        after, problems = self.build(ars=moved)
        self.assertFalse(problems)
        self.assertEqual(before, after)
        self.assertNotIn(str(self.ars_root), after)
        self.assertNotIn(str(self.suite), after)

    def test_suite_relocation(self):
        before, problems = index.build(SUITE, self.ars_root,
                                      SUITE / 'wfh-research/references/skills_index.md')
        after, other = self.build()
        self.assertFalse(problems + other)
        self.assertEqual(before, after)

    def test_changed_contract_invalidates_digest(self):
        before, problems = self.build()
        self.assertFalse(problems)
        path = self.suite / 'wfh-research/references/state_protocol.md'
        path.write_text(path.read_text() + '\n新增有效约束。\n')
        after, problems = self.build()
        self.assertFalse(problems)
        self.assertNotEqual(before, after)

    def test_manifest_mismatch_refuses(self):
        path = self.suite / '.claude-plugin/marketplace.json'
        data = json.loads(path.read_text())
        data['plugins'][0]['skills'].pop()
        path.write_text(json.dumps(data))
        self.assertTrue(any('lists differ' in p for p in self.build()[1]))

    def test_unlisted_directory_refuses(self):
        path = self.suite / 'wfh-unlisted'
        path.mkdir()
        (path / 'SKILL.md').write_text('---\nname: wfh-unlisted\ndescription: test\n---\n')
        self.assertTrue(any('directories differ' in p for p in self.build()[1]))

    def test_missing_ars_reports_without_crash(self):
        content, problems = self.build(ars=self.base / 'not-installed')
        self.assertTrue(any('ARS_NOT_AVAILABLE' in p for p in problems))
        self.assertIn('wfh | /wfh', content)
        self.assertNotIn(str(self.base), content)

    def test_readonly_check_does_not_create_missing_output(self):
        output = self.base / 'absent.md'
        result = subprocess.run([sys.executable, '-I', str(SCRIPT), '--skills-root',
                                 str(self.suite), '--ars-root', str(self.ars_root),
                                 '--output', str(output), '--check'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertFalse(output.exists())

    def test_default_entry_must_allow_model_invocation(self):
        path = self.suite / 'wfh/SKILL.md'
        path.write_text(path.read_text().replace('name: wfh\n', 'name: wfh\ndisable-model-invocation: true\n', 1))
        self.assertTrue(any('invocation role' in p for p in self.build()[1]))

    def test_shared_package_is_not_a_user_entry(self):
        path = self.suite / 'wfh-research/SKILL.md'
        path.write_text(path.read_text().replace('user-invocable: false', 'user-invocable: true'))
        self.assertTrue(any('not be user-invocable' in p for p in self.build()[1]))

    def test_duplicate_registry_rows_rejected(self):
        registry = '## demo (2 modes)\n| Mode | Spectrum | Output | Oversight | Triggers |\n|---|---|---|---|---|\n| `full` | x | y | z | a |\n| `full` | x | y | z | a |\n'
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            index.registry_rows(registry)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ars-root', required=True, type=Path)
    args = parser.parse_args()
    NavigationChecks.ars_root = args.ars_root.expanduser().resolve()
    if not (NavigationChecks.ars_root / 'MODE_REGISTRY.md').is_file():
        parser.error('provide an existing ARS document root')
    unittest.main(argv=[sys.argv[0]], verbosity=2)
