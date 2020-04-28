.PHONY: setup test integration lint check-sec all-tests doc

setup:
	@pip install -e .
	@pip install -r test/requirements.txt
	@pip install -r doc/requirements.txt

lint:
	@flake8 driftage test

test:
	@nosetests --exclude="test/integration" --with-coverage --cover-erase --cover-package=driftage

integration:
	@nosetests -w test/integration/

all-tests: test integration lint check-sec

check-sec:
	@echo "Running Bandit..."
	@bandit -r .

doc:
	@sphinx-build -b html doc doc/_build/html