# Django Best Practices and Clean Code

<br />

## List of Contents:
### 1. [Django Project Best Practices to Keep Your Developers Happy](#content-1)


<br />

---

## Contents:

## [Django Project Best Practices to Keep Your Developers Happy](https://betterprogramming.pub/django-project-best-practices-to-keep-your-developers-happy-bcb522f3eb12) <span id="content-1"></span>

### A Custom CLI Tool for Your Django Project
- Instead typing:
  ```shell
  python3 -m venv env
  source env/bin/activate
  pip install -r requirements.txt
  python3 manage.py makemigrations
  python3 manage.py migrate
  python3 manage.py collectstatic
  python3 manage.py runserver
  ```
- Using Makefile:
  ```makefile
  SHELL := /bin/bash

  include .env

  .PHONY: help
  help: ## Show this help
      @egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

  .PHONY: venv
  venv: ## Make a new virtual environment
      python3 -m venv $(VENV) && source $(BIN)/activate

  .PHONY: install
  install: venv ## Make venv and install requirements
      $(BIN)/pip install -r requirements.txt

  migrate: ## Make and run migrations
      $(PYTHON) manage.py makemigrations
      $(PYTHON) manage.py migrate

  db-up: ## Pull and start the Docker Postgres container in the background
      docker pull postgres
      docker-compose up -d

  db-shell: ## Access the Postgres Docker database interactively with psql
      docker exec -it container_name psql -d $(DBNAME)

  .PHONY: test
  test: ## Run tests
      $(PYTHON) $(APP_DIR)/manage.py test application --verbosity=0 --parallel --failfast

  .PHONY: run
  run: ## Run the Django server
      $(PYTHON) $(APP_DIR)/manage.py runserver

  start: install migrate run ## Install requirements, apply migrations, then start development server
  ```
- You’ll notice the presence of the line include .env above. This ensures that make has access to environment variables stored in a file called .env. 
- This allows Make to utilize these variables in its commands (e.g. the name of my virtual environment or to pass in $(DBNAME) to psql).
- What’s with that weird ## comment syntax? A Makefile like this gives you a handy suite of command-line aliases you can check in to your Django project.
- The help command above, which runs by default, prints a helpful list of available commands when you run make or make help:
  ```text
  help                 Show this help
  venv                 Make a new virtual environment
  install              Make venv and install requirements
  migrate              Make and run migrations
  db-up                Pull and start the Docker Postgres container in the background
  db-shell             Access the Postgres Docker database interactively with psql
  test                 Run tests
  run                  Run the Django server
  start                Install requirements, apply migrations, then start development server
  ```

### Save Your Brainpower With Pre-Commit Hooks
- One area that’s a no-brainer is using pre-commit hooks to lint code prior to checking it in. This helps to ensure the quality of the code your developers check in, but most importantly, it ensures that no one on your team is spending time trying to remember if it should be single or double quotes or where to put a line break.
- Here is my configuration file, .pre-commit-config.yaml, for my Django projects:
  ```yaml
  fail_fast: true
  repos:
    - repo: https://github.com/pre-commit/pre-commit-hooks
      rev: v3.1.0
      hooks:
        - id: detect-aws-credentials
    - repo: https://github.com/psf/black
      rev: 19.3b0
      hooks:
        - id: black
    - repo: https://github.com/asottile/blacken-docs
      rev: v1.7.0
      hooks:
        - id: blacken-docs
          additional_dependencies: [black==19.3b0]
    - repo: local
      hooks:
        - id: markdownlint
          name: markdownlint
          description: "Lint Markdown files"
          entry: markdownlint '**/*.md' --fix --ignore node_modules --config "./.markdownlint.json"
          language: node
          types: [markdown]
  ```
- These hooks check for accidental secret commits, format Python files using Black, format Python snippets in Markdown files using blacken-docs, and lint Markdown files as well.

### Useful gitignores
- Toptal’s [gitignore.io](https://www.toptal.com/developers/gitignore) can be a nice resource for generating a robust .gitignore file.
- I still recommend examining the generated results yourself to ensure that ignored files suit your use case and that nothing you want ignored is commented out


### Continuous Testing With GitHub Actions
- Tests that run in a consistent environment on every pull request can help eliminate “works on my machine” conundrums, as well as ensure no one’s sitting around waiting for a test to run locally.



**[⬆ back to top](#list-of-contents)**

<br />

---

## References:
- https://betterprogramming.pub/django-project-best-practices-to-keep-your-developers-happy-bcb522f3eb12