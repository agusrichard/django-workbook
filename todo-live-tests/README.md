<center><h1>Todo Project Fully Tested</h1></center>

### Table of Contents:
- [Description](#description)
- [GIF of what you'll see on this app](#gif-of-what-youll-see-on-this-app)
- [Installation/Development](#installationdevelopment)
- [Running Tests](#running-tests)

## Description
This project serves as coding material for Medium's article.  The article itself talks about multi-layered tests in Django and how to achieve 100% test coverage. It starts with testing models, forms, views, urls, and up to writing end-to-end tests using Selenium Web Driver.

## GIF of what you'll see on this app
Placeholder

## Installation/Development
- Clone/Download this repository and change directory to this project
- Download chrome web driver based on your chrome browser version
- Create a folder inside root directory of this project named driver and put the Chrome web driver there. Make sure the file name is `chromedriver.exe` (if you're on Windows)
- Create virtual environment (highly suggested) by running:
  ```shell
  python -m venv venv
  ```
- Activate virtual environment (depends on your operating system)
- Install all dependencies:
  ```shell
  pip install -r requirements.txt
  ```
- Migrate database:
  ```shell
  python manage.py migrate
  ```
- Finally, running the server:
  ```shell
  python manage.py runserver
  ```


## Running Tests
- Without coverage:
  ```shell
  python manage.py test
  ```
- With coverage:
  ```shell
  coverage run ./manage.py test
  ```
- Create coverage's html report:
  ```shell
  coverage html
  ```
- After you run the above command, it will create a folder `htmlcov`.
- Open `index.html` on a browser to see the test coverage
- If you want to see how the end-to-end tests run, change this variable `WEB_DRIVER_HEADLESS` inside settings.py to `False`