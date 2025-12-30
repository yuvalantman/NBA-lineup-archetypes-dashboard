VENV=.venv
<<<<<<< HEAD
PYTHON=$(VENV)/bin/python3

install:
	python3 -m venv $(VENV)
=======
PYTHON=$(VENV)/Scripts/python

install:
	python -m venv $(VENV)
>>>>>>> 35217567569a3e4a4d5abe233313123ba3bbeed6
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt
	@echo "Environment setup complete. Activate manually with:"
	@echo "  .venv\\Scripts\\activate (Windows)"
	@echo "  source .venv/bin/activate (Mac/Linux)"

run:
<<<<<<< HEAD
	$(PYTHON) -m src.app.app
=======
	$(PYTHON) -m src.app.run
>>>>>>> 35217567569a3e4a4d5abe233313123ba3bbeed6

freeze:
	$(PYTHON) -m pip freeze > requirements.txt

clean:
<<<<<<< HEAD
	rm -rf __pycache__ */__pycache__ */*/__pycache__
=======
	rm -rf __pycache__ */__pycache__ */*/__pycache__
>>>>>>> 35217567569a3e4a4d5abe233313123ba3bbeed6
