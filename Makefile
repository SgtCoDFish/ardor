.PHONY: pyenv pkg mypy

pyenv:
	@(pyenv versions | grep -q 3.5.5) || pyenv install 3.5.5
	@pyenv local 3.5.5

mypy:
	mypy ardor.py --ignore-missing-imports

venv/run: requirements.txt pyenv 
	@rm -rf $@ || :
	python -m venv $@
	$@/bin/python -m pip install -r $<

venv/build: requirements_build.txt requirements.txt pyenv
	@rm -rf $@ || :
	python -m venv $@
	$@/bin/python -m pip install -r $<
