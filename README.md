[![Coverage Status](https://coveralls.io/repos/github/gr1d99/shopping-list/badge.svg?branch=challenge-2)](https://coveralls.io/github/gr1d99/shopping-list?branch=challenge-2) [![Build Status](https://travis-ci.org/gr1d99/shopping-list.svg?branch=challenge-2)](https://travis-ci.org/gr1d99/shopping-list) [![Code Climate](https://codeclimate.com/github/gr1d99/shopping-list/badges/gpa.svg)](https://codeclimate.com/github/gr1d99/shopping-list) [![Issue Count](https://codeclimate.com/github/gr1d99/shopping-list/badges/issue_count.svg)](https://codeclimate.com/github/gr1d99/shopping-list)

# shopping-list

Is a flask powered web application that allows users to keep track of their shopping items and also allows a user to 
share the shopping lists with others, this web application also allows you to mark items that you have already 

## Prerequisites

- Python3 [Installation](https://www.python.org/downloads/)
- Git [Installation](https://git-scm.com/downloads)

## Usage
> 1. Clone this repo `git clone https://github.com/gr1d99/shopping-list.git`
> 2. Change your current directory to `shopping-list`
> 3. On your terminal type `git checkout develop`
> 4. Create a virtual enviroment `virtualenv --python=python3 env` then activate it `source env/bin/activate`
> 5. Install requirements `pip3 install -r requirements.txt`
> 6. Generate your SECRET_KEY by running `python manage.py generate_secret`, 
> the command will generate a **`secret.txt`** file that will contain the apps secret key,
> after running the command, copy the generated key and use it to
> set enviroment variable `SECRET_KEY` so that it will be available to the app configuration.
> eg.
> ```bash
> $ export SECRET_KEY=<generated key goes here>
> ```
> **DEBUG** is set to `True` but you may change it.
> 
> 7. Finally deploy your web app by running the command `python manage.py runserver` 

> **The app does not have much functionality. What you can do for now is**
> - _Create an account_
> - _Login_
> - _create/retrieve/update and delete shopping lists through the dashboard._
> - _create/retrieve/update and delete shopping items._
> - _add shopping items to a shopping list._
> - _view created shopping list and its items._
> - _mark and un-mark shopping items._



## Running the tests

All tests are located in the root of the project in a folder named `tests`.

> ### [nose](http://nose.readthedocs.io/en/latest/testing.html)
> Test the project using nose and view coverage report on your terminal
> ```bash
>  $ nosetests --with-coverage
> ```

## Deployment
This app can be deployed on [Heroku](https://www.heroku.com/what) cloud.

> ### deploy on heroku with git
> _**if you do not have any expirience with heroku kindly [start here](https://devcenter.heroku.com/articles/getting-started-with-python#introduction) to get some basics**_
> 1. create an [account](https://signup.heroku.com/) on heroku.
> 2. read this [article](https://devcenter.heroku.com/articles/git) and use it as a reference.

> ## Built with
> 1. [Flask](http://flask.pocoo.org/)

> ## Authors
> Gideon Kimutai

> ## License
> This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


> ## Acknowledgments
> - Andela Kenya
> - Boot-camp LFAs
> - The A-TEAM members(both week one and week two team)
> - All candidates.

> ### demo
> [Shopping List App](http://gideonshoppingapp.herokuapp.com/)

## Screenshots
> ## Signup Page
>![Signup](https://github.com/gr1d99/shopping-list/blob/challenge-1/screenshots/signup.png)

> ## Login Page
> ![Login](https://github.com/gr1d99/shopping-list/blob/challenge-1/screenshots/login.png)

> ## Home Page
> ![Home Page](https://github.com/gr1d99/shopping-list/blob/challenge-1/screenshots/index.png)

> ## Dashboard 
> ![Dashboard](https://github.com/gr1d99/shopping-list/blob/challenge-1/screenshots/dashboardd.png)

> ## View Items Page
> ![Items Page](https://github.com/gr1d99/shopping-list/blob/challenge-1/screenshots/itemsdashbord.png)


