#!/usr/bin/env python
"""
unittests for context module
"""
import os
import json
import tempfile
import unittest

from dockerstache.context import Context


class ContextTests(unittest.TestCase):
    """
    test cases for context class
    """
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.defaults = os.path.join(self.tempdir, 'defaults.json')
        self.context = os.path.join(self.tempdir, 'context.json')

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

    def tearDown(self):
        """cleanup test data """
        if os.path.exists(self.tempdir):
            os.system("rm -rf {}".format(self.tempdir))

    def test_default_load(self):
        """verify that load fails if no context"""
        ctx = Context()
        self.assertRaises(RuntimeError, ctx.load)

    def test_context_only_load(self):
        """test loading context file with no defaults"""
        ctx = Context(self.context)
        ctx.load()
        self.assertTrue('context' in ctx)
        self.assertTrue('defaults' in ctx)
        self.assertEqual(ctx['context']['value3'], 3)
        self.assertEqual(ctx['context']['value4'], 4)
        self.assertEqual(ctx['defaults']['value2'], 100)

    def test_context_default_load(self):
        """test default and context loading and override precedence"""
        ctx = Context(self.context, self.defaults)
        ctx.load()
        self.assertTrue('context' in ctx)
        self.assertTrue('defaults' in ctx)
        self.assertEqual(ctx['context']['value3'], 3)
        self.assertEqual(ctx['context']['value4'], 4)
        self.assertEqual(ctx['default_value'], 99)
        self.assertEqual(ctx['defaults']['value1'], 1)
        self.assertEqual(ctx['defaults']['value2'], 100)

if __name__ == '__main__':
    unittest.main()
