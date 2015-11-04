#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_recursive_dict
----------------------------------

Tests for `recursive_dict` module.
"""

import unittest

from recursive_dict import recursive_dict, safe_recursive_dict


class TestRecursive_dict(unittest.TestCase):

    def setUp(self):
        self.sample_data = {
            'alpha': {
                'first': 1,
                'second': 2,
            },
            'many': [
                {'foo': {'test': True}},
                {'foo': {'test': False}},
            ],
            'deep': [
                {'deeper': {'a': 'b'}}
            ]
        }

    def tearDown(self):
        pass

    def test_rdict(self):
        my_dict = recursive_dict(self.sample_data)
        assert my_dict['alpha', 'second'] == 2
        assert [item['foo', 'test'] for item in my_dict['many']] \
            == [True, False]
        assert my_dict['deep', 0, 'deeper', 'a'] == 'b'
        self.assertRaises(KeyError, lambda: my_dict['alpha', 'third'])

    def test_safe_rdict(self):
        my_dict = safe_recursive_dict(self.sample_data)
        assert my_dict['alpha', 'third'] is None


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
