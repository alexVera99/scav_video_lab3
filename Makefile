lint:
	./venv/bin/pylint src test
	./venv/bin/pydocstyle src test
	./venv/bin/pycodestyle --select E,W src
	./venv/bin/mypy src