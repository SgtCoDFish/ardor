.PHONY: pyenv pyenv_system mypy

SOURCES := ardor.py $(shell echo ardor/*.py) $(shell echo ardor/worlds/*.py) $(shell echo ardor/consoles/*.py)

pyenv:
	@(pyenv versions | grep -q 3.5.5) || PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.5.5
	@pyenv local 3.5.5

pyenv_system:
	@pyenv local system

mypy:
	mypy ardor.py --ignore-missing-imports

dist/ardor: $(SOURCES) pkg/hook-tdl.py venv/build
	pyinstaller --additional-hooks-dir=./pkg/ -F ardor.py

venv/run: requirements.txt pyenv
	@rm -rf $@ || :
	python -m venv $@
	$@/bin/python -m pip install -r $<

venv/build: requirements_build.txt requirements.txt pyenv_system
	@rm -rf $@ || :
	python -m venv $@
	$@/bin/python -m pip install -r $<

dist/ardor.zip: $(SOURCES) run.sh install.sh data/fonts/consolas12x12_gs_tc.png
	mkdir -p dist
	zip $@ $^
