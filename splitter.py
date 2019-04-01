#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import math
import os
import subprocess

from PyPDF2 import PdfFileReader

CMD_PDFTK = os.path.normpath('tools/pdftk/pdftk.exe')


def get_pdf_info(filename):
    with open(filename, 'rb') as f:
        r = PdfFileReader(f, strict=False)
        pages = r.getNumPages()

    statinfo = os.stat(filename)
    return pages, statinfo.st_size


def get_split_pages(filename, size=10):
    with open(filename, 'rb') as f:
        r = PdfFileReader(f, strict=False)
        pages = r.getNumPages()

    pagelist = []
    statinfo = os.stat(filename)
    n = math.trunc(statinfo.st_size / (1024 * 1024) / size)
    if n:
        n += 1
        delta = int(pages / n)
        i = 1
        while i < pages:
            pagelist.append([i, i + delta - 1])
            i += delta
        pagelist[-1][-1] = pages
    return pagelist


def split_pdf_file(source, target, pages, cwd=None):
    cmdlist = [CMD_PDFTK, os.path.abspath(source), 'cat', pages,
               'output', os.path.abspath(target)]
    p = subprocess.Popen(cmdlist,
                         cwd=cwd,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    output, _ = p.communicate()
    return p.returncode, output
