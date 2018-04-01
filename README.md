Techism
=======

**Note: Operation of the techism platform ended 2017.**

This repository contains the source code of techism.

## Setup

    $ sudo apt-get install python-pip python-virtualenv
    $ git clone git://github.com/techism/techism.git
    $ cd techism
    $ virtualenv --no-site-packages venv 
    $ source venv/bin/activate
    (venv)$ pip install -r dependencies.pip

## Development

### Start local development server

    (venv)$ ./manage.py runserver

or

    (venv)$ gunicorn_django techism

### Load testdata manually

    (venv)$ ./manage.py loaddata test-utils/fixture.json

### Save dependencies

    (venv)$ pip freeze > dependencies.pip

### Run tests

    (venv)$ ./manage.py test techism

### Edit test data

    $ cd test-utils
    $ vi fixture_template.json

Available Placeholders:
YESTERDAY
TOMORROW
NEXTWEEK

### Schema migrations

[South](http://south.readthedocs.org/) is used for database schema migrations.

Whenever changing the model create a new migration using:

    $ ./manage.py schemamigration techism --auto

Then apply the schema migration to the database:

    $ ./manage.py syncdb
    $ ./manage.py migrate


## Deployment

Create another virtualenv and install Fabric:

    $ virtualenv --no-site-packages venv-deploy
    $ source venv-deploy/bin/activate
    (venv-deploy)$ pip install Fabric

Deploy to development environment:

    (venv-deploy)$ fab deploy_dev

Deploy to staging environment:

    (venv-deploy)$ fab deploy_staging

Deploy to production environment:

    (venv-deploy)$ fab deploy_prod

There needs to be an SSH key stored on the server.

SSH host key fingerprints of the server are:

* RSA: 70:0e:9b:b7:76:7f:04:b7:10:cc:b1:f1:ac:88:a4:d3
* DSA: 9a:c3:c3:bc:5b:6b:f5:99:82:ce:7b:9c:a2:fc:29:e3
* ECDSA: 50:09:98:00:60:19:f4:b8:c1:4f:af:35:91:0c:38:d5


## Executing manage.py

If one needs to manually run manage.py, e.g. for loading data, 
some environment variables needs to be set:

For development:

    $ cd /srv/www/techism-dev
    $ source venv/bin/activate
    $ export DJANGO_SETTINGS_MODULE="techism.settings.dev"

For staging:

    $ cd /srv/www/techism-staging
    $ source venv/bin/activate
    $ export DJANGO_SETTINGS_MODULE="techism.settings.staging"

For production:

    $ cd /srv/www/techism-prod
    $ source venv/bin/activate
    $ export DJANGO_SETTINGS_MODULE="techism.settings.prod"

