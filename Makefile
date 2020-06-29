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
	@docker build -t ejabberd-driftage examples/ejabberd_config/
	@docker run --name ejabberd --rm -d -p 5222:5222 -p 5443:5443 ejabberd-driftage

ejabberd-admin:
	@docker exec -it ejabberd bin/ejabberdctl register admin localhost password

ejabberd-test-user:
	@docker exec -it ejabberd bin/ejabberdctl register monitor localhost passw0rd
	@docker exec -it ejabberd bin/ejabberdctl register analyser localhost passw0rd
	@docker exec -it ejabberd bin/ejabberdctl register planner localhost passw0rd
	@docker exec -it ejabberd bin/ejabberdctl register executor localhost passw0rd
