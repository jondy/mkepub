#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os
import subprocess

from glob import glob
from shutil import rmtree
from tempfile import mkdtemp

from ebooklib import epub

from . import COVER_SUFFIX

CMD_PDF2HTML = ['tools/pdf2html/pdf2htmlEx.exe',
                '--split-pages', '1', '--printing', '0',
                '--process-outline', '0',
                '--bg-format', 'jpg',
                '--external-hint-tool', 'tools/pdf2html/ttfautohint',
                '--page-filename', 'chapter%02d.xhtml']

logger = logging.getLogger('mkepub.pdfreader')


class PdfReader:

    def __init__(self):
        self._filename = None
        self._workpath = None

    def is_support(self, ext):
        return ext in ('.pdf',)

    def get_template(self):
        return None

    def get_cover(self):
        cover = os.path.join(self._filename[:-4] + COVER_SUFFIX)
        return cover if os.path.exists(cover) else None

    def open(self, filename):
        self._filename = filename
        self._workpath = mkdtemp(suffix='__pdf')

        cmdlist = CMD_PDF2HTML + ['--dest-dir', self._workpath]
        cmdlist.append(filename)
        p = subprocess.Popen(cmdlist,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        output, _ = p.communicate()

    def close(self):
        self._filename = None
        if self._workpath:
            rmtree(self._workpath)
            self._workpath = None

    def get_metadata(self):
        return {}

    def get_toc(self):
        return self._toc

    def images(self):
        for filename in glob(os.path.join(self._workpath, '*.jpg')):
            name = os.path.basename(filename)
            with open(filename, 'rb') as f:
                yield epub.EpubItem(uid=name,
                                    file_name="Text/%s" % name,
                                    media_type="images/jpg",
                                    content=f.read())

    def stylesheets(self):
        for filename in glob(os.path.join(self._workpath, '*.css')):
            name = os.path.basename(filename)
            with open(filename, "rb") as f:
                yield epub.EpubItem(uid=name,
                                    file_name="Styles/%s" % name,
                                    media_type="text/css",
                                    content=f.read())

    def contents(self):
        if self._workpath is None:
            return
        self._toc = []
        for filename in glob(os.path.join(self._workpath, '*.html')):
            name = os.path.basename(filename)
            url = "Text/%s" % name
            with open(filename, 'rb') as f:
                page = epub.EpubItem(file_name=url, content=f.read())
                # self._toc.append(page)
                yield page

        for filename in glob(os.path.join(self._workpath, 'chapter*.xhtml')):
            name = os.path.basename(filename)
            with open(filename, 'rb') as f:
                page = epub.EpubHtml(title=name,
                                     file_name="Text/%s" % name,
                                     content=f.read())
                yield page


def register_reader():
    return PdfReader()


if __name__ == '__main__':
    r = PdfReader()
