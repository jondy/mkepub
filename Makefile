
PYUIC5 = py37/Scripts/pyuic5
PYINSTALLER = py37/Scripts/pyinstaller
PANDOC = tools/pandoc/pandoc

HIDDEN_IMPORTS = --hidden-import chardet --hidden-import comtypes --hidden-import openpyxl --hidden-import pypdf2
DATA_FILES = --add-data 'README.html;.' --add-data 'readers;readers' --add-data 'upload.xltx;.' --add-data 'tools/pdftk;tools/pdftk'

.PHONY: test build publish

test:
	ls test/

build: ui_main.ui
	$(PYUIC5) ui_main.ui > ui_main.py

docs: README.md
	$(PANDOC) -s --metadata pagetitle="延安红云平台编辑工具" README.md > README.html

publish:
	$(PYINSTALLER) -y -w --name mkepub ${HIDDEN_IMPORTS} ${DATA_FILES} main.py transform.py

clean:
	rm -rf *.pyc *.pyo __pycache__
