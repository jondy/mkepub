#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os
import subprocess

from glob import glob
from shutil import rmtree
from tempfile import mkdtemp

from PyPDF2 import PdfFileReader
from ebooklib import epub

from . import COVER_SUFFIX

CMD_PDF2HTML = ['tools/pdf2html/pdf2htmlEx.exe',
                '--split-pages', '1', '--printing', '0',
                '--tounicode', '0', '--process-outline', '0',
                '--embed-css', '0', '--embed-font', '0',
                '--embed-javascript', '1', '--embed-image', '0',
                '--css-filename', 'epub.css', '--bg-format', 'jpg',
                '--page-filename', 'chapter%02d.xhtml']

PREV_TEMPLATE = '''<div style="text-align: center; margin-bottom: -1rem;">
<a href="%s">
<svg aria-hidden="true" focusable="false" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512" height="28">
<path fill="#f0f0f0" d="M177 255.7l136 136c9.4 9.4 9.4 24.6 0 33.9l-22.6 22.6c-9.4 9.4-24.6 9.4-33.9 0L160 351.9l-96.4 96.4c-9.4 9.4-24.6 9.4-33.9 0L7 425.7c-9.4-9.4-9.4-24.6 0-33.9l136-136c9.4-9.5 24.6-9.5 34-.1zm-34-192L7 199.7c-9.4 9.4-9.4 24.6 0 33.9l22.6 22.6c9.4 9.4 24.6 9.4 33.9 0l96.4-96.4 96.4 96.4c9.4 9.4 24.6 9.4 33.9 0l22.6-22.6c9.4-9.4 9.4-24.6 0-33.9l-136-136c-9.2-9.4-24.4-9.4-33.8 0z"></path></svg>
</a>
</div>'''
NEXT_TEMPLATE = '''<div style="text-align: center;">
<a href="%s">
<svg aria-hidden="true" focusable="false" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512" height="28">
<path fill="#f0f0f0" d="M143 256.3L7 120.3c-9.4-9.4-9.4-24.6 0-33.9l22.6-22.6c9.4-9.4 24.6-9.4 33.9 0l96.4 96.4 96.4-96.4c9.4-9.4 24.6-9.4 33.9 0L313 86.3c9.4 9.4 9.4 24.6 0 33.9l-136 136c-9.4 9.5-24.6 9.5-34 .1zm34 192l136-136c9.4-9.4 9.4-24.6 0-33.9l-22.6-22.6c-9.4-9.4-24.6-9.4-33.9 0L160 352.1l-96.4-96.4c-9.4-9.4-24.6-9.4-33.9 0L7 278.3c-9.4 9.4-9.4 24.6 0 33.9l136 136c9.4 9.5 24.6 9.5 34 .1z"></path></svg>
</a>
</div>'''

logger = logging.getLogger('mkepub.pdfreader2')


def get_num_pages(filename):
    with open(filename, 'rb') as f:
        r = PdfFileReader(f, strict=False)
        return r.getNumPages()


class PdfReader:

    def __init__(self):
        self._filename = None
        self._workpath = []

    def is_support(self, ext):
        return ext in ('.pdf',)

    def get_template(self):
        return None

    def _get_content(self, styles, pages):
        path = os.path.dirname(__file__)
        filename = os.path.join(path, '..', 'templates', 'pdf_frame.html')
        with open(filename, 'r') as f:
            return f.read() \
                .replace('%CSS_LINKS%', ''.join(styles)) \
                .replace('%PAGES%', ''.join(pages))

    def get_cover(self):
        cover = os.path.join(self._filename[:-4] + COVER_SUFFIX)
        return cover if os.path.exists(cover) else None

    def open(self, filename):
        n = get_num_pages(filename)

        batch = 100
        logger.info('Total pages: %s', n)
        for i in range(1, n, batch):
            p = mkdtemp(prefix='mkepub_', suffix='_pdf')
            self._workpath.append(p)

            j = i + batch - 1
            logger.info('Convert pages from %d to %d', i, j)
            logger.info('Target path: %s', p)

            args = ['--dest-dir', p, '-f', str(i), '-l', str(j), filename]
            cmdlist = CMD_PDF2HTML + args

            logger.info('Run command: %s', ' '.join(cmdlist))
            p = subprocess.Popen(cmdlist)
            p.communicate()

            if p.returncode != 0:
                raise RuntimeError('转换失败，pdf2htmlEx 出错')
            logger.info('Convert page %d to %d OK', i, j)
        self._filename = filename

    def close(self):
        self._filename = None
        for p in self._workpath:
            rmtree(p)
        self._workpath = []

    def get_metadata(self):
        return {}

    def get_toc(self):
        return self._toc

    def images(self):
        for p in self._workpath:
            for filename in glob(os.path.join(p, '*.jpg')):
                name = os.path.basename(filename)
                with open(filename, 'rb') as f:
                    yield epub.EpubItem(uid=name,
                                        file_name="Text/%s" % name,
                                        media_type="images/jpg",
                                        content=f.read())

    def stylesheets(self):
        n = 0
        for p in self._workpath:
            for filename in glob(os.path.join(p, '*.css')):
                name = str(n) + '/' + os.path.basename(filename)
                with open(filename, "rb") as f:
                    yield epub.EpubItem(uid=name,
                                        file_name="Styles/%s" % name,
                                        media_type="text/css",
                                        content=f.read())
            n += 1

    def contents(self):
        if not self._workpath:
            return
        self._toc = []

        def _page_name(i):
            return "pdf_frame%s.html" % (str(i) if i else '')

        n = len(self._workpath)
        for i in range(n):
            p = self._workpath[i]
            for filename in glob(os.path.join(p, '*.html')):
                with open(filename, 'r') as f:
                    content = f.read()
                m = 'link rel="stylesheet" href="'
                s = '../Styles/%d/' % i
                content = content.replace(m, m+s)
                if i:
                    m = '<div id="page-container">'
                    s = PREV_TEMPLATE % _page_name(i-1)
                    content = content.replace(m, m+s)
                if i < n - 1:
                    m = '</div>\n<div class="loading-indicator">'
                    s = NEXT_TEMPLATE % _page_name(i+1)
                    content = content.replace(m, s+m)
                url = "Text/%s" % _page_name(i)
                page = epub.EpubItem(file_name=url, content=content)
                yield page

        for p in self._workpath:
            for filename in glob(os.path.join(p, 'chapter*.xhtml')):
                name = os.path.basename(filename)
                with open(filename, 'rb') as f:
                    page = epub.EpubItem(file_name="Text/%s" % name,
                                         content=f.read())
                    yield page

        n = 0
        for p in self._workpath:
            prefix = 'Styles/' + str(n)
            n += 1
            for filename in glob(os.path.join(p, '*.woff')):
                name = os.path.basename(filename)
                with open(filename, 'rb') as f:
                    page = epub.EpubItem(
                        file_name="%s/%s" % (prefix, name),
                        content=f.read())
                    yield page


def register_reader():
    return PdfReader()


if __name__ == '__main__':
    r = PdfReader()
