#!/usr/bin/env python
"""
templates tests
"""
import os
import json
import unittest
import tempfile
import dockerstache.templates as templ


class TemplatesTests(unittest.TestCase):
    """
    test coverage for templates module
    """
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.target_dir = tempfile.mkdtemp()
        self.subdirs1 = os.path.join(self.tempdir, 'dir1', 'dir2', 'dir3')
        self.subdirs2 = os.path.join(self.tempdir, 'dir1', 'dir4', 'dir5')
        os.makedirs(self.subdirs1)
        os.makedirs(self.subdirs2)

        self.template1 = os.path.join(
            self.tempdir, 'dir1', 'dir2', 'template1.json.mustache'
        )
        self.template2 = os.path.join(
            self.tempdir, 'dir1', 'dir4', 'dir5', 'template2.json.mustache'
        )
        with open(self.template1, 'w') as handle:
            json.dump({
                'template': 1,
                'value': '{{user}}'
                }, handle)
        with open(self.template2, 'w') as handle:
            json.dump({
                'template': 2,
                'value': '{{group}}'
                }, handle)

    def tearDown(self):
        """cleanup test data """
        if os.path.exists(self.tempdir):
            os.system("rm -rf {}".format(self.tempdir))
        if os.path.exists(self.target_dir):
            os.system("rm -rf {}".format(self.target_dir))

    def test_replicate_directory_tree(self):
        """test replication of dir structure"""
        templ.replicate_directory_tree(self.tempdir, self.target_dir)
        expected_path1 = os.path.join(self.target_dir, 'dir1', 'dir2', 'dir3')
        expected_path2 = os.path.join(self.target_dir, 'dir1', 'dir4', 'dir5')
        self.failUnless(os.path.exists(expected_path1))
        self.failUnless(os.path.exists(expected_path2))

    def test_find_templates(self):
        """test find template function"""
        templates_found = templ.find_templates(self.tempdir)
        self.assertEqual(len(templates_found), 2)
        self.failUnless(self.template1 in templates_found)
        self.failUnless(self.template2 in templates_found)

    def test_render_template(self):
        """test render template call"""
        file_out = os.path.join(self.target_dir, 'template1.json')
        context = {'user': 'steve', 'group': 'vanhalen'}
        templ.render_template(self.template1, file_out, context)
        self.failUnless(os.path.exists(file_out))
        with open(file_out, 'r') as handle:
            data = json.load(handle)

        self.failUnless('template' in data)
        self.failUnless('value' in data)
        self.assertEqual(data['template'], 1)
        self.assertEqual(data['value'], context['user'])

    def test_process_templates(self):
        """test end to end process templates call"""

        context = {'user': 'steve', 'group': 'vanhalen'}
        templ.process_templates(self.tempdir, self.target_dir, context)
        expected_path1 = os.path.join(self.target_dir, 'dir1', 'dir2', 'dir3')
        expected_path2 = os.path.join(self.target_dir, 'dir1', 'dir4', 'dir5')
        self.failUnless(os.path.exists(expected_path1))
        self.failUnless(os.path.exists(expected_path2))

        expected_file1 = os.path.join(
            self.target_dir, 'dir1', 'dir2', 'template1.json'
        )
        expected_file2 = os.path.join(
            self.target_dir, 'dir1', 'dir4', 'dir5', 'template2.json'
        )

        self.failUnless(os.path.exists(expected_file1))
        self.failUnless(os.path.exists(expected_file2))

        with open(expected_file1, 'r') as handle:
            data1 = json.load(handle)
        with open(expected_file2, 'r') as handle:
            data2 = json.load(handle)

        self.failUnless('template' in data1)
        self.failUnless('value' in data1)
        self.assertEqual(data1['template'], 1)
        self.assertEqual(data1['value'], context['user'])
        self.failUnless('template' in data2)
        self.failUnless('value' in data2)
        self.assertEqual(data2['template'], 2)
        self.assertEqual(data2['value'], context['group'])

if __name__ == '__main__':
    unittest.main()
