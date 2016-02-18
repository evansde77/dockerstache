#!/usr/bin/env python
"""
tests for dotfile module
"""
import os
import json
import mock
import tempfile
import unittest

from dockerstache.dotfile import Dotfile


class DotfileTests(unittest.TestCase):
    """
    tests for Dotfile object
    """
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.defaults = os.path.join(self.tempdir, 'defaults.json')
        self.context = os.path.join(self.tempdir, 'context.json')
        self.dotfile = os.path.join(self.tempdir, '.dockerstache')

        with open(self.defaults, 'w') as handle:
            json.dump(
                {"defaults": {"value1": 1, "value2": 2}, "default_value": 99},
                handle
            )

        with open(self.context, 'w') as handle:
            json.dump(
                {
                    "defaults": {"value2": 100},
                    "context": {"value3": 3, "value4": 4}
                },
                handle
            )
        with open(self.dotfile, 'w') as handle:
            json.dump(
                {
                    "context": self.context,
                    "defaults": self.defaults
                },
                handle
            )
        self.opts = {}
        self.opts['input'] = self.tempdir
        self.opts['output'] = None
        self.opts['context'] = None
        self.opts['defaults'] = None

    def tearDown(self):
        """cleanup test data """
        if os.path.exists(self.tempdir):
            os.system("rm -rf {}".format(self.tempdir))

    def test_dotfile(self):
        """test mechnics of Dotfile load"""
        dotfile = Dotfile(self.opts)
        self.failUnless(dotfile.exists())
        self.assertEqual(dotfile.abs_input_dir(), self.tempdir)
        d = dotfile.env_dictionary()
        self.failUnless('DOCKERSTACHE_DEFAULTS' in d)
        self.failUnless('DOCKERSTACHE_POST_SCRIPT' in d)
        self.failUnless('DOCKERSTACHE_PRE_SCRIPT' in d)
        self.failUnless('DOCKERSTACHE_OUTPUT' in d)
        self.failUnless('DOCKERSTACHE_CONTEXT' in d)

        dotfile.load()
        d = dotfile.env_dictionary()
        self.assertEqual(d['DOCKERSTACHE_CONTEXT'], self.context)
        self.assertEqual(d['DOCKERSTACHE_DEFAULTS'], self.defaults)

    @mock.patch('dockerstache.dotfile.execute_command')
    def test_dotfile_context(self, mock_execute):
        """test pre and post execution, first with noop then a mock script"""
        dotfile = Dotfile(self.opts)
        with dotfile:
            dotfile.exists()
        self.assertEqual(mock_execute.call_count, 0)

        with open(self.dotfile, 'w') as handle:
            json.dump(
                {
                    "context": self.context,
                    "defaults": self.defaults,
                    "pre_script": "do_a_thing.sh",
                    "post_script": "done_a_thing.sh"
                },
                handle
            )
        dotfile = Dotfile(self.opts)
        with dotfile:
            dotfile.exists()
        self.assertEqual(mock_execute.call_count, 2)
        call_args = [x[0][1] for x in mock_execute.call_args_list]
        self.assertEqual(call_args, ['do_a_thing.sh', 'done_a_thing.sh'])

if __name__ == '__main__':
    unittest.main()
