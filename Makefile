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

all-tests: | test integration lint check-sec

check-sec:
	@echo "Running Bandit..."
	@bandit -r .

doc:
	@sphinx-build -b html doc doc/_build/html

ejabberd:
	@docker run --name ejabberd --rm -d -p 5222:5222 -p 5443:5443 ejabberd/ecs
	@docker exec -it ejabberd bin/ejabberdctl register admin localhost password