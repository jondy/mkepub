#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import chardet
import os
import re

from ebooklib import epub

PAT_TITLE = r'^(#+)(.*)\s*$'
PAT_CONTENT = '!#'

COVER_SUFFIX = '-封面.jpg'

# TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'templates', 'txt')

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
        return None

    def _iter_lines2(self):
        if self._filename is None:
            return
        with open(self._filename, 'rb') as f:
            buf = f.read()
            charinfo = chardet.detect(buf)
        yield from buf.decode(charinfo['encoding']).splitlines()

    def _iter_lines(self):
        if self._filename is None:
            return
        with open(self._filename,
                  encoding=self._encoding,
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
            if row > 100:
                break
        return meta

    def get_toc(self):
        return self._toc

    def contents(self):
        titles = []
        paras = None

        try:
            index = 0
            self._toc = []

            def write_page():
                page = epub.EpubHtml(title=titles[-1][-1],
                                     file_name='page-%d.xhtml' % index,
                                     lang='zh')
                page.set_content(''.join(paras))
                n, t = self._toc.pop()
                self._toc.append((n, page))
                return page

            for line in self._iter_lines():
                if line.startswith(PAT_CONTENT):
                    paras = []
                    continue

                header = self._is_title(line)
                if header:
                    if paras:
                        index += 1
                        yield write_page()
                        titles = []
                    paras = None
                    titles.append(header)
                    self._toc.append(header)

                elif paras is not None:
                    for n, t in titles:
                        if line.strip() == t:
                            paras.append('<h{0}>{1}</h{0}>'.format(n, t))
                            break
                    else:
                        paras.append('<p>{0}</p>'.format(line))

            if paras:
                index += 1
                yield write_page()

        finally:
            pass

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
