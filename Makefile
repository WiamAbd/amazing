PYTHON = python3
MAIN = a_maze_ing.py

.PHONY: install run clean lint

install:
	$(PYTHON) -m pip install --user flake8 mypy

run:
	$(PYTHON) $(MAIN) $(CONFIG)

clean:
	rm -rf __pycache__ .mypy_cache
	find . -name "*.pyc" -delete

lint:
	flake8 .
	mypy .