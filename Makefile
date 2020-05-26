.PHONY: setup test integration lint check-sec all-tests doc

setup:
	@pip install -e .
	@pip install -r test/requirements.txt
	@pip install -r doc/requirements.txt

lint:
	@flake8 driftage test

test:
	@pytest --ignore="test/integration" --cov=driftage

integration:
	@pytest --ignore="test/unit/"

all-tests: | test integration lint check-sec

check-sec:
	@echo "Running Bandit..."
	@bandit -r .

doc:
	@rm -rf doc/_build/
	@sphinx-build -b html doc doc/_build/html

ejabberd:
	@docker build -t ejabberd-driftage . 
	@docker run --name ejabberd --rm -d -p 5222:5222 -p 5443:5443 ejabberd-driftage

ejabberd-user:
	@docker exec -it ejabberd bin/ejabberdctl register admin localhost password