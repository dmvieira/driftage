.PHONY: setup test integration coverage lint check-sec all-tests doc

setup:
	@pip install -e .
	@pip install -r test/requirements.txt
	@pip install -r doc/requirements.txt

lint:
	@flake8 driftage test

test:
	@pytest --ignore="test/integration"

integration:
	@pytest --ignore="test/unit/"

coverage:
	@pytest --cov=driftage

all-tests: | coverage lint check-sec

check-sec:
	@echo "Running Bandit..."
	@bandit -r .

doc:
	@rm -rf doc/_build/
	@sphinx-build -b html doc doc/_build/html

ejabberd:
	@docker-compose -f examples/health_monitor/docker-compose.yml up --build -d ejabberd
