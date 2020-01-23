help:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

VENV_NAME?=venv
VENV_ACTIVATE_PATH=$(VENV_NAME)/bin/activate
PYTHON_PATH=${VENV_NAME}/bin/python3

venv: requirements.txt ## Setup virtual environment and dependencies
		test -d $(VENV_NAME) || virtualenv --python=python3 $(VENV_NAME)
		. $(VENV_ACTIVATE_PATH); pip install -Ur requirements.txt
		touch $(VENV_ACTIVATE_PATH)

.PHONY=lint
lint: venv ## Run Flake8
		$(PYTHON_PATH) -m flake8 --statistics --count \
		--exclude=venv,.git,__pycache__,.pytest_cache \
		--max-complexity 10

.PHONY=test
test: venv ## Run test
		. $(VENV_ACTIVATE_PATH); $(PYTHON_PATH) -m pytest
		. $(VENV_ACTIVATE_PATH); behave

.PHONY=run
run: venv ## Run the project
		$(PYTHON_PATH) run.py

.PHONY=clean
clean: ## Clean virtual environment
		rm -rf $(VENV_NAME)

.PHONY=cloudbuild
cloudbuild: ## Push changes to CloudBuild
		gcloud builds submit
