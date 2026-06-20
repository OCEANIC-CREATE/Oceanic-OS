VENV=.venv
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip
UVICORN=$(VENV)/bin/uvicorn

.PHONY: venv install run test clean

venv:
	python3 -m venv $(VENV)

install: venv
	$(PIP) install -r requirements.txt

run: install
	$(UVICORN) oceanic_os.api:app --reload

test: install
	$(PYTHON) -m pytest -q

clean:
	rm -rf $(VENV)
	find . -name "__pycache__" -type d -exec rm -rf {} +
