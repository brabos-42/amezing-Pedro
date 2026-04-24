VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

$(VENV):
	python3 -m venv $(VENV)

 install: $(VENV)
	$(PYTHON) -m pip install --upgrade pip 
	$(PIP) install -r requirements.txt
run: $(VENV)
	$(PYTHON) a_maze_ing.py config.txt

debug: $(VENV)
	$(PYTHON) -m pdb a_maze_ing.py config.txt

clean:
	rm -rf __pycache__ .mypy_cache

lint: $(VENV)
	$(VENV)/bin/flake8 .
	$(VENV)/bin/mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

actualize: $(VENV)
	$(VENV)/bin/pip freeze > requirements.txt
	