# -*- coding: utf-8 -*-
"""A dict subclass that can lookup several layers deep.

>>> my_dict = recursive_dict(**{
...     'alpha': {
...         'first': 1,
...         'second': 2,
...     },
...     'many': [
...         {'foo': {'test': True}},
...         {'foo': {'test': False}},
...     ]
... })
>>> my_dict['alpha', 'second']
2
>>> [item['foo', 'test'] for item in my_dict['many']]
[True, False]
"""

__author__ = 'Ryan Anguiano'
__email__ = 'ryan.anguiano@gmail.com'
__version__ = '0.1.0'


class recursive_dict(dict):
    raise_errors = True

    def make_recursive(self, item):
        if isinstance(item, list):
            item = map(self.make_recursive, item)
        elif isinstance(item, dict):
            item = recursive_dict(**item)
        return item

    def __getitem__(self, key):
        item = super(recursive_dict, self)
        try:
            if isinstance(key, tuple):
                for arg in key:
                    item = item.__getitem__(arg)
            else:
                item = item.__getitem__(key)
            return self.make_recursive(item)
        except (KeyError, IndexError):
            if self.raise_errors:
                raise


class safe_recursive_dict(recursive_dict):
    raise_errors = False


rdict = recursive_dict
safe_rdict = safe_recursive_dict
