
PYUIC5 = py37/Scripts/pyuic5
PYINSTALLER = py37/Scripts/pyinstaller
PANDOC = tools/pandoc/pandoc
INNOSETUP = C:/Program Files (x86)/Inno Setup 5/Compil32.exe

HIDDEN_IMPORTS = --hidden-import chardet --hidden-import comtypes --hidden-import openpyxl --hidden-import pypdf2
DATA_FILES = --add-data 'README.html;.' --add-data 'readers;readers' --add-data 'upload.xltx;.' --add-data 'tools/pdftk;tools/pdftk' --add-data 'config.json;.' --add-data 'templates;templates'

.PHONY: test build publish

test:
	ls test/

build: ui_main.ui ui_correct.ui
	$(PYUIC5) ui_main.ui > ui_main.py
	$(PYUIC5) ui_correct.ui > ui_correct.py

docs: README.md
	$(PANDOC) -s --metadata pagetitle="延安红云平台编辑工具" README.md > README.html

publish:
	$(PYINSTALLER) -y -w --name mkepub ${HIDDEN_IMPORTS} ${DATA_FILES} main.py transform.py
	"$(INNOSETUP)" /cc setup.iss
	scp -i ~/.ssh/id_rsa dist/yanhong-editor.exe root@yancloud.red:/www/wwwroot/www.yancloud.red/downloads

clean:
	rm -rf *.pyc *.pyo __pycache__
