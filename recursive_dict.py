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
__version__ = '0.2.0'


class recursive_lookup(object):
    _original = None
    _raise_errors = True

    def make_recursive(self, item):
        if isinstance(item, list):
            item = recursive_list.from_list(item, self._raise_errors)
        elif isinstance(item, dict):
            item = recursive_dict.from_dict(item, self._raise_errors)
        return item

    def __getitem__(self, key):
        item = super(recursive_lookup, self)
        try:
            if isinstance(key, tuple):
                for arg in key:
                    item = item.__getitem__(arg)
            else:
                item = item.__getitem__(key)
            return self.make_recursive(item)

        except (KeyError, IndexError):
            if self._raise_errors:
                raise

    def __setitem__(self, key, value):
        item = super(recursive_lookup, self)
        try:
            if isinstance(key, tuple):
                args, key = key[:-1], key[-1]
                for arg in args:
                    item = item.__getitem__(arg)
            item.__setitem__(key, value)

            original = getattr(item, '_original', None)
            if original:
                original.__setitem__(key, value)

        except (KeyError, IndexError):
            if self._raise_errors:
                raise

    def __getattribute__(self, item):
        excluded = ('_original', '_raise_errors', '__getitem__', '__setitem__')
        if item not in excluded and self._original and hasattr(self._original, item):
            return getattr(self._original, item)
        else:
            return super(recursive_lookup, self).__getattribute__(item)


class recursive_dict(recursive_lookup, dict):
    @classmethod
    def from_dict(cls, original, raise_errors=True):
        new_dict = cls(**original)
        new_dict._original = original
        new_dict._raise_errors = raise_errors
        return new_dict


class safe_recursive_dict(recursive_dict):
    _raise_errors = False


class recursive_list(recursive_lookup, list):
    @classmethod
    def from_list(cls, original, raise_errors=True):
        new_list = cls(original)
        new_list._original = original
        new_list._raise_errors = raise_errors
        return new_list

    def __init__(self, seq=()):
        super(recursive_list, self).__init__(map(self.make_recursive, seq))


rdict = recursive_dict
safe_rdict = safe_recursive_dict
