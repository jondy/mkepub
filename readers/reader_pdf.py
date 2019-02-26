#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess

from glob import glob
from shutil import rmtree
from tempfile import mkdtemp

CMD_PDF2HTML = ['pdf2htmlEx', '--split-pages', '1',
                '--embed-css', '0', '--embed-font', '0',
                '--embed-image', '0', '--embed-javascript', '0',
                '--embed-outline', '0',
                '--css-filename', 'pdf2.css',
                '--outline-filename', 'frame.xhtml',
                '--page-filename', 'page-%d.xhtml']


class PdfReader:

    def __init__(self):
        self._filename = None
        self._workpath = None

    def is_support(self, ext):
        return ext in ('.pdf',)

    def get_template(self):
        return None

    def get_cover(self):
        return None

    def open(self, filename):
        self._filename = filename
        self._workpath = mkdtemp(suffix='__pdf')

        cmdlist = CMD_PDF2HTML + ['--dest-dir', self._workpath]
        cmdlist.append(filename)
        p = subprocess(cmdlist,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT)
        output, _ = p.communicate()

    def close(self):
        self._filename = None
        if self._workpath:
            rmtree(self._workpath)
            self._workpath = None

    def images(self):
        return glob(os.path.join(self._workpath, '*.jpg'))

    def stylesheets(self):
        return [os.path.join(self._workpath, 'pdf2.css')]

    def pages(self):
        if self._workpath is None:
            return
        yield from glob(os.path.join(self._workpath, 'page-*.xhtml'))

    def _is_title(self, line):
        for pat in self._pat_titles:
            m = pat.match(line)
            if m:
                return len(m.group(1)) - 2, m.group(2)


# def register_reader():
#     return PdfReader()


if __name__ == '__main__':
    r = PdfReader()
