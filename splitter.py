#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess

from PyPDF2 import PdfFileReader

CMD_PDFTK = os.path.normpath('tools/pdftk/pdftk.exe')


def get_pdf_num_pages(filename):
    with open(filename, 'rb') as f:
        r = PdfFileReader(f, strict=False)
        return r.getNumPages()


def split_pdf_file(source, target, pages, cwd=None):
    cmdlist = [CMD_PDFTK, os.path.abspath(source), 'cat', pages,
               'output', os.path.abspath(target)]
    p = subprocess(cmdlist,
                   cwd=cwd,
                   stdout=subprocess.PIPE,
                   stderr=subprocess.STDOUT)
    output, _ = p.communicate()
    return p.returncode, output
