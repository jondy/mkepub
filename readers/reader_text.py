#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re

PAT_TITLE = r'^(#+)(.*)\s*$'
COVER_SUFFIX = '-封面.jpg'


class TextReader:

    def __init__(self):
        self._filename = None
        self._pat_titles = [re.compile(PAT_TITLE)]

    def is_support(self, ext):
        return ext in ('.txt',)

    def get_template(self):
        return None

    def get_cover(self):
        cover = os.path.join(self._filename[:-4] + COVER_SUFFIX)
        return cover if os.path.exists(cover) else None

    def open(self, filename):
        self._filename = filename

    def close(self):
        self._filename = None

    def images(self):
        return []

    def stylesheets(self):
        return []

    def contents(self):
        if self._filename is None:
            return
        level = -1
        title = None
        paras = []
        with open(self._filename) as f:
            for line in f:
                if line.strip():
                    newtitle = self._is_title(line)
                    if newtitle is None:
                        raise Exception('不支持的文本格式')
                    level, title = newtitle
                    break

            # Empty file
            if title is None:
                return

            for line in f:
                newtitle = self._is_title(line)
                if newtitle:
                    if title:
                        yield (level, title, ''.join(paras))
                    level, title = newtitle
                    paras = []
                elif line.startswith('!#'):
                    pass
                else:
                    paras.append(line)
            yield (level, title, ''.join(paras))

    def _is_title(self, line):
        for pat in self._pat_titles:
            m = pat.match(line)
            if m:
                return len(m.group(1)) - 2, m.group(2)


def register_reader():
    return TextReader()


if __name__ == '__main__':
    r = TextReader()
    print(r._is_title('##Title2\n'))

    filename = '__test__.txt'
    with open(filename, 'w') as f:
        f.write('##Title\nPara1\n###Title3\nPara2')
    r.open('__test__.txt')
    print(list(r.contents()))
    r.close()
    os.remove(filename)
