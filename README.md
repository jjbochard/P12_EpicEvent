# P12_EpicEvents
## Table of contents
- [Table of content](#table-of-content)
- [Foreword](#foreword)
- [Installation](#installation)
- [How to use](#how-to-use)
- [Possible improvements](#possible-improvements)

## Foreword


The aim of this project is to build a secure Customer Relationship Management (CRM)
I have to use Django REST framework to build an API.
I also have to use PostgreSQL database and make front-end interface with the admin django in order to let the administrators manage the application.

When a new user create his account, an admin must give him a group (Sales or Support)

Admin users have access to an admin front-end interface

Depend on this group, user can do different action or not. (see tables below)

Sales user permissions:
|  | POST | GET | PUT | DELETE |
|---|:-:|:-:|:-:|:-:|
| Client | Yes | Only his clients | Only his clients | Only his clients |
| Contract | Yes | Only for those related to his clients | Only for those related to his clients | Only for those related to his clients |
| Event | Only for those related to his clients | No | No | Only for those related to his clients |

Support user permissions

|  | POST | GET | PUT | DELETE |
|---|:-:|:-:|:-:|:-:|
| Client | No | Only those related to his event | No | No |
| Contract | No | No | No | No |
| Event | No | Only his events | Only his events | No |


Users can also add some filters to the API endpoints.
Here are the filters enable:
- contract endpoint:
  - date_created
  - amount
  - last_name
  - email

- client endpoints:
  - last_name
  - email

- event endpoints:
  - date
  - last name
  - email
## Installation

### Clone the code source (using ssh)

    mkdir foo
    git clone git@github.com:jjbochard/P10_SoftDesk.git foo
    cd foo

### Create your virtual environnement

First, install [Python 3.6+](https://www.python.org/downloads/).

Then, create your virtual environnement :
qw
    python3 -m venv <your_venv_name>

Activate it :

- with bash command prompt

        source <your_venv_name>/bin/activate

- or with Windows PowerShell

        .\venv\Scripts\activate

Finally, install required modules

    pip3 install -r requirements.txt

To deactivate your venv :

    deactivate

### Django management commands and run Django

First, apply all migrations to the database :

    django epic_event/manage.py migrate


Then, start the server

    django epic_event/manage.py runserver

### Optionnal : configure your git repository with pre-commit (if you want to fork this project)

You can install pre-commit with python

    pip install pre-commit

You can install the configured pre commit hook with

    pre-commit install

## How to use

You can use [Postman](https://www.postman.com/) in order to test the endpoints

If you're not familiar with it, follow the [tutorial](https://learning.postman.com/docs/getting-started/introduction/)

## Possible improvements
- use front-view for all the API
- comment many functions
- do some refactor
