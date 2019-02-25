import os
from importlib import import_module

_readers = []


def find_reader(filename):
    ext = os.path.splitext(filename)[1].lower()
    for r in _readers:
        if r.is_support(ext):
            return r


def search_readers(path=None):
    if path is None:
        path = os.path.dirname(__file__)
    for filename in os.listdir(path):
        if filename.startswith('reader_'):
            m = import_module('readers.%s' % os.path.splitext(filename)[0])
            if hasattr(m, 'register_reader'):
                _readers.append(m.register_reader())


search_readers()
