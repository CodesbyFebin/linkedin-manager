"""Offline regressions for approval, duplicate writes, and install integrity."""
import contextlib
import io
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import requests
import yaml

ROOT = Path(__file__).resolve().parents[1]


def script(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / f'{name}.py')
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class SchedulingApproval(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tool = script('schedule_post')

    def run_schedule(self, *flags, answer=None):
        with tempfile.TemporaryDirectory() as directory:
            draft = Path(directory) / 'draft.txt'
            draft.write_text('The audit passed. The signed evidence is ready for review.')
            argv = ['schedule_post.py', '--file', str(draft), *flags]
            with mock.patch.object(sys, 'argv', argv), mock.patch('lib.active_backend', return_value='publora'), \
                 mock.patch('lib.publish', return_value={'postGroupId': 'test-id'}) as publish, \
                 mock.patch('builtins.input', side_effect=EOFError if answer is None else [answer]), \
                 mock.patch.object(self.tool, 'LOG_PATH', Path(directory) / 'log.jsonl'), contextlib.redirect_stdout(io.StringIO()):
                code = self.tool.main()
                return code, publish.call_count

    def test_unattended_schedule_requires_approval(self):
        self.assertEqual(self.run_schedule(), (2, 0))

    def test_declined_schedule_does_not_publish(self):
        self.assertEqual(self.run_schedule(answer='no'), (0, 0))

    def test_explicit_confirmation_sends_once(self):
        self.assertEqual(self.run_schedule(answer='yes'), (0, 1))

    def test_prior_approval_flag_sends_once(self):
        self.assertEqual(self.run_schedule('--approved'), (0, 1))

    def test_dry_run_never_publishes(self):
        self.assertEqual(self.run_schedule('--dry-run'), (0, 0))

    def test_invalid_timezone_fails_before_publish(self):
        with self.assertRaises(SystemExit) as error:
            self.run_schedule('--timezone', 'invalid/timezone')
        self.assertEqual(error.exception.code, 2)

    def test_slot_rules(self):
        self.assertEqual(self.tool.selftest(), 0)


class NonIdempotentWrites(unittest.TestCase):
    def test_timeout_is_not_replayed(self):
        from lib.publora_client import PubloraClient
        client = PubloraClient(api_key='test-placeholder')
        client._session.post = mock.Mock(side_effect=requests.Timeout('unknown outcome'))
        with self.assertRaises(requests.Timeout):
            client.create_post(content='approved text', platforms=['linkedin-test'])
        self.assertEqual(client._session.post.call_count, 1)

    def test_server_error_is_not_replayed(self):
        from lib.publora_client import PubloraClient, PubloraError
        client = PubloraClient(api_key='test-placeholder')
        response = mock.Mock(status_code=503)
        response.json.return_value = {'error': 'service unavailable'}
        client._session.post = mock.Mock(return_value=response)
        with self.assertRaises(PubloraError):
            client.create_comment(post_urn='urn:li:activity:123', message='approved', platform_id='linkedin-test')
        self.assertEqual(client._session.post.call_count, 1)


class DraftCredentialDetection(unittest.TestCase):
    def test_security_vocabulary_is_not_a_credential(self):
        gate = script('approval_gate')
        self.assertIsNone(gate.SECRET.search('The token expires after the API key is revoked. Keep the password private.'))

    def test_assignment_and_token_prefix_are_detected(self):
        gate = script('approval_gate')
        for text in ['api_key=example123456', 'password: example123456', 'ghp_example123456']:
            with self.subTest(text=text):
                self.assertIsNotNone(gate.SECRET.search(text))


class PackageIntegrity(unittest.TestCase):
    def test_every_claude_link_resolves_to_canonical_skill(self):
        for path in (ROOT / 'skills').glob('*/SKILL.md'):
            mirror = ROOT / '.claude/skills' / path.parent.name
            self.assertTrue(mirror.is_symlink())
            self.assertEqual(mirror.resolve(), path.parent.resolve())

    def test_manifests_and_citation_agree(self):
        codex = json.loads((ROOT / '.codex-plugin/plugin.json').read_text())
        claude = json.loads((ROOT / '.claude-plugin/plugin.json').read_text())
        marketplace = json.loads((ROOT / '.claude-plugin/marketplace.json').read_text())['plugins'][0]
        for item in (claude, marketplace):
            for key in ('name', 'version', 'description', 'author', 'license', 'homepage'):
                self.assertEqual(codex[key], item[key], key)
        citation = yaml.safe_load((ROOT / 'CITATION.cff').read_text())
        self.assertEqual(citation['version'], codex['version'])
        self.assertEqual(citation['license'], codex['license'])

    def test_sync_refuses_filled_tracked_templates(self):
        sync = script('sync_codex_marketplace')
        blob = mock.Mock(returncode=0, stdout='filled: yes\nprivate material')
        with tempfile.TemporaryDirectory() as directory, mock.patch.object(sync.subprocess, 'run', return_value=blob):
            with self.assertRaises(RuntimeError):
                sync.restore_templates(Path(directory))
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_catalog_round_trips_quoted_descriptions(self):
        catalog = json.loads((ROOT / 'skills.json').read_text())
        self.assertEqual(catalog['skill_count'], 40)
        for skill in catalog['skills']:
            data = yaml.safe_load((ROOT / skill['path']).read_text().split('---', 2)[1])
            self.assertEqual(skill['description'], data['description'])
            self.assertIn(f"[{skill['name']}]({skill['path']})", (ROOT / 'SKILLS.md').read_text())

    def test_generated_catalog_is_current(self):
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/build_catalog.py'), '--check'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_selftest_offline_never_runs_remote_schema_check(self):
        tool = script('selftest')
        calls = []
        def run(argv, **kwargs):
            calls.append(argv)
            return mock.Mock(returncode=0, stdout='OK', stderr='Ran 1 tests\nOK')
        with mock.patch.object(tool.subprocess, 'run', side_effect=run):
            tool.phase_tests(ROOT, offline=True)
        self.assertFalse(any('check_actor_inputs.py' in ' '.join(args) for args in calls))


if __name__ == '__main__':
    unittest.main()
