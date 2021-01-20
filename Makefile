.PHONY: setup test integration coverage lint check-sec all-tests doc result example

setup:
	@pip install -e .
	@pip install -r test/requirements.txt
	@pip install -r doc/requirements.txt

lint:
	@flake8 driftage test examples

test:
	@pytest --ignore="test/integration"

integration:
	@pytest --ignore="test/unit/"
	@-docker-compose -f examples/health_monitor/docker-compose.yml down --remove-orphans

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
	@-docker rmi -f healthmonitor_ejabberd
	@docker-compose -f examples/health_monitor/docker-compose.yml up --build -d ejabberd

result:
	@docker-compose -f examples/analyse-in-memory/docker-compose.yml down --remove-orphans
	@docker-compose -f examples/analyse-in-memory/docker-compose.yml up --build

example:
	@mkdir -p examples/health_monitor/build/timescaledb
	@mkdir -p examples/health_monitor/build/executor
	@docker-compose -f examples/health_monitor/docker-compose.yml down --remove-orphans
	@docker-compose -f examples/health_monitor/docker-compose.yml up --build