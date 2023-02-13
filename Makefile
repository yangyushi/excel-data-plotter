PYTHON = python3
PYINSTALLER = pyinstaller

all: package

package:
	$(PYINSTALLER) --onefile main.py  --name=data_plotter --upx-exclude='*matplotlib*'
	mv dist/data_plotter .

clean:
	rm -rf build dist __pycache__ .DS_Store
	find . -name "*.spec" -delete

.PHONY: all package clean

