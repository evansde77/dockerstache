#!/usr/bin/env python
"""
dockerstache module test coverage for API calls

"""
import os
import tempfile
import json
import unittest
import mock

from dockerstache.dockerstache import run


class RunAPITests(unittest.TestCase):
    """tests for run API call"""
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

    @mock.patch('dockerstache.dockerstache.process_templates')
    def test_run(self, mock_process):
        """test run method"""
        run(**self.opts)
        self.failUnless(mock_process.called)

    @mock.patch('dockerstache.dockerstache.process_templates')
    def test_run_extend_context(self, mock_process):
        """test run method with extras for context"""
        extend = {'extensions': {'extras': 'values'}}
        self.opts['extend_context'] = extend
        run(**self.opts)
        self.failUnless(mock_process.called)
        context = mock_process.call_args[0][2]
        self.failUnless('extensions' in context)


if __name__ == '__main__':
    unittest.main()
