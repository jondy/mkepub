#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import chardet
import os
import re

from ebooklib import epub

PAT_TITLE = r'^(#+)\s*(.*)\s*$'
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

    def is_support(self, ext):
        return ext in ('.txt',)

    def get_template(self):
        return os.path.join(os.path.dirname(__file__), 'templates', 'txt')

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
                for s in pats:
                    if line.startswith(s):
                        meta[k] = line[len(s):].strip()
                        break
                if meta.get(k):
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

        def write_page():
            self._pindex += 1
            level, title = self._toc.pop()
            page = epub.EpubHtml(title=title,
                                 file_name='page-%d.xhtml' % self._pindex)
            page.set_content(''.join(paras))
            self._toc.append((level, page))
            return page

        for line in self._iter_lines():
            self._row += 1
            if line.startswith(PAT_COMMENT):
                continue

            header = self._is_title(line)
            if header:
                if paras:
                    yield write_page()
                paras = None
                self._toc.append(header)

            elif self._toc:
                if paras is None:
                    paras = []
                    level, title = self._toc[-1]
                    paras.append('<h{0}>{1}</h{0}>'.format(level, title))
                    if line.strip() == title:
                        continue
                paras.append('<p>{0}</p>'.format(line))

        if paras:
            yield write_page()

    def _is_title(self, line):
        for pat in self._pat_titles:
            m = pat.match(line)
            if m:
                return len(m.group(1)), m.group(2)


def register_reader():
    return TextReader()


def build_toc(sections):
    if not sections:
        return None

    def make_node(t):
        return epub.Section(t) if isinstance(t, str) else t, []

    level, page = sections[0][0]
    node = make_node(page)
    stack = [node]
    toc = [node]

    def reform_node():
        if not stack[0][1]:
            parent = stack[1][1] if len(stack) > 1 else toc
            temp = parent.pop()
            parent.append(temp[0])

    ref = level
    for level, page in sections:
        node = make_node(page)
        n = level - ref
        if n >= len(stack):
            if not isinstance(page, str):
                for parent in stack:
                    if not isinstance(parent[0], epub.Section):
                        break
                    if parent[0].href == '':
                        parent[0].href = page.get_name()
            stack[0][1].append(node)
            stack.insert(0, node)
        else:
            reform_node()

            if n == 0:
                stack = [node]
                toc.append(node)
            else:
                stack[:n] = []
                stack[0][1].append(node)
    reform_node()


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
