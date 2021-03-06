#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import chardet
import os
import re

from ebooklib import epub
from . import COVER_SUFFIX

PAT_TITLE = r'^(#+)\s*(.*)\s*$'
PAT_EMPTY = r'<p>\s*</p>'
PAT_COMMENT = '!#'
PAT_ALIGN_RIGHT = '#:'
PAT_INLINE_IMAGE = r'!\[(.+)\]\((.+)\)'

TEMPLATE_PARA = '<p>{0}</p>'
TEMPLATE_INLINE_IMAGE = '<div class="picture"><img src="../Images/{0}" alt="{1}"/><p>{1}</p></div>'
TEMPLATE_RIGHT_PARA = '<p class="text-right">{0}</p>'

MAX_META_ROW = 100
PAT_METADATAS = {
    'title': ('书名:', '书名：'),
    'author': ('作者:', '作者：'),
    'publisher': ('出版者:', '出版者：'),
    'date': ('出版时间:', '出版时间：'),
    'ISBN': ('ISBN:', 'ISBN：'),
}


def build_toc(sections):
    if not sections:
        return None

    def make_node(t):
        return epub.Section(t) if isinstance(t, str) else t, []

    level, page = sections[0]
    node = make_node(page)
    stack = [node]
    toc = [node]

    def reform_node():
        if not stack[0][1]:
            parent = stack[1][1] if len(stack) > 1 else toc
            temp = parent.pop()
            parent.append(temp[0])

    ref = level
    for level, page in sections[1:]:
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

    return toc


class TextReader:

    def __init__(self):
        self._filename = None
        self._toc = None
        self._encoding = None
        self._pat_titles = [re.compile(PAT_TITLE)]
        self._pat_empty = re.compile(PAT_EMPTY)
        self._pat_inline_image = re.compile(PAT_INLINE_IMAGE)

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
        self._images = []
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
        return build_toc(self._toc)

    def images(self):
        yield from self._images

    def stylesheets(self):
        return []

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
            page.set_content('<div>%s</div>' % ''.join(paras))
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
                if line.strip() and line.strip() not in titles:
                    if line.startswith(PAT_ALIGN_RIGHT):
                        n = len(PAT_ALIGN_RIGHT)
                        paras.append(TEMPLATE_RIGHT_PARA.format(line[n:]))
                    else:
                        m = self._pat_inline_image.match(line.strip())
                        if m:
                            title, url = m.group(1, 2)
                            fname = os.path.join(os.path.dirname(self._filename), url)
                            media_type = 'images/' + url.rsplit('.')[-1]
                            with open(fname, 'rb') as f:
                                img = epub.EpubItem(
                                    file_name='Images/' + url,
                                    media_type=media_type,
                                    content=f.read())
                            self._images.append(img)
                            paras.append(TEMPLATE_INLINE_IMAGE.format(url, title))
                        else:
                            paras.append(TEMPLATE_PARA.format(line))

        if not_empty(paras):
            yield write_page()

    def _is_title(self, line):
        if line.startswith(PAT_ALIGN_RIGHT):
            return
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
