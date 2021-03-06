INNOSETUP = C:/Program Files (x86)/Inno Setup 5/Compil32.exe
PYINSTALLER = py37/Scripts/pyinstaller
PYUIC5 = py37/Scripts/pyuic5
PANDOC = tools/pandoc/pandoc
ifneq ($(PYINSTALLER),$(wildcard $(PYINSTALLER)))
    PYINSTALLER = ../easy-han/py34/Scripts/python -m PyInstaller
    INNOSETUP = C:/Program Files/Inno Setup 5/Compil32.exe
    PYUIC5 = C:/Python34/Lib/site-packages/PyQt5/pyuic5.bat
endif


HIDDEN_IMPORTS = --hidden-import chardet --hidden-import comtypes --hidden-import openpyxl --hidden-import transform
DATA_FILES = --add-data 'README.html;.' --add-data 'readers;readers' --add-data 'upload.xltx;.' --add-data 'tools/pdftk;tools/pdftk' --add-data 'tools/pdf2html;tools/pdf2html' --add-data 'config.json;.' --add-data 'templates;templates' --add-data 'tools/batch;tools/batch'

.PHONY: test build publish

test:
	ls test/

build: ui_main.ui ui_correct.ui
	$(PYUIC5) ui_main.ui > ui_main.py
	$(PYUIC5) ui_correct.ui > ui_correct.py

docs: README.md
	$(PANDOC) -s --metadata pagetitle="延安红云平台编辑工具" README.md > README.html

publish:
	$(PYINSTALLER) -y --name mkepub ${HIDDEN_IMPORTS} ${DATA_FILES} ${EXTRA_PATHS} main.py
	cp -a ../easy-han/dist/easy-han/qt5_plugins dist/mkepub
	"$(INNOSETUP)" /cc setup.iss
	scp -i ~/.ssh/id_rsa dist/yanhong-editor.exe root@yancloud.red:/www/wwwroot/www.yancloud.red/downloads

clean:
	rm -rf *.pyc *.pyo __pycache__
