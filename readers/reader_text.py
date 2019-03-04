#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import chardet
import os
import re

from ebooklib import epub

PAT_TITLE = r'^(#+)\s*(.*)\s*$'
PAT_EMPTY = r'<p>\s*</p>'
PAT_COMMENT = '!#'

COVER_SUFFIX = '-封面.jpg'

MAX_META_ROW = 100
PAT_METADATAS = {
    'title': ('书名:', '书名：'),
    'author': ('作者:', '作者：'),
    'publisher': ('出版者:', '出版者：'),
    'date': ('出版时间:', '出版时间：'),
    'ISBN': ('ISBN:', 'ISBN：'),
}


class TextReader:

    def __init__(self):
        self._filename = None
        self._toc = None
        self._encoding = None
        self._pat_titles = [re.compile(PAT_TITLE)]
        self._pat_empty = re.compile(PAT_EMPTY)

    def is_support(self, ext):
        return ext in ('.txt',)

    def _iter_lines(self):
        if self._filename is None:
            return
        with open(self._filename, encoding=self._encoding,
                  errors='ignore') as f:
            yield from f

    def get_cover(self):
        cover = os.path.join(self._filename[:-4] + COVER_SUFFIX)
        return cover if os.path.exists(cover) else None

    def open(self, filename):
        self._filename = filename
        with open(self._filename, 'rb') as f:
            buf = f.read()
            charinfo = chardet.detect(buf)
        self._encoding = charinfo['encoding']

    def close(self):
        self._filename = None
        self._toc = None

    def get_metadata(self):
        row = 0
        meta = {}
        for line in self._iter_lines():
            for k, pats in PAT_METADATAS.items():
                if meta.get(k):
                    continue
                for s in pats:
                    if line.startswith(s):
                        meta[k] = line[len(s):].strip()
                        break
            row += 1
            if row > MAX_META_ROW:
                break
        return meta

    def get_toc(self):
        return self._toc

    def contents(self):
        self._pindex = 0
        self._row = 0
        self._toc = []

        paras = None
        titles = []

        def write_page():
            self._pindex += 1
            file_name = 'Text/chapter%02d.xhtml' % self._pindex
            level, title = self._toc.pop()
            page = epub.EpubHtml(title=title, file_name=file_name)
            page.set_content(''.join(paras))
            self._toc.append((level, page))
            return page

        def not_empty(paras):
            if paras:
                for p in paras:
                    if not self._pat_empty.match(p):
                        return True

        for line in self._iter_lines():
            self._row += 1
            if line.startswith(PAT_COMMENT):
                continue

            header = self._is_title(line)
            if header:
                if not_empty(paras):
                    yield write_page()
                paras = None
                self._toc.append(header)

            elif self._toc:
                if paras is None:
                    paras = []
                    titles = []
                    level, title = self._toc[-1]
                    for n, t in reversed(self._toc):
                        if n > level or (not isinstance(t, str)):
                            break
                        paras.insert(0, '<h{0}>{1}</h{0}>'.format(n, t))
                        titles.append(t)
                        level = n
                if line.strip() not in titles:
                    paras.append('<p>{0}</p>'.format(line))

        if not_empty(paras):
            yield write_page()

    def _is_title(self, line):
        for pat in self._pat_titles:
            m = pat.match(line)
            if m:
                return len(m.group(1)), m.group(2)


def register_reader():
    return TextReader()


if __name__ == '__main__':
    r = TextReader()
    print(r._is_title('##Title2\n'))

    # filename = '__test__.txt'
    # with open(filename, 'w') as f:
    #     f.write('##Title\nPara1\n###Title3\nPara2')
    # r.open('__test__.txt')
    # print(list(r.contents()))
    # r.close()
    # os.remove(filename)

    r.open('test2.txt')
    list(r._iter_lines())
