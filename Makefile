VENV=.venv
PYTHON=$(VENV)/bin/python3

install:
	python3 -m venv $(VENV)
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt
	@echo "Environment setup complete. Activate manually with:"
	@echo "  .venv\\Scripts\\activate (Windows)"
	@echo "  source .venv/bin/activate (Mac/Linux)"

run:
	$(PYTHON) -m src.app.app

freeze:
	$(PYTHON) -m pip freeze > requirements.txt

clean:
	rm -rf __pycache__ */__pycache__ */*/__pycache__