# Todo Project Fully Tested


### Table of Contents:
- [Description](#description)
- [What you'll see on this app](#what-youll-see-on-this-app)
- [Installation/Development](#installationdevelopment)
- [Running Tests](#running-tests)


## Description
This project serves as coding material for Medium's article here:
> https://levelup.gitconnected.com/writing-tests-for-a-foolproof-django-project-3c5527bd602d

The article itself talks about multi-layered tests in Django and how to achieve 100% test coverage. It starts with testing models, forms, views, urls, and up to writing end-to-end tests using Selenium Web Driver.


## What you'll see on this app
https://user-images.githubusercontent.com/51517401/167234128-7a132f13-efdb-497a-bccb-071642fba659.mp4


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
